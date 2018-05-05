"""
This script generates editors infomation, including whether one made revisions in during the block, ratio of traditional character.
"""

from __future__ import division
import csv
from datetime import datetime
from collections import defaultdict

def rev_inblock(ts, ts_fmt='%Y-%m-%dT%H:%M:%S'):
	"""
	determine whether the timestamp of a revision is within the block
	"""
	ts = datetime.strptime(ts, ts_fmt)
	if ts >= datetime(2002, 6, 2) and ts <= datetime(2002, 6, 21):
		return True
	elif ts >= datetime(2004, 9, 23) and ts <= datetime(2004, 9, 27):
		return True
	elif ts >= datetime(2005, 10, 19) and ts <= datetime(2006, 10, 10):
		return True
	elif ts >= datetime(2006, 11, 17) and ts <= datetime(2007, 07, 15):
	    return True
	else:
		return False

editor_dict = defaultdict(lambda: {'editor_id': '',
								   'editor_ip': '',
								   'total_char_add': 0,
								   'total_tradchar_add': 0,
								   'trad_ratio': 0,
								   'within_block': False,
								   'blocked': False,
								   'join_date': datetime(9999,12,31)})

infile = open('../data/full_history.csv', 'rb')
reader = csv.DictReader(infile)
outfile = open('../data/editor_info.csv', 'wb')
writer = csv.DictWriter(outfile, 
						fieldnames=['editor_id', 'editor_name', 'editor_ip',
									'total_char_add', 'total_tradchar_add',
									'trad_ratio', 'in_block', 'blocked',
									'join_date'])
writer.writeheader()

for idx, line in enumerate(reader):
	print idx
	editor_name = line['editor_name']
	if editor_name not in editor_dict:
		editor_dict[editor_name] = {'editor_name': editor_name,
									'editor_id': line['editor_id'],
									'editor_ip': line['editor_ip'],
									'total_char_add': 0,
									'total_tradchar_add': 0,
									'trad_ratio': 0,
									'in_block': False,
									'blocked': False,
									'join_date': datetime.strptime(line['ts'],
										'%Y-%m-%dT%H:%M:%S')}
	editor_dict[editor_name]['total_char_add'] += int(line['char_add'])
	editor_dict[editor_name]['total_tradchar_add'] += int(line['tradchar_add'])
	if (editor_dict[editor_name]['in_block'] == True or
		rev_inblock(line['ts']) == True):
		editor_dict[editor_name]['in_block'] = True

for editor_info in editor_dict.values():
	editor_info['trad_ratio'] = editor_info['total_tradchar_add'] / max(editor_info['total_char_add'], 1)
	editor_info['blocked'] = (editor_info['trad_ratio'] <= 0.21 and
							  editor_info['in_block'] == False)
	writer.writerow(editor_info)
