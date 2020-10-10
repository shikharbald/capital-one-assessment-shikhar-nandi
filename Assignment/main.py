# These are various packages needed for the program to work.
import sys
import os
import json


# Import classes that will be used to help extract information, located in the modules folder.
from modules.extensiontype import ExtensionType
from modules.extractinfo import ExtractInfo


"""
Function:

checkExtension(): checks whether the given file is a valid program file, if it is returns the extension type (Needed for analysis).

Arguments: 

fileName: is the name of the file going to be parsed.
syntaxes: is a json object that can help tell us whether a given file matches any program languages we know the syntaxes of.

Exception: 

If file is found to not be a programming file will throw an Invalid File exception.

Return:

Returns a string that is the extensio portion of the file's name.

"""

def checkExtension(fileName,syntaxes):
    name = os.path.basename(fileName)
    extension = os.path.splitext(fileName)[1]

    if (name.startswith('.') or name == "" or extension == "" or extension not in syntaxes):
        raise TypeError("Invalid File")
    else:
        return extension 

'''
Function: 

openJSON(): opens the file containing information about particular syntax for each programming language and returns a usable object.

Return: 

returns a json object.
'''
def openJSON():
    with open('./syntaxes.json') as f:
        syntaxes = json.load(f)
    return syntaxes
        
'''
Function: 

main(): executes the scanning of the file.

Arguments: 

file: The file that is going to be parsed.

'''
def main(file):
    # syntaxes: used to store the json object containing information about programming languages and their comment syntax.
    syntaxes = openJSON()
    fileName = file.name # stores name of the file
    # extension: used to store the extension name of a file, for example if a file is named hello.java, extension will contain the .java part.
    extension = checkExtension(fileName,syntaxes)
    # et: stores all the necessary comment syntax pertaining to a specific programming language.
    languageSyntax = ExtensionType(extension, syntaxes)
    # ei: extracts all the necessary information from the given programming file.
    ei = ExtractInfo(file,languageSyntax)
    # prints the retrived information onto the terminal.
    ei.print()
    

'''
The main call of the program file, 

Exception: 

If no file is given, will throw a File Not Found Exception.

'''    
if __name__ == "__main__":
    if (len(sys.argv) <= 1):
        raise FileNotFoundError("No file found")
    with open(sys.argv[1], 'r') as f:
        file = f
    main(file)