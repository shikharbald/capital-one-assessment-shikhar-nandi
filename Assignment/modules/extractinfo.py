import sys
import os 
import json 

'''
Class:

ExtractInfo is a class designed to extract all the necessary information from the file.

Arguments: 

f: The file that is going to be parsed.
languageSyntax: The details about the comment syntax of the file that is going to be parsed.

The object after its creation should contain six attributes:


'''
class ExtractInfo:
    '''
    Initializes the class, the object by the end will have six attributes, each representing the total number of lines
    part of it's category.

    Arguments:

    f: Is the file to be parsed
    et: The specific comment syntax details of the programming file that is going to be parsed.

    Object's attributes:

    totalLines: Is the total number of lines in the file being parsed.
    commentLines: Is the total number of lines that are considered comments in the file being parsed, 
    it is singleLineComments + commentLinesWithinBlocks
    singleLineComments: Is the total number of lines that are single lined comments, includes todo comments.
    commentLinesWithinBlocks: Is the total number of lines within block comments.
    blockLineComments: Is the total number of block comments 
    todo: Is the total number of lines that are todo comments.

    Function:

    parse(): The function that conducts the parsing, look at parse() function below for further details.

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

    checkifValidComment(): Checks whether a comment Syntax exists in the current substring of the string.
    The way the substring works is since we are iterating over every character in the string in parse(), 
    this helper function will create a substring from the current character being iterated to the length 
    of a given commentSyntax and then check if that substring matches the commentSyntax. An example would be
    if were checking "//TODO:" the java syntax ot todo comment and we were on a character "/" in the file, 
    we would check the next length of "//TODO:" string characters to see if it is "//TODO:"

    Arguments: 

    commentSyntax: is the comment Syntax we want to check exists within the current iteration of the string.
    str: is the file converted to a string.
    i: is the current index of the string we are iterating on.

    Return: 

    returns true if comment Syntax exists, else false.


    ''' 

    def checkIfValidComment(self,commentSyntax,str,i):
        # j is the intial length of a string we want to build.
        # temp is a string we want to build
        j = 0
        temp = ""
        
        # Build the temp string from the str (file converted to string) till we reach the length of the commentSyntax.
        # j < len(commentSyntax), as we want to create a string that forms from the current character to the length of the commentSyntax
        # i+j < len(str) makes sure we dont iterate over the length of the file.
        while (j < len(commentSyntax) and i+j < len(str)):
            temp += str[i+j] 
            j += 1
        if (temp == commentSyntax): # Make the comparison after temp is built.
            return True
        else: 
            return False

    '''
    Function:

    getString(): Converts a file to a string.

    Arguments:

    file: The file to be parsed.

    Return: 

    Returns the string

    '''

    def getString(self,file):
        # str will store the file as a string.
        str = ""

        #iterate the file and place append every line.
        for line in file:
            str += line
        return str.replace(" ","") # remove all the spaces between the characters, except "\n", to make parsing easier.


    '''
    Function: 

    getSymbols(): loads up data containing the open and its corresponding closed symbol.

    Return: 

    returns the object containing all that data.

    '''

    def getSymbols(self):
        symbols = {
            "(":")",
            '"':'"'
        }
        return symbols


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

    parse(): Analyses the file that needs to be analysed to extract the necessary information.
    The way this function works is that it iterates the file by converting it to a string
    which allows us to parse it character by character. If a character meets a certain 
    requirement, we use flags to indicate that a requirement has been met and until that flag
    is closed we can skip certain checks of other criterias.

    Arguments:

    f: The file that is going to be parsed/

    et: the comment syntax of the given programming file's type.

    '''

    def parse(self,file,languageSyntax):


        # These three lines load up the file and call a helper function, which will convert it to a string.
        file = open(file.name, "r")               
        file = file.readlines()
        str = self.getString(file)
        
        '''
        This calls a helper function that will load the symbols data, these symbols use opening and closing 
        syntax and is used to help that if we encounter a particular opening symbol, we ignore any type of comments 
        until we reach a corrseponding closing synbol. exmaple: //TODO: is a todo in java, but surrounding it in 
        quotations "//TODO" removes its ability to be a //TODO:
        '''
        symbols = self.getSymbols()

        # This calls a helper function that simply counts the total number of lines in a file and stores it in the 
        # totalLines attribute.
        self.getTotalLines(file)
        
        '''
        Variables we use during the iteration of the string.

        i: keeps track of which iteration we are in the string or in other words what character we are currently on.

        openFlag: A flag used to indicate if the current character is an opening symbol from the symbols variable defined above.
        0 means we have not encountered, 1 means we have already seen an opening symbol and will ignore analysing for any other 
        comments until we reach a corresponding closing symbol.

        singleFlag: A flag used to indicate if the current character is the same as the singlecomment attribute from the 
        languageSyntax object.  If it is 0, it means we have not yet encountered a singleComment. If it is 1, it means 
        we have encountered a single comment line until and can ignore analysing  every proceeding iteration until
        we reach a "\n" (new line), where it will change back to 0.

        blockFlag: A flag used to indicate if the current character is the same as the blockComment attribute from the
        languageSyntax object. If it is 0, it means we have not yet encountered a blockComment. If is 1, it means we
        have encountered the starting part of a block comment and can ignore analysing every proceeding iteration
        until we reach a character that matches the ending part of a block comment where it will change back to 0.

        blockCount: If a blockFlag is 1, we use blockCount to count the number of lines within a block Comment until
        the blockFlag becomes 0. We increment everytime we reach a "\n" (new line).

        c: If the current character is an opening symbol from the symbols object, c is used to store its corresponding 
        closing symbol, to help us evaluate if a character later on is the closed symbol.

        '''
        i = 0
        openFlag = 0 
        singleFlag = 0
        blockFlag = 0
        blockCount = 0
        closedSymbol = ""

        while (i < len(str)):
            if (str[i] == "\n"):                                            # checks if current character is \n.
                if (singleFlag == 1):                                       # given current character is \n, if singleFlag = 1, make it 0, as single comment would be finished.
                    singleFlag = 0
                if (blockFlag == 1):                                        # given current character is \n, if blockFlag = 1, increment blockCount, as we are in a new line.
                    blockCount += 1
            elif (openFlag == 0 and singleFlag == 0 and blockFlag == 0) :   # if all flags are 0, we need to check if current character matches some known character
                if (str[i] in symbols):                                     # check if current character is an open symbol.
                    openFlag = 1                                            
                    closedSymbol = symbols[str[i]]                          # gets the corresponding closedSymbol of the str[i]
                elif (self.checkIfValidComment(languageSyntax.todo,str,i)): # check if substring from current character to length of languageSyntax todo attribute is a todo comment
                    singleFlag = 1                                          
                    self.singleLineComments += 1                            # we add to signleLineComments as well as todo comments are also counted as single lines.
                    self.todo += 1 
                    i += len(languageSyntax.todo)-1                         
                elif (self.checkIfValidComment(languageSyntax.singleComment,str,i)): # check if substring from current character to length of languageSyntax singleComment attribute is a single comment
                    singleFlag = 1    
                    self.singleLineComments += 1                                            
                    i += len(languageSyntax.singleComment)-1                
                elif (self.checkIfValidComment(languageSyntax.blockComment[0],str,i)): # check if substring from current character to length of languageSyntaxe blockComment[0] attribute is a block comment start
                    blockFlag = 1                                           
                    self.blockLineComments += 1
                    i += len(languageSyntax.blockComment[0])-1
            elif (openFlag == 1 and str[i] == closedSymbol):                # else if openFlag is 1, checks if current character is the corresponding closedSymbol.
                openFlag = 0
            elif (blockFlag == 1):                                          # else if blockFlag is 1 check if current character to length of languageSyntax block comment[1] attribute is a block comment end
                if (self.checkIfValidComment(languageSyntax.blockComment[1],str,i)): 
                    blockFlag = 0
                    if (blockCount > 0):                                    # if blockCount > 0, we want to add to the commentLinesWithinBlocks 
                        self.commentLinesWithinBlocks += blockCount-1
                        blockCount = 0                                      # we reset so next blockComments will start at zero, if encounter one
                    i += len(languageSyntax.blockComment[1])-1
            
            i += 1

        
        # We simply just add the singleLineComments and commentLinesWithinBlocks to get the total number of comment lines in the file.
        self.commentLines = self.singleLineComments+self.commentLinesWithinBlocks
        
        
      