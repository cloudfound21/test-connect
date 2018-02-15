import os
import sys
import re

def para_list( para_nme ):
    
    para_path = para_nme
    # Check if the list which has the called paragraphs within the given paragraph is 
    # empty or not
    if len(para_tree[para_nme]) > 0:
        # iterate through all the values in the list which is for all the paragraphs within
        # a paragraph
        for para_nm in para_tree[para_nme]:
            # call the same function recursively to build the procedural path of the program
            para_path = para_path + "+" + para_list(para_nm)

    return para_path

# this variable is just to track down a variable -- function still have to be built
var_to_be_search = 'TOTAL-READ'
# print (sys.version)

# This dictionary has all the lines of the code including comments 
# Column 7-72 only
code = dict()
# This dictionary will hold the paragraph names as the key and value as the starting
# line number of the paragraph
para_start = dict()
# This dictionary will hold the paragraph names as the key and value as the ending
# line number of the paragraph
para_end = dict()
var_track = list()
# List of all paragraphs in the program
para_name = list()

# This dictionary will hold the paragraph names as the key and value as the list of
# all Paragraphs called in the given Paragraph
para_tree = dict()

# This dictionary will hold all Comments for a given Paragraph. Key will be Paragraph name
para_comment = dict()
# This list will hold all the initial comments for a Paragraph temporarily
para_comment_list = list()

# A list to hold the list of Paragraphs temporarily
para_tree_branch = list()

# Variable to hold the line number of the PROCEDURE division
procedure_div = ''
# Variable to hold the starting line number of the LINKAGE Section
linkage_storage_start = ''
# Variable to hold the starting line number of the WORKING STORAGE Section
working_storage_start = ''

# THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
# my_file = os.path.join(THIS_FOLDER, 'cobol.txt')

item = 0
with open("cobol.txt") as f:
    for line_terminated in f:
        
        # only pick the code that is between column 7 and 72
        code[item] = line_terminated.rstrip('\n')[6:72]
        
        # This piece of code identifies the various section of the program and also
        # establishes the location of the variable used.
        # ignore all the commented out lines
        if code[item][0:1]  != '*':

            if var_to_be_search in code[item]:
               var_track.append(item)

            if code[item][1:10] == 'PROCEDURE':
                procedure_div = item
            
            if code[item][1:16] == 'WORKING-STORAGE':
                working_storage_start = item

            if code[item][1:16] == 'LINKAGE-SECTION':
                linkage_storage_start = item
         
         #increment the counter for populating the dictionary key 'Code' i.e. line number       
        item = item + 1

############################################################################################
# start and end lines of a paragraph
############################################################################################
# define a variable to store a paragraph name temporarily to calculate the start
last_para_name = ''
line_no = 0

for line_number in code:
    # print(str(line_number)+code[line_number])
    # ignore all the commented out lines
    if line_number > procedure_div:
        # this condition checks if we have '\n' when the line is empty
        # when someone copy pastes the code in text file
        if len(code[line_number][1:2]) > 0:
            #Checks the column 8 is empty or not
            if code[line_number][1:2] != ' ':
                # mark the ending line number for the last paragraph read          
                if last_para_name in para_start:
                    
                    para_end[last_para_name] = line_number - 1

                # append the name of the new paragraph to the list
                para_name.append(code[line_number].strip()[:-1])
                
                # set the start line of the paragraph                
                para_start[code[line_number].strip()[:-1]] = line_number
                
                # save the name of the current paragraph to be checked in the next iteration
                last_para_name = code[line_number].strip()[:-1]
    
    line_no = line_no + 1

# populate the end lines for the last paragraph
para_end[last_para_name] = line_no - 1

############################################################################################
# find out all the paragraphs called in a given paragraph
############################################################################################
for para in para_name:
    # initialize the list which will hold the paragaphs called with a Paragraph
    para_tree_branch = []
    # initialize the list which will hold the comments for a Paragraph
    para_comment_list = []

    # get the start line and end line of a given paragraph
    para_start_line = para_start[para]
    para_end_line = para_end[para]
    initial_comment = 'YES'
    # print(para)
    # print(para_start_line)
    # print(para_end_line)
    # Now go through each line within a paragraph to find the paragraph name
    #   The very first line here will have the Paragraph Name starting from Column 8
    #   which we ignore by adding + 1 to the starting line of this paragraph
    for line_no in range(para_start_line + 1, para_end_line):
        if code[line_no][0:1]  != '*':
            # set the indicator so that only the comments just after the paragraph name
            # is parsed and displayed in the report
            initial_comment = 'NO'

            # This will give the list of all words in a given statement
            wordList = code[line_no][5:66].split()

            # look for a Paragraph name only when there are more than or equal to 2 words in a statement
            if len(wordList) >= 2:
                # In order to get the Paragraph name, the first word in the list or line
                # must be 'PERFORM' and second word which might be UNTIL and VARYING should 
                # not be counted
                if wordList[0] == 'PERFORM' and wordList[1] != 'UNTIL' and wordList[1] != 'VARYING':
                    # Further check if there is a hyphen '-' in the Paragraph name. I have never
                    # seen a Paragraph name without it
                    if ("-" in wordList[1]):
                        # Since the second word in the line or the Paragraph name might end up with
                        # a period. hence removing the period if found.
                        para_tree_branch.append(wordList[1].rstrip('.'))
        else:
            if initial_comment == 'YES':
                para_comment_list.append(code[line_no])

    # Add the list which is the Paragraph names called for a given Paragraph to the Dictionary            
    para_tree[para] = para_tree_branch
    # Add the comments for a Paragraph name to the dictionary
    para_comment[para] = para_comment_list

# call the function para_list which is a recursive function to get the all the paths in the
# cobol program
program_flow = para_list(para_name[0])
# Split the Paragraph names to get a list which will later be used in the report
program_flow_list = program_flow.split(sep='+')


# print(para_comment)
# print(program_flow_list)    
# print(para_tree)
# print(para_start)
# print(para_end)
# print(para_name)
# print(para_name[0])
# print(var_track)
# print(procedure_div)
# print(working_storage_start)
# print(linkage_storage_start)


