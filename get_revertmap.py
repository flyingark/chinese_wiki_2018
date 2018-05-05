"""
This script identifies reverts in the full history.
The identification of revert is based on the byte/char size. If the byte/char size after an revision is the same as a previous one, this revision is regarded as a revert.
"""

import csv

def identify_revert(rev_list):
	"""
	Return a list of revert info. Each item corresponds a revert described by ts, reverted_rev_id, reverting_rev_id, reverted_editor_name and reverting_editor_name
	"""
	revert_list = []
	for i in range(len(rev_list)):
		for j in range(i-1, -1, -1):
			if (rev_list[i]['byte'] == rev_list[j]['byte'] and
				rev_list[i]['char'] == rev_list[j]['char']):
				revert_list.append(
					{'ts': rev_list[i]['ts'],
					 'reverted_rev_id': rev_list[j]['rev_id'],
					 'reverting_rev_id': rev_list[i]['rev_id'],
					 'reverted_editor_name': rev_list[j]['editor_name'],
					 'reverting_editor_name': rev_list[i]['editor_name']})
				break
	return revert_list

infile = open('../data/full_history.csv', 'rb')
reader = csv.DictReader(infile)
outfile = open('../data/revert.csv', 'wb')
writer = csv.DictWriter(outfile, fieldnames=['page_id','page_name',
											 'page_ns', 'ts',
											 'reverted_rev_id',
											 'reverting_rev_id',
											 'reverted_editor_name',
											 'reverting_editor_name'])
writer.writeheader()

# initialization
page_id = -1
page_name = ''
page_ns = -1
# a list recording revision info in the current article
rev_list = []

# go through the history file
for idx, line in enumerate(reader):
	print idx
	if page_id != line['page_id']:
		if page_id != -1:
			revert_list = identify_revert(rev_list)
			for revert in revert_list:
				revert['page_id'] = page_id
				revert['page_name'] = page_name
				revert['page_ns'] = page_ns
				writer.writerow(revert)
		page_id = line['page_id']
		page_name = line['page_name']
		page_ns = line['ns']
		rev_list = []
	rev_list.append(line)

# write the last record
print idx
revert_list = identify_revert(rev_list)
for revert in revert_list:
	revert['page_id'] = page_id
	revert['page_name'] = page_name
	revert['page_ns'] = page_ns
	writer.writerow(revert)