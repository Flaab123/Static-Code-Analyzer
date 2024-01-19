import re
import os
from operator import attrgetter
import sys

for arg in sys.argv:
    user_input = arg

if re.match(r".*.py$", user_input):
    directory = False
    file = user_input
    files = False
else:
    directory = user_input
    file = False
    to_read_files = []
    for root, dirs, files in os.walk(user_input, topdown=False):
        for name in files:
            if re.match(r".*.py$", name):
                to_read_files.append(os.path.join(root, name))


class ErrorList:
    """Class representing all errors"""
    all_errors = []

    def __init__(self, line, error_code, filename=None):
        self.line = line
        self.error_code = error_code
        self.filename = filename
        ErrorList.all_errors.append(self)

    def print_err(self):
        print(f"{self.filename}: Line {self.line}: {self.error_code}")


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
        comment = line[comment_index + 1:]
    elif not comment_index:
        not_comment = line
        comment = None
    else:
        not_comment = line[0:comment_index]
        comment = line[comment_index + 1:]
    return not_comment, comment


def chk_s001(filename, name):
    for line_n, line in enumerate(filename, 1):
        if len(line) > 79:
            ErrorList(line_n, "S001 Too long", name)


def chk_s002(filename, name):
    for line_n, line in enumerate(filename, 1):
        not_comment, _ = split_comment(line)
        if not_comment:
            indentation = 0
            for char in line:
                if char != ' ':
                    break
                else:
                    indentation += 1
            if indentation % 4 != 0:
                ErrorList(line_n, "S002 Indentation is not a multiple of four", name)


def chk_s003(filename, name):
    for line_n, line in enumerate(filename, 1):
        not_comment, _ = split_comment(line)
        if not_comment:
            not_comment = not_comment.rstrip()
            if re.match(r".*;$", not_comment):
                ErrorList(line_n, "S003 Unnecessary semicolon", name)


def chk_s004(filename, name):
    for line_n, line in enumerate(filename, 1):
        not_comment, comment = split_comment(line)
        if not_comment != None and comment != None:
            indentation = 0
            for char in not_comment[::-1]:
                if char != ' ':
                    break
                else:
                    indentation += 1
            if indentation < 2:
                ErrorList(line_n, "S004 Less than two spaces before inline comments", name)


def chk_s005(filename, name):
    for line_n, line in enumerate(filename, 1):
        _, comment = split_comment(line)
        if comment != None:
            if re.match(r".*todo.*", comment, re.IGNORECASE):
                ErrorList(line_n, "S005 TODO found", name)


def chk_s006(filename, name):
    blank_index = [index for index, line in enumerate(filename) if line == '']
    consecutive_blanks = 0
    last_index = -1
    for index in blank_index[0:]:
        if index == last_index + 1:
            consecutive_blanks += 1
            last_index = index
            if index == blank_index[-1] and consecutive_blanks >= 2:
                ErrorList(index + 2, "S006 More than two blank lines used before this line", name)
        else:
            if consecutive_blanks >= 2:
                ErrorList(index + 2, "S006 More than two blank lines used before this line", name)
            consecutive_blanks = 0
            last_index = index


def chk_s007(filename, name):
    for line_n, line in enumerate(filename, 1):
        not_comment, _ = split_comment(line)
        if not_comment:
            if re.match(r".*def( ){2,}.*", not_comment):
                ErrorList(line_n, "S007 Too many spaces after 'def'", name)
            if re.match(r".*class( ){2,}.*", not_comment):
                ErrorList(line_n, "S007 Too many spaces after 'class'", name)


def chk_s008(filename, name):
    for line_n, line in enumerate(filename, 1):
        not_comment, _ = split_comment(line)
        if not_comment:
            if re.match(r"[ ]*class( ){1,}[a-z_].*[(:]", not_comment) or re.match(r"[ ]*class( ){1,}[A-Z].*_.*[(:]",
                                                                                  not_comment):
                class_name = re.search(r'class(.*?)[\(:]', not_comment).group(1).strip()
                ErrorList(line_n, f"S008 Class name '{class_name}' should use CamelCase", name)


def chk_s009(filename, name):
    for line_n, line in enumerate(filename, 1):
        not_comment, _ = split_comment(line)
        if not_comment:
            if re.match(r"[ ]*def( ){1,}_*[A-Z].*[(:]", not_comment):
                func_name = re.search(r'def(.*?)[\(:]', not_comment).group(1).strip()
                ErrorList(line_n, f"S009 Function name '{func_name}' should use snake_case", name)


def run_all_checks(file, name):
    chk_s001(file, name)
    chk_s002(file, name)
    chk_s003(file, name)
    chk_s004(file, name)
    chk_s005(file, name)
    chk_s006(file, name)
    chk_s007(file, name)
    chk_s008(file, name)
    chk_s009(file, name)


if file:
    reading_file = import_file(file)
    run_all_checks(reading_file, file)
elif directory:
    for name in to_read_files:
        reading_file = import_file(name)
        run_all_checks(reading_file, name)

for err in sorted(ErrorList.all_errors, key=attrgetter('filename', 'line', 'error_code')):
    err.print_err()
