#!/usr/bin/env python
# Python program to convert JSON file to CSV


import json
import csv
import re
import sys


# Opening JSON file and loading the data into the variable data
input_data = json.load(sys.stdin)

# now we will open a file for writing
output_file = open('output_file.csv', 'w')

# create the csv writer object
csv_writer = csv.writer(output_file)

headers = [
	'cookie',
	'table',
	'priority',
	'matches',
	'actions',
	'resubmit-table'
]
csv_writer.writerow(headers)

for input_row in input_data:
	matches = input_row['matches']
	if any(['icmp6' in match or 'udp6' in match or 'ipv6' in match for match in matches]):
		continue

	resubmit_table = ''
	actions = input_row['actions']
	for action in list(actions):
		for action_key in action.viewkeys():
			re_result = re.match('^resubmit\(,(\d+)', action_key)
			if re_result:
				resubmit_table = re_result.group(1)
				actions.remove(action)
				break

	output_row = [
		input_row['cookie'],
		input_row['table'],
		input_row['priority'],
		matches,
		actions,
		resubmit_table
	]
	csv_writer.writerow(output_row)

output_file.close()
