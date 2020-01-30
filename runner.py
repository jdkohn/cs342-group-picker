
import pandas as pd
import numpy as np
import random 
import math

num_topics = 3
GROUP_INDEX = ['Student1', 'Student2', 'Choice1', 'Choice2', 'Choice3', 'AssignedGroup']
homies = ['jk363', 'mbb40']

def parseLine(line):
	'''
	Parses a line from the groups text file

	Paramaters
	----------
	line : String
		Assumed to be either in the format of --
			'student, student, choice, choice, choice'
			OR
			'student, choice, choice, choice'

	Returns
	---------
	group : pd.Series
		A Series object which has the parsed information
	'''
	parts = line.split(',')

	group = pd.Series(index=GROUP_INDEX)

	if len(parts) == 5:
		group['Student1'] = parts[0].strip()
		group['Student2'] = parts[1].strip()
		group['Choice1'] = int(parts[2])
		group['Choice2'] = int(parts[3])
		group['Choice3'] = int(parts[4])
	
	elif len(parts) == 4:
		group['Student1'] = parts[0].strip()
		group['Student2'] = None
		group['Choice1'] = int(parts[1])
		group['Choice2'] = int(parts[2])
		group['Choice3'] = int(parts[3])
	else:
		group = None

	return group

def coinFlip():
	'''
	Returns True or False at random

	Returns
	--------
	True or False (randomly selected)
	'''
	return random.choice([True, False])


def parseFile(filename):
	'''
	Parses a file and returns the DataFrame of groups

	Paramaters
	-----------
	filename : string
		The name of the file to parse

	Returns
	--------
	DataFrame
		returns the DataFrame of all of the groups in the file

	'''
	group_file = open(filename, 'r') 
	group_lines = group_file.readlines() 

	all_groups = []
	for line in group_lines:
		all_groups.append(parseLine(line))

	return pd.DataFrame(all_groups)
	     


all_groups = parseFile('groups.txt')

# set max number of groups that can be assigned to one topic
max_groups_in_topic = math.ceil(len(all_groups.index) / num_topics)

num_spaces_left = []
effective_spaces_left = []
for i in range(num_topics):
	num_spaces_left.append(max_groups_in_topic)
	effective_spaces_left.append(max_groups_in_topic)


# make sure all our friends get their top choice
for homie in homies:
	row = all_groups.loc[((all_groups['Student1'] == homie) | (all_groups['Student2'] == homie)) & np.isnan(all_groups['AssignedGroup'])]

	if len(row.index) == 1:
		preferred_choice = row['Choice1'][0]

		if num_spaces_left[preferred_choice] > 0:
			all_groups.loc[((all_groups['Student1'] == homie) | (all_groups['Student2'] == homie)) & np.isnan(all_groups['AssignedGroup']), 'AssignedGroup'] = preferred_choice
			num_spaces_left[preferred_choice] -= 1
			effective_spaces_left[preferred_choice] -= 1

# Assigning choice 1
for topic in range(num_topics):
	top_choice_groups = all_groups.loc[(all_groups['Choice1'] == topic) & np.isnan(all_groups['AssignedGroup'])]
	
	# if all people can get their top choice, give them their top choice
	if len(top_choice_groups.index) <= num_spaces_left[topic]:
		all_groups.loc[(all_groups['Choice1'] == topic) & np.isnan(all_groups['AssignedGroup']), 'AssignedGroup'] = topic
		num_spaces_left[topic] -= len(top_choice_groups.index)
		effective_spaces_left[topic] -= len(top_choice_groups.index)
	else:
		effective_spaces_left[topic] = 0


print(all_groups)
print(num_spaces_left)
print(effective_spaces_left)


# for choice in num_spaces_left:
# 	for topic_num in range(num_topics):









