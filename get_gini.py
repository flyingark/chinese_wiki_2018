# generate a csv file recording an article's number of revision,
# number of editor, Gini, conflict before and after
from __future__ import division
import csv
import json
from datetime import date, datetime, timedelta
from collections import Counter
import numpy as np

def GetGini(s):
	"""return normalized Gini coefficient"""
	if len(s) == 0:
		return ''
	elif len(s) == 1:
		return 1
	else:
		s.sort()
		res = 0
		n = len(s)
		for k in range(1,n):
			res = res + (s[k]-s[k-1])*k*(n-k)
		if res == 0:
			return 0
		else:
			return res / (sum(s) - n) / (n-1)

def TimestampToDate(ts):
	"""convert timestamp to date object"""
	return datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S').date()

# get the set of real editors
real_editor_set = set()
for line in csv.DictReader(open('../data/real_editor_list.csv', 'rb')):
	real_editor_set.add(line['editor_name'])

infile = open('../data/full_history.csv', 'rb')
reader = csv.DictReader(infile)
outfile = open('../data/gini.csv', 'wb')
writer = csv.DictWriter(outfile, 
						fieldnames = ['page_id', 'page_name', 'page_ns',
									  'gini_before', 'gini_after'])
writer.writeheader()

# initialize for new article
page_id = -1
page_name = ''
page_ns = -1
editor_rev_map_before = Counter()
editor_rev_map_after = Counter()

# go through the history file
for idx, line in enumerate(reader):
	print idx
	# output the results
	if page_id != line['page_id']:
		if page_id != -1:
			writer.writerow(
				{'page_id': page_id, 'page_name': page_name,
				 'page_ns': page_ns,
				 'gini_before': GetGini(editor_rev_map_before.values()),
				 'gini_after': GetGini(editor_rev_map_after.values())})
		page_id = line['page_id']
		page_name = line['page_name']
		page_ns = line['ns']
		editor_rev_map_before = Counter()
		editor_rev_map_after = Counter()

	# process current line
	if line['editor_name'] in real_editor_set:
		if (TimestampToDate(line['ts']) < date(2005, 10, 19) and
			TimestampToDate(line['ts']) >= date(2004, 10, 19)):
			if line['editor_name'] not in editor_rev_map_before:
				editor_rev_map_before[line['editor_name']] = 0
			editor_rev_map_before[line['editor_name']] += 1
		elif (TimestampToDate(line['ts']) < date(2006, 10, 19) and
			  TimestampToDate(line['ts']) >= date(2005, 10, 19)):
			if line['editor_name'] not in editor_rev_map_after:
				editor_rev_map_after[line['editor_name']] = 0
			editor_rev_map_after[line['editor_name']] += 1