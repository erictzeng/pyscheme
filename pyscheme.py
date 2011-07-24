import ast
import data
import env
import prim

def tokenize(s):
    return s.replace('(', ' ( ').replace(')', ' ) ').split()

# STUFF FOR TESTING, REMOVE LATER
glob = env.Env(None)
glob.new_var('+', prim.plus)

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
