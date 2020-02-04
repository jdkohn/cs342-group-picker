# cs342-group-picker

A Python program created by Matthew Brecher (mbb40) and Jacob Kohn (jk363) which assigns groups to topics for CS342.

# Requirements

All the requirements are in the `requirements.txt` file. To install them run `pip install -r requirements.txt` in the terminal.

# ToDo

In order to run this program correctly, set `num_topics` equal to the number of topics on line 7.

# Input format

The program reads line-by-line from the file groups.txt. An example of this file is included in the repository. 

A line must be structured either as:

netid_1 (string), netid_2 (string), choice1 (int), choice2 (int), choice3 (int)

OR

netid_1 (string), choice1 (int), choice2 (int), choice3 (int)

# TL;DR

0. Make sure that our friends to their top choice. 
1. Assign people to their top choice. 
1a. If there are ties, assign the people who are least likely to get their second and third choices to their first chioce. 
2. Repeat for second choice
3. Assign groups to third choice
3a. If there are ties, assign as many groups as possible to third choice
4. Assign remaining groups randomly to topics which have open spaces
5. Combine groups of 1 or 2 into groups of 3, 4, or 5
6. Print out what the groups to the console.

# Methodology

First, make sure that our friends get their first choice. Our friends' NetIDs are the `homies` array and will be automatically assigned to their first choice if space allows it.

If there are n groups and m topics, the ceiling of n / m groups can be assigned to a topic. This number will be referred to as q. 

Each group has a first choice, second choice and third choice. If x teams have topic 3 listed as their first choice, two things can happen. Either x is less than or equal to q or x is greater than q. In the first scenario, all of the x teams are assigned to topic 3. In the second situation, a number which we called the 'MiseryIndex' is calculated. This is done by multiplying 2 * (the number of spots remaining in their second choice) + (the number of spots remaining in their third choice). Then, the teams with the lowest MiseryIndex are assigned topic 3, as they would have less of a chance to get one of their top 3 choices.

This process is repeated for the second choice. For the third choice, if there are d spaces left in a topic, the program assigns the first d teams which listed that topic as their third choice to that topic. If there are still teams left, assign them to the first group which has open slots.

Finally, combine groups. Start with merging together groups of 2. If there are an odd number of groups of 2, fill spots 3 and 4 in the final group with people who signed up by themselves. Then add a fifth member to teams within that topic. 

Finally, print out the groups that were made.
