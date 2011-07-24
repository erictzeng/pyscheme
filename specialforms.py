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

def set_bang(var, val, env):
    env.__setitem__(var.eval(env), val.eval(env))

def let(var_val_pairs, body, env):
    vars_and_vals = zip(var_val_pairs.items)
    vars = var.name for var in vars_and_vals[0]
    vals = val.eval(env) for val in vars_and_vals[1]
    new_lambda = Lambda(vars, body, env)
    new_lambda._apply_evaluated(vals)

def define():
    pass

def _and(*args, env):
    for arg in args:
        if arg.eval(env) == False:
            return ast.Bool("#f")
    return args[-1]

def _or(*args, env):
    for arg in args:
        if arg.eval(env) == True:
            return ast.Bool("#t")
    return ast.Bool("#f")

def _if(condition, true_case, false_case, env):
    if condition.eval(env).eval(env) != "#f":
        return true_case.eval(env)
    elif false_case is None:
        return None()
    else:
        return false_case.eval(env)
