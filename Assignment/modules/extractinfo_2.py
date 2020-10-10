import sys
import os
import json

'''
Class:

ExtractInfo is a class designed to extracts all the necessary information from the file.

Arguments: 

f: The file that is going to be parsed.
et: The details about the comment syntax of the file that is going to be parsed.

The object after its creation should contain six attributes:

'''
class ExtractInfo:
    '''
    Initializes the class, the object by the end will have six variables, each representing the total number of lines
    part of it's category.

    Arguments:

    file: Is the file to be parsed
    languageSyntax: The specific comment syntax details of the programming file that is going to be parsed.

    Object's attributes:

    totalLines: Is the total number of lines in the file being parsed.
    commentLines: Is the total number of lines that are considered comments in the file being parsed, 
    it is singleLineComments + commentLinesWithinBlocks
    singleLineComments: Is the total number of lines that are single lined comments, includes todo comments.
    commentLinesWithinBlocks: Is the total number of lines within block comments.
    blockLineComments: Is the total number of block comments 
    todo: Is the total number of lines that are todo comments.

    Function:

    parse(): The function that conducts the parsing, look at analyse() function below for further details.
    '''
    def __init__(self,file,languageSyntax):
        self.totalLines = 0
        self.commentLines  = 0 
        self.singleLineComments  = 0 
        self.commentLinesWithinBlocks  = 0 
        self.blockLineComments  = 0 
        self.todo = 0
        self.parse(file,languageSyntax)

    '''
    Function:

    print(): Prints all the object's attributes to the terminal.
    
    '''

    def print(self):
        print("INFORMATION ABOUT FILE:\n")
        print("Total number of lines: "+str(self.totalLines))
        print("Total number of comment lines: "+str(self.commentLines))
        print("Total number of single line comments: "+str(self.singleLineComments))
        print("Total numnber of comment lines within blocks: "+str(self.commentLinesWithinBlocks))
        print("Total number of block line comments: "+str(self.blockLineComments))
        print("Total number of TODO's: "+str(self.todo))


    '''
    Function: 

    checkIfString(): checks if the line has a string and if so, if the commentSyntax is within the string or outside. 
    A string is defined for general purposed as anything between quotations.

    Arguments:

    line: the line of the file we are currently iterating on in analyse()
    commentSyntax: The syntax of a comment for a specific programming language.
    
    Return: 

    If there is a string and the commentSyntax is within the string return false, else return true 


    '''

    def checkIfString(self,line,commentSyntax):
        flag = 0
        begin = 0
        i = 0
        c = ""
        for char in line:                                    # iterates through char in the line 
            if (flag == 0 and (char == '"' or char == "'")): #if flag is zero, we haven't encountered a quotation mark yet. checks if the char is a quotation mark
                flag = 1 
                begin = i                                    # start of a subtring
                c = char  
            elif (flag == 1 and char == c):                  # if flag is 1, we check if current char equals to the closing of a quotation mark.
                flag = 0
                if (commentSyntax in line[begin:i]):         # check the substring from the open quotation to the closed quotation to see if commentSyntax is within
                    if (commentSyntax in line[i+1:len(line)]): # if it is, we check the rest of the string, by recursively calling on the remaining string.
                        return self.checkIfString(line[i+1:len(line)],commentSyntax)
                    else: 
                        return True                         # if it doesnt within the string return true 
            i += 1
        return False # return false if it does.s

    '''
    Function: 

    getTotalLines(): Counts the number of total lines in a file.

    Argument: 

    file: takes the file to be parsed as input.

    '''

    def getTotalLines(self,file):
        self.totalLines = len(file)      


    '''
    Function: 

    checkTODO(): checks whether the line contains a todoSyntax. If it does increment the todo by 1.

    Argument: 

    line: ine: the line of the file we are currently iterating on in analyse()
    todoSyntax: is the syntax of a single comment from the languageSyntax todo attribute.

    '''   
    
    def checkTodo(self,line,todoSyntax):
        line = line.replace(" ","")
        if (line.startswith(todoSyntax) or (todoSyntax in line and not self.checkIfString(line,todoSyntax))): #checks if line starts with todoSyntax or if not but contains todoSyntax, checks if todoSyntax is part of string or not 
            self.todo += 1
                
    '''
    Function: 

    checkSingleComments(): checks whether the line contains a singleCommentSyntax. If it does increment the singleLineComments attribute by 1.

    Argument: 

    line: the line of the file we are currently iterating on in analyse()
    singleCommentSyntax: is the syntax of a single comment from the languageSyntax singleComment attribute.

    '''   
    
    def checkSingleComment(self,line,singleCommentSyntax):
        if (line.startswith(singleCommentSyntax) or (singleCommentSyntax in line and not self.checkIfString(line, singleCommentSyntax))): # checks if line starts with singleCommentSyntax, or if not but contains todo, checks if singleCommentSyntax is part of string or not
            self.singleLineComments += 1

    '''
    Function: 

    checkBlockComment(): checks whether the line contains a blockCommentSyntax. If it does increment the blockLineComments attribute by 1.

    Argument: 

    line: the line of the file we are currently iterating on in analyse()
    blockCommentSyntax: is the array of syntax of a block comment from the languageSyntax blockComment attribute.

    Return: 

    if blockCommentSyntax[0] is found then it will return 1, else if blockCommentSyntax[1] is found it will return 0.

    '''   

    def checkBlockComment(self,line,blockCommentSyntax,blockFlag):
        if (blockCommentSyntax[0] in line and blockCommentSyntax[1] in line # checks the special case where block starts and ends on same line
        and line.find(blockCommentSyntax[0]) < line.find(blockCommentSyntax[1])): # makes sure that the block open syntax is before the block close syntax.
            self.blockLineComments += 1 
            return 0
        elif (blockFlag == 0 and blockCommentSyntax[0] in line): # if we find a block open syntax 
            return 1  #we return 1 to the blockFlag in parse.
        elif (blockFlag == 1 and blockCommentSyntax[1] in line): # given that we are in a block, we check if we have reached the end of the block by checking for the block closed syntax 
            self.blockLineComments += 1
            return 0 # return 0 to the blockFlag in parse to finish parsing the current block
        return blockFlag

    '''
    Function: 

    parse():  Analyses the file that needs to be analysed to extract the necessary information.
    The way this function works is that it iterates the file by going through each line and checking whether
    the line meets a particular requirement.     
    '''
          
            
    def parse(self,file,languageSyntax):


        # Opens the file and stores it as an array where each element is a line.
        file = open(file.name, "r")               
        file = file.readlines()
        
        '''
        Variables we use during the iteration of the array file 

        blockFlag: When dealing with a block comment, block comments don't necessarily end on the same line the way todo and
        single comments do, therefore if we encounter the opening part of a block comment in a line, we set the flag to 1, which
        makes sure lines that do not have the closing part of a block comment are analysed. Will be set back to 0, once we do 
        encounter the closing part of a block.

        blockCounter: When a blockFlag is 1, for every line we dont encounter the closing part of a block comment, we increment 
        blockCounter, which once we do encounter a closed, the blockFlag will be reset back to 0. BlockCounter will be added 
        to the CommentLinesWithinBlocks attribute and then be set  to 0.

        '''
        blockFlag = 0
        blockCounter = 0
        
        self.getTotalLines(file) # calls helper function to count the total number of lines.
        
        for line in file: # Iterates each line in the array 

            if (blockFlag == 0 and line):
                self.checkTodo(line.strip(),languageSyntax.todo) #checks if line contains todo

            if (blockFlag == 0 and line):
                self.checkSingleComment(line.strip(),languageSyntax.singleComment) # checks if line contains single comment

            if (blockFlag == 1 and line): # if block comment start was already found, keep incrementing 
                blockCounter += 1 
            elif (blockFlag == 0 and blockCounter > 0): # if blockFlag = 0 and blockCounter > 0, this means that in last iteration we encountered a closing 
                self.commentLinesWithinBlocks += blockCounter-1
                blockCounter = 0
            if (line):
                blockFlag = self.checkBlockComment(line.strip(),languageSyntax.blockComment,blockFlag) # checks if line contains block comment start or end 

        # We simply just add the singleLineComments and commentLinesWithinBlocks to get the total number of comment lines in the file.  
        self.commentLines = self.singleLineComments+self.commentLinesWithinBlocks
      