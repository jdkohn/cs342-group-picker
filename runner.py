
import pandas as pd
import random 
import math

num_topics = 3
GROUP_INDEX = ['Student1', 'Student2', 'Choice1', 'Choice2', 'Choice3']


def parseLine(line):
	parts = line.split(',')

	group = pd.Series(index=GROUP_INDEX)

	if len(parts) == 5:
		group['Student1'] = parts[0]
		group['Student2'] = parts[1]
		group['Choice1'] = int(parts[2])
		group['Choice2'] = int(parts[3])
		group['Choice3'] = int(parts[4])
	
	elif len(parts) == 4:
		group['Student1'] = parts[0]
		group['Student2'] = None
		group['Choice1'] = int(parts[1])
		group['Choice2'] = int(parts[2])
		group['Choice3'] = int(parts[3])
	else:
		group = None

	return group

def coinFlip():
	return random.choice([True, False])


def parseFile(filename):
	group_file = open(filename, 'r') 
	group_lines = group_file.readlines() 

	all_groups = []
	for line in group_lines:
		all_groups.append(parseLine(line))

	return pd.DataFrame(all_groups)
	     
all_groups = parseFile('groups.txt')

# set max number of groups that can be assigned to one topic
max_groups_in_topic = math.ceil(len(all_groups.index) / num_topics)











