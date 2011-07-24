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

import ast
import data
import env
import prim

def tokenize(s):
    return s.replace('(', ' ( ').replace(')', ' ) ').split()

# STUFF FOR TESTING, REMOVE LATER
glob = env.GlobalEnv()

def make_ast(s):
    tokens = tokenize(s)
    return read(tokens)

def read(tokens):
    token = tokens.pop(0)
    try:
        num = int(token)
        return ast.IntLiteral(num)
    except ValueError, TypeError:
        if token == "(":
            token_list = []
            while tokens[0] != ")":
                token_list.append(read(tokens))
            tokens.pop(0)
            return ast.ExpList(*token_list)
        elif token == ")":
            raise SyntaxError("mismatched parens")
        else:
            return ast.Identifier(token)

def repl(prompt = "pyscheme > "):
    while True:
        val = make_ast(raw_input(prompt)).eval(glob)
        print val.__repr__()

repl()
