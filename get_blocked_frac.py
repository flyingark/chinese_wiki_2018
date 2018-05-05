"""
This script identifies the leader associated with each article
"""

from __future__ import division
import csv
from collections import defaultdict
from datetime import datetime, date
import numpy as np
from scipy.stats import norm

def TimestampToDate(ts):
	"""convert timestamp to date object"""
	return datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S').date()

def get_leader_origin(editor_rev_dict):
	"""
	Return a set of editors who are identified as leaders.
	"""
	# find the threshold value
	if editor_rev_dict == {}:
		return []
	else:
		threshold = 0
		min_distance = 2
		len_ = len(editor_rev_dict)
		max_ = max(editor_rev_dict.values())
		for idx, value in enumerate(sorted(editor_rev_dict.values(),
										   reverse=True)):
			if pow((idx+1) / len_, 2) + pow(value / max_, 2) < min_distance:
				threshold = value
				min_distance = pow((idx+1) / len_, 2) + pow(value / max_, 2)

		leader_origin_list = []
		for key, value in editor_rev_dict.iteritems():
			if value > threshold:
				leader_origin_list.append(key)

	return leader_origin_list

def get_leader_interquartile(editor_rev_dict):
	"""
	Return a set of editors who are identified as leaders using inter-quarticle rules.
	"""
	if editor_rev_dict == {}:
		return []
	else:
		values_ = np.array(editor_rev_dict.values())
		lower_quartile = np.percentile(values_, 25)
		upper_quartile = np.percentile(values_, 75)
		threshold = upper_quartile + 1.5 * (upper_quartile - lower_quartile)
		leader_iq_list = []
		for key, value in editor_rev_dict.iteritems():
			if value > threshold:
				leader_iq_list.append(key)

	return leader_iq_list		


# create a dictionary recording whether an real editor is blocked
editor_block_dict = {}
infile = open('../data/real_editor_list.csv', 'rb')
reader = csv.DictReader(infile)
for idx, line in enumerate(reader):
	print idx
	editor_block_dict[line['editor_name']] = (
		True if line['blocked'] == '1' else False)

infile = open('../data/full_history.csv', 'rb')
reader = csv.DictReader(infile)
outfile = open('../data/article_leader.csv', 'wb')
writer = csv.DictWriter(outfile, 
						fieldnames = ['page_id', 'page_name', 'page_ns',
									  'block_frac',
									  'leader_block_frac_origin',
									  'block_frac_by_leader_origin',
									  'leader_block_frac_iq',
									  'block_frac_by_leader_iq'])
writer.writeheader()

# initialization
page_id = -1
page_name = ''
page_ns = -1
# a dict recording the number of revisions by an editor
editor_rev_dict = defaultdict(lambda: 0)

# go through the history file
for idx, line in enumerate(reader):
	print idx
	if page_id != line['page_id']:
		if page_id != -1:
			leader_origin_list = get_leader_origin(editor_rev_dict)
			leader_iq_list = get_leader_interquartile(editor_rev_dict)

			# calculate block_frac
			num_rev_blocked = 0
			num_rev_by_leader_origin = 0
			num_rev_by_blockedleader_origin = 0
			num_rev_by_leader_iq = 0
			num_rev_by_blockedleader_iq = 0
			num_rev = 0
			for editor, rev in editor_rev_dict.iteritems():
				num_rev += rev
				if editor_block_dict[editor] == True:
					num_rev_blocked += rev
				if editor in leader_origin_list:
					num_rev_by_leader_origin += rev
				if editor_block_dict[editor] == True and editor in leader_origin_list:
					num_rev_by_blockedleader_origin += rev
				if editor in leader_iq_list:
					num_rev_by_leader_iq += rev
				if editor_block_dict[editor] == True and editor in leader_iq_list:
					num_rev_by_blockedleader_iq += rev

			block_frac = num_rev_blocked / num_rev if num_rev > 0 else ""
			
			leader_block_frac_origin = num_rev_by_blockedleader_origin / num_rev_by_leader_origin if num_rev_by_leader_origin > 0 else ""
			block_frac_by_leader_origin = num_rev_by_blockedleader_origin / num_rev_blocked if num_rev_blocked > 0 else ""

			leader_block_frac_iq = num_rev_by_blockedleader_iq / num_rev_by_leader_iq if num_rev_by_leader_iq > 0 else ""
			block_frac_by_leader_iq = num_rev_by_blockedleader_iq / num_rev_blocked if num_rev_blocked > 0 else ""


			writer.writerow({'page_id': page_id, 'page_name': page_name,
							 'page_ns': page_ns,
							 'block_frac': block_frac,
							 'leader_block_frac_origin': leader_block_frac_origin,
							 'block_frac_by_leader_origin': block_frac_by_leader_origin,
							 'leader_block_frac_iq': leader_block_frac_iq,
							 'block_frac_by_leader_iq': block_frac_by_leader_iq
							 })
		
		page_id = line['page_id']
		page_name = line['page_name']
		page_ns = line['ns']
		editor_rev_dict = defaultdict(lambda: 0)

	if (TimestampToDate(line['ts']) < date(2005, 10, 19) and
		line['editor_name'] in editor_block_dict):
		editor_rev_dict[line['editor_name']] += 1