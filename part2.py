import re
import os

class ErrorList:
    """Class representing all errors"""
    all_errors = []

    def __init__(self, line, error_code, filename=None):
        self.line = line
        self.error_code = error_code
        self.filename = filename
        ErrorList.all_errors.append(self)
        
    def print_err(self):
        if self.filename:
            print(f"")
        else:
            print(f"Line {self.line}: {self.error_code}")


def import_file(filename):
    if not os.path.isfile(filename):
        print("File not found.")
    else:
        imported_file = open(filename, 'r')
        imported_data = [line.rstrip('\n') for line in imported_file]
    return imported_data

def split_comment(line):
    comment_index = None
    for char, index in enumerate(line):
        if char == '#':
            comment_index = index
            break
    if comment_index == 0:
        not_comment = None
        comment = line[comment_index +1:]
    elif comment_index > 0:
        not_comment = line[0:comment_index-1]
        comment = line[comment_index +1:]
    else:
        not_comment = line
        comment = None
    return not_comment, comment
        
    

def chk_s001(filename):
    for line_n, line in enumerate(filename,1):
        if len(line) > 79:
            ErrorList(line_n,"S001 Too long")
            
def chk_s002(filename):
    for line_n, line in enumerate(filename,1):
        if not line:
            pass
        else:
            indentation = 0
            for char in line:
                if char != ' ':
                    break
                else:
                    indentation += 1
            if indentation % 4 != 0:
                ErrorList(line_n,"S002 Indentation is not a multiple of four") 
                
def chk_s003(filename):
    for line_n, line in enumerate(filename,1):
        if len(line) > 79:
            ErrorList(line_n,"S001 Too long")
            
def chk_s004(filename):
    for line_n, line in enumerate(filename,1):
        if len(line) > 79:
            ErrorList(line_n,"S001 Too long")
            
def chk_s005(filename):
    for line_n, line in enumerate(filename,1):
        if len(line) > 79:
            ErrorList(line_n,"S001 Too long")
            
def chk_s006(filename):
    for line_n, line in enumerate(filename,1):
        if len(line) > 79:
            ErrorList(line_n,"S001 Too long")
            
            
A = import_file("test.py")
chk_s001(A)

for B in A:
    print(B == '')

for err in ErrorList.all_errors:
    err.print_err()

