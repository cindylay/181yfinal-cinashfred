## pre-processing script 
import re
import os

def retrieve_file_paths(path):
    AllFiles = list(os.walk(path))   # get every folder
    all_file_paths = []

    for item in AllFiles:    # every folder
        foldername, LoDirs, LoFiles = item

        for filename in LoFiles:   # every file in every folder
            if filename[-2:] != 'py': continue   # only txt files

            fullfilename = foldername + "/" + filename  # usual stuff...
            all_file_paths.append(fullfilename)
    return all_file_paths


def readfile( filePath ):
    """
        opens txt file and returns it as string
    """
    f = open(filePath, 'r')
    contents = f.read()
    f.close()

    # print(f"These are the file document contents: \n{contents}")
    return contents

def findDocString( string3 ):
    """
        given a string, finds the docstring and returns it with its quotes
    """

    final_string = ""
    matches = re.finditer('"""', string3)
    matches_positions = [match.start() for match in matches] 

    if len(matches_positions) < 2:
        return "no docstring"

    return string3[matches_positions[0] : matches_positions[1]+3] 

    # for i in range(len(matches_positions) - 1):
    #     print(len(matches_positions))
    #     func_text = contents[matches_positions[i]:matches_positions[i+1]]
    #     # docstring = findDocString(func_text)
    #     final_string +=  func_text + end
    #     print('did it work')

    # print(string)
    # string2 = '\"\"\"werewxwefe\"\"\"'
    
    # m = re.search('x', string)

    # m = re.search('"{3}(.*?)"{3}', string3)
    # print(m.group(0), 'hi')
    # return str(m.group(0))

    # if string == "":
    #     return 'empty string'
    # idx = 0
    # idx2 = 0
    # while True:
    #     if string[idx : idx+3] == '"""': # we found the start of a docstring
    #         # print(string[idx : idx+3], 'just to check')
    #         sub_string = string[idx+3:]
    #         for i in range(len(sub_string)):
    #             if sub_string[i:i+3] == '"""': # found the end of the docstring
    #                 # print(sub_string[i:i+3], 'just to check 2.0')
    #                 idx2 = idx+3+i+3
    #         return string[idx:idx2]
    #     else:
    #         idx += 1

### TESTS for findDocString ### 
test0 = ''
test1 = 'def findDocString( string ):\n"""hello"""\nidx = 0\nwhile True:'

test1a = 'def findDocString( string ):\n\"\"\"hello\"\"\"\nidx = 0\nwhile True:'

test2 = '"""\ngiven a string, gives back the string\ninput:"a string"\noutput:"string"\n"""'
test3 = 'def sq(x):\n"""Returns the square of its argument\nArgument x: a number (int of float)\n"""\nreturn x*x'

# print(test1 == test1a)

# print(f"test1 {test1}\n")
# print(f"test2 {test2}\n")
# print(f"test3 {test3}\n")
# assert findDocString(test0) == 'empty string', 'should be empty string'
# assert findDocString(test1) == '"""hello"""', 'should be: """hello"""'
# assert findDocString(test2) == '"""\ngiven a string, gives back the string\ninput:"a string"\noutput:"string"\n"""', 'should be: """\ngiven a string, gives back the string\ninput:"a string"\noutput:"string"\n"""'
# assert findDocString(test3) == '"""Returns the square of its argument\nArgument x: a number (int of float)\n"""', 'should be: """Returns the square of its argument\nArgument x: a number (int of float)\n"""'

# print(findDocString(test2), '2!!!')

def processText( contents ):
    """
    takes in a string full of text file contents and cleans it
    """
    # FUNC_AMOUNT = 0
    # NEW_LINES = 0
    end = "\n <|endoftext|> \n"
 
    final_string = ""
    matches = re.finditer("def", contents)
    matches_positions = [match.start() for match in matches]  

    for i in range(len(matches_positions) - 1):
        # print(len(matches_positions))
        func_text = contents[matches_positions[i]:matches_positions[i+1]]
        docstring = findDocString(func_text)
        final_string += docstring + '\n' + func_text + end
        # print('did it work')

    return final_string + "\n"

    # print(f"\nThis file has {FUNC_AMOUNT} functions")
    # print(f"This file has {NEW_LINES} new lines")

### run script


if True:
    all_file_paths = retrieve_file_paths("CS5")
    cum_file = ''
    for f in all_file_paths:
        if f == "CS5/hw2pr2.py":
            print(processText(readfile(f)))
        cum_file += processText(readfile(f))

    f = open("preprocess.txt","w+")
    f.write(cum_file)
    f.close()
    