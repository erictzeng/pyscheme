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

def primitive(name, type="function"):
    def decorator(arg):
        glob = env.GlobalEnv()
        if type == "function":
            obj = data.Primitive(name, arg)
        else:
            obj = arg
        glob.new_var(name, obj)
        return arg
    return decorator

@primitive('exit')
def scheme_exit(*args):
    exit()

########################################################################
## Nil

primitive('nil', "variable")(data.Nil())

########################################################################
## Primitive functions
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

## List Procedures #####################################################
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

## Vector procedures ###################################################
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
