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

def make_global_dec(cls):
    def decorator(name):
        def add_to_global(py_proc):
            glob = env.GlobalEnv()
            scheme_proc = cls(name, py_proc)
            glob.new_var(name, scheme_proc)
            return py_proc
        return add_to_global
    return decorator

primitive = make_global_dec(data.Primitive)
specialform = make_global_dec(data.SpecialForm)

# Global variables

glob = env.GlobalEnv()

glob.new_var('nil', data.Nil())
glob.new_var('true', data.Boolean("#t"))
glob.new_var('false', data.Boolean("#f"))


# Special forms

@specialform('set!')
def set_bang(env, var, val):
    env.__setitem__(str(var), val.eval(env))

@specialform('lambda')
def _lambda(env, params, *body):
    if len(body) == 0:
        raise Exception("lambda: bad syntax")
    params = [str(param) for param in params]
    return data.Lambda(params, body, env)

@specialform('let')
def let(env, var_val_pairs, body):
    vars_and_vals = zip(var_val_pairs.items)
    let_vars = [var.name for var in vars_and_vals[0]]
    vals = [val.eval(env) for val in vars_and_vals[1]]
    new_lambda = Lambda(let_vars, body, env)
    new_lambda._apply_evaluated(vals)

@specialform('define')
def define(env, var, body):
    env.new_var(str(var), body.eval(env))
    return var

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

@specialform('quote')
def quote(env, arg):
    return arg

@specialform('delay')
def delay(env, arg):
    return data.Promise(arg, env)


# Primitive functions

@primitive('exit')
def scheme_exit(*args):
    exit()

@primitive('+')
def plus(*args):
    return sum(args, data.IntLiteral(0))

@primitive('-')
def minus(*args):
    return args[0] - sum(args[1:], data.IntLiteral(0)) if len(args) > 1 else -args[0]

@primitive('*')
def multiply(*args):
    return reduce(operator.mul, args)

@primitive('/')
def divide(*args):
    return args[0] / reduce(operator.mul, args[1:]) \
        if len(args) > 1 else data.IntLiteral(1)/args[0]

@primitive('=')
def equal(*args):
    if len(args) == 0:
        raise Exception("too few parameters")
    return data.Boolean("#t") if args.count(args[0]) == len(args) else data.Boolean("#f")

@primitive('set-car!')
def set_car_bang(cons_pair, new_car):
    cons_pair.car = new_car

@primitive('set-cdr!')
def set_cdr_bang(cons_pair, new_cdr):
    cons_pair.cdr = new_cdr

@primitive('list')
def scheme_list(*args):
    if len(args) == 0:
        return data.Nil()
    else:
        return reduce(lambda accum, next: cons(next, accum),
                      args[::-1],
                      data.Nil())

@primitive('append!')
def append_bang(list1, list2):
    lastPair = None
    currPair = list1
    while True:
        if currPair.cdr == Nil():
            lastPair = currPair
        else:
            currPair = currPair.cdr
    lastPair.cdr = list2

@primitive('append')
def scheme_append(list1, list2):
    new_list = copy.deepycopy(list1)
    append_bang(new_list, list2)
    return new_list

@primitive('cons')
def cons(car, cdr):
    return data.ConsPair(car, cdr)

@primitive('car')
def car(pair): return pair.car

@primitive('cdr')
def cdr(pair): return pair.cdr

@primitive('caar')
def caar(pair): return pair.car.car

@primitive('cadr')
def caar(pair): return pair.cdr.car

@primitive('cdar')
def caar(pair): return pair.car.cdr

@primitive('cddr')
def caar(pair): return pair.cdr.cdr

@primitive('vector-ref')
def vector_ref(vec, index):
    return vec.vector_ref(index)

@primitive('vector-set!')
def vector_set_bang(vec, index, new_val):
    vec.vector_set_bang(index, new_val)

@primitive('vector')
def vector(*args):
    vec = Vector()
    vec.init_with_vals(*args)
    return vec

@primitive('make-vector')
def make_vector(*args):
    vec = Vector()
    if len(args) == 1:  # i.e. (make-vector 3)
        vec.init_with_length(args[0])
        return vec
    elif len(args) == 2:  # i.e. (make-vector 3 'hi)
        vec.init_with_initial_val(args[0], args[1])
        return vec
    else:
        raise Exception("incorrect number of arguments")

@primitive('force')
def force(prom):
    if prom.forced:
        return prom.val
    else:
        prom.val = prom.expr.eval(prom.env)
        prom.forced = True
        return prom.val
