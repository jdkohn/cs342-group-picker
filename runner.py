
import pandas as pd
import numpy as np
import random 
import math

num_topics = 4
GROUP_INDEX = ['Student1', 'Student2', 'Choice1', 'Choice2', 'Choice3', 'AssignedGroup', 'MiseryIndex']
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
	     
def getNextAvailableTopic():
	'''
	Gets the next available topic

	Returns
	-------
	topic : int
		The index of the next topic with room for groups, -1 if not possible
	'''
	for topic in range(num_topics):
		if num_spaces_left[topic] != 0:
			return topic

	return -1

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

############ CHOICE 1 ##################

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

# Create the misery index !!!! Lower is worse
for index, row in all_groups.iterrows():
	if effective_spaces_left[row['Choice1']] == 0 and np.isnan(row['AssignedGroup']):
		choice_two_rem = effective_spaces_left[row['Choice2']]
		choice_three_rem = effective_spaces_left[row['Choice3']]

		all_groups.loc[index, 'MiseryIndex'] = 2.1 * choice_two_rem + choice_three_rem

# sort in order to misery index
all_groups = all_groups.sort_values(by=['MiseryIndex'])

for topic in range(num_topics):

	# group had more than possible first choices
	if effective_spaces_left[topic] != num_spaces_left[topic]:
		# Select first num_spaces_left[topic] with lowest misery index
		top_x = all_groups.loc[(all_groups['Choice1'] == topic) & np.isnan(all_groups['AssignedGroup'])].head(num_spaces_left[topic])

		for index, row in top_x.iterrows():
			all_groups.loc[(all_groups['Student1'] == row['Student1']) & (all_groups['Student2'] == row['Student2']), 'AssignedGroup'] = topic


		num_spaces_left[topic] = 0

########### CHOICE 2 #############

for topic in range(num_topics):

	if num_spaces_left[topic] != 0:

		top_choice_groups = all_groups.loc[(all_groups['Choice2'] == topic) & np.isnan(all_groups['AssignedGroup'])]
		
		# if all people can get their top choice, give them their top choice
		if len(top_choice_groups.index) <= num_spaces_left[topic]:
			all_groups.loc[(all_groups['Choice2'] == topic) & np.isnan(all_groups['AssignedGroup']), 'AssignedGroup'] = topic
			num_spaces_left[topic] -= len(top_choice_groups.index)
			effective_spaces_left[topic] -= len(top_choice_groups.index)
		else:
			effective_spaces_left[topic] = 0

# Create the misery index !!!! Lower is worse
for index, row in all_groups.iterrows():
	if effective_spaces_left[row['Choice2']] == 0 and np.isnan(row['AssignedGroup']):
		choice_three_rem = effective_spaces_left[row['Choice3']]

		all_groups.loc[index, 'MiseryIndex'] = choice_three_rem

# sort in order to misery index
all_groups = all_groups.sort_values(by=['MiseryIndex'])

for topic in range(num_topics):

	# group had more than possible first choices
	if effective_spaces_left[topic] != num_spaces_left[topic]:
		# Select first num_spaces_left[topic] with lowest misery index
		top_x = all_groups.loc[(all_groups['Choice2'] == topic) & np.isnan(all_groups['AssignedGroup'])].head(num_spaces_left[topic])

		for index, row in top_x.iterrows():
			all_groups.loc[(all_groups['Student1'] == row['Student1']) & (all_groups['Student2'] == row['Student2']), 'AssignedGroup'] = topic

		num_spaces_left[topic] = 0

########### CHOICE 3 #############

for topic in range(num_topics):

	if num_spaces_left[topic] != 0:

		top_choice_groups = all_groups.loc[(all_groups['Choice3'] == topic) & np.isnan(all_groups['AssignedGroup'])]
		
		# if all people can get their top choice, give them their top choice
		if len(top_choice_groups.index) <= num_spaces_left[topic]:
			all_groups.loc[(all_groups['Choice3'] == topic) & np.isnan(all_groups['AssignedGroup']), 'AssignedGroup'] = topic
			num_spaces_left[topic] -= len(top_choice_groups.index)
			effective_spaces_left[topic] -= len(top_choice_groups.index)
		else:
			effective_spaces_left[topic] = 0


for topic in range(num_topics):
	if num_spaces_left[topic] != effective_spaces_left[topic]:
		max_spaces_left = num_spaces_left[topic]

		for i in range(max_spaces_left):
			# get top 'num_spaces_left' groups from that topic randomly
			# assign those to group

			row = all_groups.loc[(all_groups['Choice3'] == topic) & np.isnan(all_groups['AssignedGroup'])].head(1)

			if len(row.index) > 0:

				all_groups.loc[(all_groups['Student1'] == row['Student1']) & (all_groups['Student2'] == row['Student2']), 'AssignedGroup'] = topic

########## RANDOM ASSIGN #########

remaining = all_groups.loc[np.isnan(all_groups['AssignedGroup'])]

if len(remaining.index):
	topic = 0

	for index, row in remaining.iterrows():
		
		s1 = row['Student1']
		s2 = row['Student2']

		while num_spaces_left[topic] == 0:
			topic = topic + 1

		all_groups.loc[(all_groups['Student1'] == s1) & (all_groups['Student2'] == s2), 'AssignedGroup'] = topic

remaining = all_groups.loc[np.isnan(all_groups['AssignedGroup'])]

if len(remaining.index) != 0:
	print('FAILED TO PLACE THESE GROUPS:')
	print(remaining)

print('\n\nFINAL GROUPS:')
print(all_groups[['Student1', 'Student2', 'AssignedGroup']])


