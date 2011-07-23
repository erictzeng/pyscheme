import ast
import data
import env
import prim

def tokenize(s):
    return s.replace('(', ' ( ').replace(')', ' ) ').split()

# STUFF FOR TESTING, REMOVE LATER
glob = env.Env(None)
glob.new_var('+', prim.plus)
