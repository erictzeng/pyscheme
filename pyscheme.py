import ast
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

def tokenize_list(input):
    # Returns a list of tokens, leaving parenthesized expressions as is
    result = []
    while input:
        whitespace = re.match(r" +", input)
        integer = re.match(r"\d+", input)
        variable = re.match(r"[!$%&*+-./:<=>?@^_~a-zA-Z]([!$%&*+-./:<=>?@^_~a-zA-Z0-9])*", input)
        # Removes starting whitespace
        if whitespace:
            input = input[len(whitespace.group()):]
            continue
        # Matches integers
        elif integer:
            result += [ast.IntLiteral(int(integer.group()))]
            input = input[len(integer.group()):]
            continue
        # Matches variables
        elif variable:
            result += [ast.Identifier(variable.group())]
            input = input[len(variable.group()):]
        # Handles parenthesized expressions
        elif input[0] == '(':
            parencount = index = 1
            while parencount > 0:
                if input[index] == '(':
                    parencount += 1
                if input[index] == ')':
                    parencount -= 1
                index += 1
            result += [input[:index]]
            input = input[index:]
            continue
        else:
            return None
    return result


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
    while not val == "(exit)":
        val = make_ast(raw_input(prompt)).eval(glob)
        print val.__repr__()
repl()
