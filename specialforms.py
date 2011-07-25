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
import operator

import env
import data
import util

def specialform(name, type="function"):
    def decorator(arg):
        glob = env.GlobalEnv()
        obj = data.SpecialForm(name, arg)
        glob.new_var(name, obj)
        return arg
    return decorator


@specialform('set!')
def set_bang(env, var, val):
    env.__setitem__(var.eval(env), val.eval(env))

@specialform('let')
def let(env, var_val_pairs, body):
    vars_and_vals = zip(var_val_pairs.items)
    let_vars = [var.name for var in vars_and_vals[0]]
    vals = [val.eval(env) for val in vars_and_vals[1]]
    new_lambda = Lambda(let_vars, body, env)
    new_lambda._apply_evaluated(vals)

@specialform('define')
def define(env):
    pass

@specialform('and')
def _and(env, *args):
    args = map(lambda arg: arg.eval(env), args)
    return reduce(lambda x, y: x and y, args)

@specialform('or')
def _or(env, *args):
    args = map(lambda arg: arg.eval(env), args)
    return reduce(lambda x, y: x or y, args)

@specialform('if')
def _if(env, condition, true_case, false_case):
    if condition.eval(env):
        return true_case.eval(env)
#    elif false_case == None:
#        return None
    else:
        return false_case.eval(env)
