import re
import argparse
import os
import ast


class Checker:
    def __init__(self):
        file_name = input()
        self.file_open(file_name)

    def file_open(self, file):
        n = 0
        empty_line = 0
        with open(file, 'r') as f1:
            tree = ast.parse(f1.read())

        with open(file, 'r') as f2:
            for line in f2.readlines():
                n += 1
                self.s001(line, n, file)
                self.s002(line, n, file)
                self.s003(line, n, file)
                self.s004(line, n, file)
                self.s005(line, n, file)
                if line == '\n':
                    empty_line += 1
                elif empty_line > 2 and line != '\n':
                    self.s006(n, file)
                    empty_line = 0
                else:
                    empty_line = 0
                self.s007(line, n, file)
                self.s008(line, n, file)
                self.s009(line, n, file)
                self.s010(tree, n, file)
                self.s011(tree, n, file)
                self.s012(tree, n, file)

    def s001(self, line, num, file):
        try:
            assert len(line) <= 79, f'{file}: Line {num}: S001 Too long'
        except AssertionError as err:
            print(err)

    def s002(self, line, num, file):
        multiple = 4
        indent = len(line) - len(line.lstrip())
        if indent % multiple and line != '\n':
            print(f'{file}: Line {num}: S002 Indentation is not a multiple of four')

    def s003(self, line, num, file):
        if ';' in line and not (re.match(r'.*[\'\"].*;.*[\'\"]', line) or re.match(r'.*#.*;.*', line)):
            print(f'{file}: Line {num}: S003 Unnecessary semicolon')

    def s004(self, line, num, file):
        if '#' in line and not re.match(r'.*\s\s#.*', line) and not re.match(r'#.*', line):
            print(f'{file}: Line {num}: S004 At least two spaces required before inline comments')

    def s005(self, line, num, file):
        if '#' in line and re.match(r'.*?#.*[Tt][Oo][Dd][Oo].*?', line):
            print(f'{file}: Line {num}: S005 TODO found')

    def s006(self, num, file):
        print(f'{file}: Line {num}: S006 More than two blank lines used before this line')

    def s007(self, line, num, file):
        if re.match('.*(class|def)\s{2,}', line):
            print(f'{file}: Line {num}: S007 Too many spaces after construction_name (def or class)')

    def s008(self, line, num, file):
        if re.match('^class.*_', line) or re.match('^class [a-z]', line):
            class_name = line.split()[1].replace(':', '')
            print(f"{file}: Line {num}: S008 Class name '{class_name}' should use CamelCase")

    def s009(self, line, num, file):
        if re.match('def.*[A-Z]', line):
            function_name = line.split()[1].replace(':', '')
            print(f"{file}: Line {num}: S009 Function name '{function_name}' should use snake_case")

    def s010(self, tree, num, file):
        for el in ast.walk(tree):
            if isinstance(el, ast.FunctionDef):
                for argument_name in [a.arg for a in el.args.args]:
                    if re.match(r'^[A-Z]', argument_name):
                        print(f"{file}: Line {num}: S010 Argument name '{argument_name}' should be written snake_case")

    def s011(self, tree, num, file):
        for el in ast.walk(tree):
            if isinstance(el, ast.Name) and isinstance(el.ctx, ast.Store):
                variable_name = el.id
                if re.match(r'^[A-Z]', variable_name):
                    print(f"{file}: Line {num}: S011 Variable '{variable_name}' in function should be snake_case")

    def s012(self, tree, num, file):
        for el in ast.walk(tree):
            if isinstance(el, ast.FunctionDef):
                for item in el.args.defaults:
                    if isinstance(item, ast.List):
                        print(f"{file}: Line {num}: S012 Default argument value is mutable")


class ProjectParser(Checker):
    def __init__(self):
        self.args = argparse.ArgumentParser()
        self.args.add_argument('path')
        parser = self.args.parse_args()

        file = parser.path
        if os.path.isdir(file):
            for i in sorted(os.listdir(file)):
                if re.match(r'.*\.py$', i):
                    path = file + '/' + i
                    self.file_open(path)
        else:
            self.file_open(file)


if __name__ == '__main__':
    project = ProjectParser()
