#!/usr/bin/env python
# Python program to convert openflow dump from JSON file to CSV
#
# usage:
# step1: flozer --json < flows_dump.txt > flows.json
# step2: zjson2csv < data.json


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
	'matches-protocol',
	'matches-reg5',
	'matches-reg6',
	'actions',
	'actions-resubmit-table'
]
csv_writer.writerow(headers)

for input_row in input_data:
	matches = input_row['matches']
	if any(['icmp6' in match or 'udp6' in match or 'ipv6' in match for match in matches]):
		continue

	matches_protocol = ''
	matches_reg5 = ''
	matches_reg6 = ''
	matches = input_row['matches']
	protocols = ['arp', 'tcp', 'udp', 'icmp', 'ip']
	for match in list(matches):
		for match_key, match_value in match.viewitems():
			if match_key == 'reg5':
				matches_reg5 = match_value
			if match_key == 'reg6':
				matches_reg6 = match_value
			if match_key in protocols:
				matches_protocol = match_key

	actions_resubmit_table = ''
	actions = input_row['actions']
	for action in list(actions):
		for action_key in action.viewkeys():
			re_result = re.match('^resubmit\(,(\d+)', action_key)
			if re_result:
				actions_resubmit_table = re_result.group(1)
				break

	output_row = [
		input_row['cookie'],
		input_row['table'],
		input_row['priority'],
		matches,
		matches_protocol,
		matches_reg5,
		matches_reg6,
		actions,
		actions_resubmit_table
	]
	csv_writer.writerow(output_row)

output_file.close()
