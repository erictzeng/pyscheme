"""
Copyright (C) 2011 AUTHORS

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import data
import env
import prim
import util

import re
import sys
import exception
import readline
import traceback

glob = env.GlobalEnv()

###################
#  Lexer, Parser  #
###################

def make_list(input):
    # Input: string
    tokenized = tokenize_list(input)
    expression_list = data.Nil()
    while tokenized:
        token = tokenized.pop()
        if isinstance(token, str):
            if token == ".":
                expression_list = data.ConsPair(tokenized.pop(), expression_list.car)
            else:
                expression_list = data.ConsPair(make_list(token[1:-1]), expression_list)
        else:
            expression_list = data.ConsPair(token, expression_list)
    return expression_list

def tokenize_list(input_string):
    # Returns a list of tokens, leaving parenthesized expressions as is
    result = []
    while input_string:
        # Handle the shorthand quote
        quote = re.match(r"'", input_string)
        if quote:
            input_string = input_string[1:]

        # Match the beginning of the input
        whitespace   = re.match(r" +", input_string)
        integer      = re.match(r"\d+", input_string)
        dot          = re.match(r"\.", input_string)
        variable     = re.match(r"[!$%&*+-./:<=>?@^_~a-zA-Z]([!$%&*+-./:<=>?@^_~a-zA-Z0-9])*", input_string)
        boolean      = re.match(r"#[tf]", input_string)
        # Removes starting whitespace
        if whitespace:
            token = None
            index = len(whitespace.group())
        # Matches integers
        elif integer:
            token = data.IntLiteral(int(integer.group()))
            index = len(integer.group())
        # Matches the dot in literal pairs
        elif dot:
            token = "."
            index = 1
        # Matches variables
        elif variable:
            token = data.Identifier(variable.group())
            index = len(variable.group())
        # Matches booleans
        elif boolean:
            token = data.Boolean(boolean.group())
            index = len(boolean.group())
        # Handles parenthesized expressions
        elif input_string[0] == '(':
            parencount = index = 1
            while parencount > 0:
                if input_string[index] == '(': parencount += 1
                if input_string[index] == ')': parencount -= 1
                index += 1
            token = input_string[:index]
        # Should not reach this case
        else:
            raise exception.ParseError(input_string)

        # Append the correct string to parse later
        if quote:
            result.append("(quote {0})".format(input_string[:index]))
        elif not token is None:
            result.append(token)
        input_string = input_string[index:]
    return result

##########
#  REPL  #
##########
def repl(prompt = "pyscheme > "):
    while True:
        try:
            input_string = raw_input(prompt)
            check = _check_input_parens(input_string)
            while(not check == 0):
                if check == -1:
                    raise exception.MismatchedParensError(input_string)
                elif check > 0:
                    input_string += " {0}".format(raw_input(" " * (len(prompt) - 2) + "> "))
                    check = _check_input_parens(input_string)
                    continue
            for element in reversed(make_list(input_string)):
                util.EvalStack().push(util.EvalCall(element, glob, None, 0))
                while not util.EvalStack().isEmpty():
                    util.EvalStack().do_useful()
        except Exception as e:
            if debug:
                traceback.print_exc(file=sys.stdout)
            else:
                print "***Error:"
                print "   {0}".format(e.msg)
                continue

def _check_input_parens(input_string):
    # Returns
    #  * -1 if invalid parens
    #  * number of right parens minus number of left parens otherwise
    parencount = 0
    for char in input_string:
        if char == "(":
            parencount += 1
        elif char == ")":
            parencount -= 1
        if parencount < 0:
            return parencount
    return parencount

if __name__ == "__main__":
    debug = len(sys.argv) >= 2 and sys.argv[1] == "debug"
    util.EvalStack()._clear_stack()
    repl()
