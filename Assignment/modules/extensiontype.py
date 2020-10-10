import sys
import os
import json


''' 
Class: 

ExtensionType class acquires all important comment syntax related to the type of programming file being parsed.
example: .java files have different symbols for indicating single comments and block comments compared to .py files.

'''

class ExtensionType:
    '''
    Initializes the class, the object by the end will have three attributes, each representing the syntax of a single
    /block/todo comment is represented in a specific programming language.

    Arguments:

    extension: The file's type
    syntaxes: A json object containing details of every programming language's comment syntax.

    Object's parameters:

    singleComment: The syntax of a single comment for a given programming language
    blockComment: The syntax of a block comment for a given programming language, 
    is an array because block Comments syntax is representing by an opening and closing syntax.
    todo: The syntax of a todo comment for a given programming language

    '''
    def __init__(self,extension, syntaxes):
        self.singleComment = self.getSingleCommentSyntax(extension, syntaxes)
        self.blockComment = self.getBlockCommentSyntax(extension, syntaxes)
        self.todo = self.getTodoSyntax(extension, syntaxes)

    '''
    Function: 

    getSingleCommentSymbol(): gets the specific language syntax that defines a single comment.

    Arguments: 

    extension: The file's type
    syntaxes: A json object containing details of every programming language's comment syntax.

    Return:

    returns a string that represents a single comment syntax for a given extension

    '''
    #gets the single comment structure based on the file type/extension
    def getSingleCommentSyntax(self,extension, syntaxes):
        return syntaxes[extension]["firstComment"]
    '''
    Function: 

    getBlockCommentSymbol(): gets the specific language syntax that defines a block comment.

    Arguments: 

    extension: The file's type
    syntaxes: A json object containing details of every programming language's comment syntax.

    Return: 

    returns an array of two elements that represents the beginning syntax and end syntax of a block comment for a given extension

    '''

    #gets the multicomment structure based on the file type/extension
    def getBlockCommentSyntax(self,extension, syntaxes):
        return syntaxes[extension]["blockComment"]

    '''
    Function: 

    getTODO(): gets the specific language syntax that defines a todo comment.

    Arguments: 

    extension: The file's type
    syntaxes: A json object containing details of every programming language's comment syntax.
    
    Return:

    returns a string that represents a todo comment syntax for a given extension
    '''
      
    #gets the todo structure based on the file type/extension
    def getTodoSyntax(self,extension, syntaxes):
        return syntaxes[extension]["todo"]