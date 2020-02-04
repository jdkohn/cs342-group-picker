
import pandas as pd
import numpy as np
import random 
import math

num_topics = 4
GROUP_INDEX = ['Student1', 'Student2', 'Choice1', 'Choice2', 'Choice3', 'AssignedGroup', 'MiseryIndex', 'FinalAssignment']
FINAL_INDEX = ['Student1', 'Student2', 'Student3', 'Student4', 'Student5', 'Topic']
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
		group['FinalAssignment'] = False
	
	elif len(parts) == 4:
		group['Student1'] = parts[0].strip()
		group['Student2'] = None
		group['Choice1'] = int(parts[1])
		group['Choice2'] = int(parts[2])
		group['Choice3'] = int(parts[3])
		group['FinalAssignment'] = False
	else:
		group = None

	return group

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

def readNetIds(filename):
	'''
	Parses a file and returns a list of all the net ids

	Paramaters
	----------
	filename : string
		The name of the file to parse

	Returns
	--------
	ids : [string]
		Array of all the netids in CS342
	'''
	netid_file = open(filename, 'r')
	netids = netid_file.readlines()

	ids = []
	for netid in netids:
		ids.append(netid.replace('\n', ''))

	return ids


all_groups = parseFile('groups.txt')
all_students = readNetIds('netids.txt')

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

				all_groups.loc[(all_groups['Student1'] == row['Student1'].iloc[0]) & (all_groups['Student2'] == row['Student2'].iloc[0]), 'AssignedGroup'] = topic
				num_spaces_left[topic] -= 1


########## RANDOM ASSIGN #########

remaining = all_groups.loc[np.isnan(all_groups['AssignedGroup'])]

if len(remaining.index):
	topic = 0



	for index, row in remaining.iterrows():
		s1 = row['Student1']
		s2 = row['Student2']

		while num_spaces_left[topic] == 0:
			topic = topic + 1

		if s2 is None:
			all_groups.loc[(all_groups['Student1'] == s1) & (all_groups['Student2'].isnull()), 'AssignedGroup'] = topic
		else:
			all_groups.loc[(all_groups['Student1'] == s1) & (all_groups['Student2'] == s2), 'AssignedGroup'] = topic

remaining = all_groups.loc[np.isnan(all_groups['AssignedGroup'])]


all_final_groups = []
# put groups together
for topic in range(num_topics):

	final_groups = []

	# get all 2-person groups
	groups_in_topic = all_groups.loc[(all_groups['AssignedGroup'] == topic) & ~all_groups['Student2'].isnull() & ~all_groups['FinalAssignment']]

	while len(groups_in_topic.index) > 1:
		top_two = groups_in_topic.head(2)

		g = pd.Series(index=FINAL_INDEX)
		g['Student1'] = top_two['Student1'].iloc[0]
		g['Student2'] = top_two['Student2'].iloc[0]
		g['Student3'] = top_two['Student1'].iloc[1]
		g['Student4'] = top_two['Student2'].iloc[1]
		g['Student5'] = None
		g['Topic'] = topic

		final_groups.append(g)

		all_groups.loc[(all_groups['Student1'] == g['Student1']) | (all_groups['Student1'] == g['Student3']), 'FinalAssignment'] = True

		groups_in_topic = all_groups.loc[(all_groups['AssignedGroup'] == topic) & ~all_groups['Student2'].isnull() & ~all_groups['FinalAssignment']]


	# Add single groups
	single_groups = all_groups.loc[(all_groups['AssignedGroup'] == topic) & all_groups['Student2'].isnull() & ~all_groups['FinalAssignment']]

	if len(groups_in_topic.index) == 1:
		g = pd.Series(index=FINAL_INDEX)
		g['Student1'] = groups_in_topic['Student1'].iloc[0]
		g['Student2'] = groups_in_topic['Student2'].iloc[0]

		if len(single_groups.index) >= 2:
			g['Student3'] = single_groups['Student1'].iloc[0]
			g['Student4'] = single_groups['Student1'].iloc[1]
		elif len(single_groups.index) == 1:
			g['Student3'] = single_groups['Student1'].iloc[0]
			g['Student4'] = None
		else:
			g['Student3'] = None
			g['Student4'] = None

		g['Student5'] = None
		g['Topic'] = topic

		final_groups.append(g)

		all_groups.loc[(all_groups['Student1'] == g['Student1']) | (all_groups['Student1'] == g['Student3']) | (all_groups['Student1'] == g['Student4']), 'FinalAssignment'] = True


	# Now only have single groups
	single_groups = all_groups.loc[(all_groups['AssignedGroup'] == topic) & all_groups['Student2'].isnull() & ~all_groups['FinalAssignment']]
	final_group_index = 0

	while len(single_groups.index) > 0:
		foundGroup = False 
		create_new_group = False
		group_ids = []

		while not foundGroup:

			if final_group_index >= len(final_groups):
				group_ids = single_groups['Student1'].values
				create_new_group = True
				break

			if final_groups[final_group_index]['Student5'] is None:
				final_groups[final_group_index]['Student5'] = single_groups['Student1'].iloc[0]
				foundGroup = True
				all_groups.loc[(all_groups['Student1'] == single_groups['Student1'].iloc[0]), 'FinalAssignment'] = True
			else:
				final_group_index += 1

		if create_new_group:
			g = pd.Series(index=FINAL_INDEX)
			for i in range(len(group_ids)):
				col_str = 'Student' + str(i + 1)
				g[col_str] = group_ids[i]
				g['Topic'] = topic

			final_groups.append(g)
			break

		single_groups = all_groups.loc[(all_groups['AssignedGroup'] == topic) & all_groups['Student2'].isnull() & ~all_groups['FinalAssignment']]


	all_final_groups = all_final_groups + final_groups

final_groups = pd.DataFrame(all_final_groups)

assigned_students = []
for i in range(5):
	student_str = 'Student' + str(i + 1)

	students = final_groups[student_str].values.tolist()

	if students is None:
		continue


	if len(assigned_students) > 0:
		assigned_students = assigned_students + students
	else: 
		assigned_students = students

unassigned = set(all_students) - set(assigned_students)

if len(unassigned) > 0:
	print('Failed to assign to groups:')
	for s in unassigned:
		print(s)

for index, row in final_groups.iterrows():
	s = ''

	for i in range(5):
		student_str = 'Student' + str(i + 1)
		if row[student_str] is not None and type(row[student_str]) is str:
			s = s + row[student_str] + ','

	s = s + str(row['Topic'])

	print(s)





