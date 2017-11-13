#!/usr/bin/python
# very hacky convertor
# does some of the donkey work required to port the ruby examples to 
# python
#
# Some observations
# a) probably would be better starting with the old ycp examples (as these
#    don't have the Ops.xyz and Convert.xyz additional code (which we dont't
#    use
# b) using yacc/bison with a simple lang desc for the above probably would be
#    more successful.
# c) still not sure if we shouldn't have converted
#    :somesymbol -> Symbol("somesymbol Certainly there is some opportunity for
#    conversion ambiguity and confusion with the present approach

import sys
import re

def convert_file(input_file):
    file_contents = open(input_file, "r")
    converted = ""
    for line in file_contents:
        # swallow Yast.import "UI" => 
        if "Yast.import" in line:
            continue
        # swallow nil (on it's own)
        if "nil" == line.strip():
            continue
        # swallow end (on it's own)
        if "end" == line.strip():
            continue

        # module Yast => from yast import *
        if line.strip() == "module Yast":
            converted = converted + "from yast import *\n"
            continue
        # begin => while True:
        if line.strip() == "begin":
            converted = converted + line.replace("begin", "while True:")
            continue

        if "true" in line:
            line = line.replace("true", "True")

        if "false" in line:
            line = line.replace("false", "False")

        if "nil" in line:
            line = line.replace("nil", "None")

        # && => and
        if '&&' in line:
	    line = line = line.replace('&&', 'and')

        # || => or
        if '||' in line:
	    line = line.replace('||', 'or')

        # only handle trivial elseif (with no condintional)
        if 'elseif' in line.strip():
            converted = converted + line.replace('elseif', 'elif:')
            continue

        # only handle trivial else (with no condintional)
        if 'else' in line.strip():
            converted = converted + line.replace('else', 'else:')
            continue

        # UI.UserInput => UI.UserInput()
        if line.strip().endswith('UI.UserInput'):
            line = line.replace('UI.UserInput', 'UI.UserInput()')

        # UI.CloseDialog => UI.CloseDialog()
        if line.strip().endswith('UI.CloseDialog'):
            line = line.replace('UI.CloseDialog', 'UI.CloseDialog()')

        # make sure the main class has no indentation
        if line.strip().startswith("class") and "Client" in line:
            line = line.lstrip()
       
        if "def" in line:
            if "def main" in line:
                line = line.replace('def main', 'def main(self):')
#            else:
#                # make sure all other methods are not 'class'
#                # methods
#                line = line.lstrip()
        # => => :
        if "=>" in line:
                line = line.replace('=>', ':')


        # Yast::someclass.new.main => someclass().main()
        newline = re.sub(r'Yast::([A-Za-z][A-Za-z0-9]+)\.new\.main', r'\1().main()',line)
        # class xyz < Client => start of line class xyz:
        newline = re.sub(r'class\s+([A-Za-z][_A-Za-z0-9]+)\s+<\s+Client', r'class \1:', newline)
        # @anyword => "word"
        newline = re.sub(r'@([A-Za-z][A-Za-z0-9]+)', r'\1', newline)
        # :anyword => "word"
        newline = re.sub(r'([(,\s]+):([A-Za-z][_A-Za-z0-9]+)', r'\1"\2"', newline)
        # term(..) => Term(..)
        newline = re.sub(r'term\(',r'Term(', newline)
        # Builtins => ycpbuiltins
        if 'Builtins' in newline:
		newline = newline.replace('Builtins', 'ycpbuiltins')
        # true => True
        if 'true' in line:
		newline = newline.replace('true', 'True')
        converted = converted + newline 
    return converted

def main():
    if len(sys.argv) < 2:
        print "usage: %s file"
        sys.exit(1)
    input_file1 =  sys.argv[1]
    contents = convert_file(input_file1)
    print contents
if __name__ == '__main__':
    main()
