import re
import os
from operator import attrgetter


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
    if line == '':
        not_comment = None
        comment = None
        return not_comment, comment
    for index, char in enumerate(line):
        if char == '#':
            comment_index = index
            break
    if comment_index == 0:
        not_comment = None
        comment = line[comment_index+1:]
    elif not comment_index:
        not_comment = line
        comment = None
    else:
        not_comment = line[0:comment_index]
        comment = line[comment_index+1:]
    return not_comment, comment
        
def chk_s001(filename):
    for line_n, line in enumerate(filename,1):
        if len(line) > 79:
            ErrorList(line_n,"S001 Too long")
            
def chk_s002(filename):
    for line_n, line in enumerate(filename,1):
        not_comment, _ = split_comment(line)
        if not_comment:
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
        not_comment, _ = split_comment(line)
        if not_comment:
            not_comment = not_comment.rstrip()
            if not_comment[-1] == ';':
                ErrorList(line_n,"S003 Unnecessary semicolon") 
            
def chk_s004(filename):
    for line_n, line in enumerate(filename,1):
        not_comment, comment = split_comment(line)
        if not_comment != None and comment != None:
            indentation = 0
            for char in not_comment[::-1]:
                if char != ' ':
                    break
                else:
                    indentation += 1
            if indentation < 2:
                ErrorList(line_n,"S004 Less than two spaces before inline comments") 

def chk_s005(filename):
    for line_n, line in enumerate(filename,1):
        _, comment = split_comment(line)
        if comment != None:
            if re.match(r".*todo.*",comment,re.IGNORECASE):
                ErrorList(line_n,"S005 TODO found") 
            
def chk_s006(filename):
    blank_index = [index for index,line in enumerate(filename) if line == '']
    consecutive_blanks = 0
    last_index = -1
    for index in blank_index[0:]:
        if index == last_index+1:
            consecutive_blanks += 1
            last_index = index
            if index == blank_index[-1] and consecutive_blanks >= 2:
                ErrorList(index+2,"S006 More than two blank lines used before this line") 
        else: 
            if consecutive_blanks >= 2:
                ErrorList(index+2,"S006 More than two blank lines used before this line") 
            consecutive_blanks = 0
            last_index = index           
            
            
A = import_file("test.py")
chk_s001(A)
chk_s002(A)
chk_s003(A)
chk_s004(A)
chk_s005(A)
chk_s006(A)


for err in sorted(ErrorList.all_errors, key=attrgetter('filename', 'line', 'error_code')):
    err.print_err()
