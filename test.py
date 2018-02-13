import os
import sys
import re

var_to_be_search = 'TOTAL-READ'
print (sys.version)
code = dict()
para_start = dict()
para_end = dict()
var_track = list()
para_name =list()

procedure_div = ''
linkage_storage_start = ''
working_storage_start = ''

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'cobol.txt')

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
         
         #increment the counter for populating the dictionary       
        item = item + 1

# define a variable to store a paragraph name temporarily to calculate the start
last_para_name = ''
line_no = 0

for line_number in code:
    # and end of a paragraph
    # ignore all the commented out lines
    if line_number > procedure_div:
        if len(code[line_number][1:2]) > 0:
            if code[line_number][1:2] != ' ':
                # mark the ending line number for the last paragraph read
                
                if len(para_start) > 0:
                
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

# find out all the paragraphs called in a given paragraph
for para in para_name:
    
    # get the start line and end line of a given paragraph
    para_start_line = para_start[para]
    para_end_line = para_end[para]

    # Now go through each line within a paragraph to find the paragraph name
    for line_no in range(para_start_line, para_end_line):
        if code[line_no][0:1]  != '*':
            wordList = code[line_no][5:66].split()
        print(wordList)

print(para_start)
print(para_end)
print(para_name)
print(var_track)
print(procedure_div)
print(working_storage_start)
print(linkage_storage_start)
