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
import re

def tokenize(s):
    return s.replace('(', ' ( ').replace(')', ' ) ').split()

def make_list(input):
    # Input: string
    tokenized = tokenize_list(input)
    expression_list = data.Nil()
    for token in reversed(tokenized):
        if isinstance(token, str):
            expression_list = data.ConsPair(make_list(token[1:-1]), expression_list)
        else:
            expression_list = data.ConsPair(token, expression_list)
    return expression_list

def tokenize_list(input_string):
    # Returns a list of tokens, leaving parenthesized expressions as is
    result = []
    while input_string:
        whitespace = re.match(r" +", input_string)
        integer    = re.match(r"\d+", input_string)
        variable   = re.match(r"[!$%&*+-./:<=>?@^_~a-zA-Z]([!$%&*+-./:<=>?@^_~a-zA-Z0-9])*", input_string)
        boolean    = re.match(r"#[tf]", input_string)
        # Removes starting whitespace
        if whitespace:
            input_string = input_string[len(whitespace.group()):]
        # Matches integers
        elif integer:
            result += [data.IntLiteral(int(integer.group()))]
            input_string = input_string[len(integer.group()):]
        # Matches variables
        elif variable:
            result += [data.Identifier(variable.group())]
            input_string = input_string[len(variable.group()):]
        # Matches booleans
        elif boolean:
            result += [data.Boolean(boolean.group())]
            input_string = input_string[len(boolean.group()):]
        # Handles parenthesized expressions
        elif input_string[0] == '(':
            parencount = index = 1
            while parencount > 0:
                if input_string[index] == '(':
                    parencount += 1
                if input_string[index] == ')':
                    parencount -= 1
                index += 1
            result += [input_string[:index]]
            input_string = input_string[index:]
            continue
        else:
            return None
    return result


# STUFF FOR TESTING, REMOVE LATER
glob = env.GlobalEnv()

#def make_ast(s):
#    tokens = tokenize(s)
#    return read(tokens)

#def read(tokens):
#    token = tokens.pop(0)
#    try:
#        num = int(token)
#        return ast.IntLiteral(num)
#    except ValueError, TypeError:
#        if token == "(":
#            token_list = []
#            while tokens[0] != ")":
#                token_list.append(read(tokens))
#            tokens.pop(0)
#            return ast.ExpList(*token_list)
#        elif token == ")":
#            raise SyntaxError("mismatched parens")
#        else:
#            return ast.Identifier(token)

def repl(prompt = "pyscheme > "):
    while True:
        input_string = raw_input(prompt)
        check = _check_input_parens(input_string)
        try:
            while(not check == 0):
                if check == -1:
                    raise Exception("Mismatched parens: {0}".format(input_string))
                elif check > 0:
                    input_string += raw_input()
                    check = _check_input_parens(input_string)
                    continue
            val = make_list(input_string)
            while not val == data.Nil():
                print val.car.eval(glob)
                val = val.cdr
        except Exception as e:
            print e.args[0]
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
    repl()
