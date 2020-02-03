# cs342-group-picker

A Python program created by Matthew Brecher (mbb40) and Jacob Kohn (jk363) which assigns groups to topics for CS342.

# Input format

The program reads line-by-line from the file groups.txt. An example of this file is included in the repository. 

A line must be structured either as:

netid_1 (string), netid_2 (string), choice1 (int), choice2 (int), choice3 (int)
OR
netid_1 (string), choice1 (int), choice2 (int), choice3 (int)

# Methodology

First, make sure that our friends get their first choice. Our friends' NetIDs are the `homies` array and will be automatically assigned to their first choice if space allows it.

If there are n groups and m topics, the ceiling of n / m groups can be assigned to a topic. This number will be referred to as q. 

Each group has a first choice, second choice and third choice. If x teams have topic 3 listed as their first choice, two things can happen. Either x is less than or equal to q or x is greater than q. In the first scenario, all of the x teams are assigned to topic 3. In the second situation, a number which we called the 'MiseryIndex' is calculated. This is done by multiplying 2 * (the number of spots remaining in their second choice) + (the number of spots remaining in their third choice). Then, the teams with the lowest MiseryIndex are assigned topic 3, as they would have less of a chance to get one of their top 3 choices.

This process is repeated for the second choice. For the third choice, if there are d spaces left in a topic, the program assigns the first d teams which listed that topic as their third choice to that topic. If there are still teams left, assign them to the first group which has open slots.

At the end, the table of groups will be saved as groups.csv.
