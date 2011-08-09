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
import ConfigParser

import env
import data
import util
import exception
import copy



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

######################
#  Global variables  #
######################

glob = env.GlobalEnv()

glob.new_var('nil', data.Nil())
glob.new_var('true', data.Boolean("#t"))
glob.new_var('false', data.Boolean("#f"))

config = ConfigParser.ConfigParser()
config.read("config")
for name, value in config.items("Variables"):
    if value.lower() in ["#t", "true", "yes"]:
        glob.new_var(name, data.Boolean("#t"))
    elif value.lower() in ["#f", "false", "no"]:
        glob.new_var(name, data.Boolean("#f"))


###################
#  Special forms  #
###################

@specialform('and')
def _and(env, *args):
    for arg in args:
        if not arg.eval(env):
            return data.Bool("#f")
    return args[-1]

@specialform('or')
def _or(env, *args):
    for arg in args:
        if arg.eval(env):
            return arg
    return data.Bool("#f")

@specialform('define')
def define(env, *args):
    if len(args) == 2:
        var, body = args
        if var.isIdentifier():
            env.new_var(str(var), body.eval(env))
        elif var.isList():
            if not var == data.Nil() and var.car.isIdentifier():
                env.new_var(str(var.car), _lambda(env, var.cdr, body))
                var = var.car
            else:
                raise exception.WrongArgumentTypeError('define', 'variable or function', var)
        else:
            raise exception.WrongArgumentTypeError('define', 'variable or function', var)
    else:
        raise exception.ArgumentCountError('define', 'exactly two', len(args))

@specialform('lambda')
def _lambda(env, *args):
    if len(args) > 1:
        return data.Lambda(env, args[0], args[1:])
    else:
        raise exception.ArgumentCountError('lambda', 'two or more', len(args))

@specialform('delay')
def delay(env, *args):
    if len(args) == 1:
        return data.Promise(args[0], env)
    else:
        raise ArgumentCountError('delay', 'exactly one', len(args))

@specialform('if')
def _if(env, *args):
    if len(args) == 2:
        if args[0].eval(env):
            return args[1].eval(env)
    elif len(args) == 3:
        if args[0].eval(env):
            return args[1].eval(env)
        else:
            return args[2].eval(env)
    else:
        raise ArgumentCountError('if', 'two or three', len(args))

@specialform('let')
def let(env, *args):
    if len(args) > 1:
        bindings, body = args[0], args[1:]
        variables, values = data.Nil(), []
        if bindings.isList():
            for pair in bindings:
                if pair.isPair():
                    variables = data.ConsPair(pair.car, variables)
                    values = [pair.cdr.car] + values
                else:
                    raise WrongArgumentTypeError('let', 'pair', pair)
            return data.Lambda(env, variables, body)._apply_evaluated(map(lambda value: value.eval(env), values))
        else:
            raise WrongArgumentTypeError('let', 'list', bindings)
    else:
        raise ArgumentCountError('let', 'two or more', len(args))

@specialform('quote')
def quote(env, *args):
    if len(args) == 1:
        return args[0]
    else:
        raise ArgumentCountError('quote', 'exactly one', len(args))

@specialform('set!')
def set_bang(env, *args):
    if len(args) == 2:
        var, val = args
        if var.isIdentifier():
            env.__setitem__(str(var), val.eval(env))
        else:
            raise WrongArgumentTypeError('set!', 'variable', var)
    else:
        raise ArgumentCountError('set!', 'exactly two', len(args))

###########################
#  Arithmetic  functions  #
###########################

@primitive('exit')
def scheme_exit(*args):
    exit()

@primitive('+')
def plus(*args):
    for arg in args:
        if not arg.isNumber():
            raise exception.WrongArgumentTypeError('+', 'numerical type', arg)
    return sum(args, data.IntLiteral(0))

@primitive('-')
def minus(*args):
    if len(args) > 0:
        for arg in args:
            if not arg.isNumber():
                raise exception.WrongArgumentTypeError('-', 'numerical type', arg)
        return args[0] - sum(args[1:], data.IntLiteral(0)) if len(args) > 1 else -args[0]
    else:
        raise exception.ArgumentCountError('-', 'one or more', '0')

@primitive('*')
def multiply(*args):
    for arg in args:
        if not arg.isNumber():
            raise exception.WrongArgumentTypeError('*', 'numerical type', arg)
    return reduce(operator.mul, args)

@primitive('/')
def divide(*args):
    if len(args) > 0:
        for arg in args:
            if not arg.isNumber():
                raise exception.WrongArgumentTypeError('/', 'numerical type', arg)
        return args[0] / reduce(operator.mul, args[1:]) \
            if len(args) > 1 else data.IntLiteral(1)/args[0]
    else:
        raise exception.ArgumentCountError('/', 'one or more', '0')

@primitive('=')
def equal(*args):
    if len(args) == 0:
        raise exception.ArgumentCountError('=', 'one or more', '0')
    return data.Boolean("#t") if args.count(args[0]) == len(args) else data.Boolean("#f")


#########################
#  List/Pair Functions  #
#########################


@primitive('list')
def scheme_list(*args):
    return reduce(lambda accum, next: cons(next, accum), args[::-1], data.Nil())

@primitive('append')
def scheme_append(*args):
    for element in args[:-1]:
        if not element.isList():
            raise exception.WrongArgumentTypeError('append', 'list', element)
    if len(args) == 0:
        return data.Nil()
    elif len(args) == 1:
        return args[0]
    else:
        front = current = args[0].copy()
        for element in args[1:]:
            element = element.copy()
            while not current.cdr == data.Nil():
                current = current.cdr
            if not element.isList():
                current.cdr = data.ConsPair(element, data.Nil())
            else:
                current.cdr = element
            current = current.cdr
        return front

@primitive('append!')
def append_bang(*args):
    for element in args[:-1]:
        if not element.isList():
            raise exception.WrongArgumentTypeError('append!', 'list', element)
    if len(args) == 0:
        return data.Nil()
    elif len(args) == 1:
        return args[0]
    else:
        front = current = args[0]
        for element in args[1:]:
            while not current.cdr == data.Nil():
                current = current.cdr
            if not element.isList():
                current.cdr = data.ConsPair(element, data.Nil())
            else:
                current.cdr = element
            current = current.cdr

@primitive('cons')
def cons(*args):
    if len(args) == 2:
        return data.ConsPair(args[0], args[1])
    else:
        raise exception.ArgumentCountError('cons', 'exactly two', len(args))        

@primitive('car')
def car(*args):
    if len(args) == 1:
        return args[0].car
    else:
        raise exception.ArgumentCountError('car', 'exactly one', len(args))

@primitive('cdr')
def cdr(*args):
    if len(Args) == 1:
        return args[0].cdr
    else:
        raise exception.ArgumentCountError('cdr', 'exactly one', len(args))

@primitive('caar')
def caar(*args):
    if len(args) == 1:
        if args[0].isPair() and args[0].car.isPair():
            return args[0].car.car
        else:
            raise exception.WrongArgumentTypeError('caar', 'list', args[0])
    else:
        raise exception.ArgumentCountError('caar', 'exactly one', len(args))

@primitive('cadr')
def caar(pair):
    if len(args) == 1:
        if args[0].isPair() and args[0].cdr.isPair():
            return pair.cdr.car
        else:
            raise exception.WrongArgumentTypeError('cadr', 'list', args[0])
    else:
        raise exception.ArgumentCountError('cadr', 'exactly one', len(args))
### TODO ###
@primitive('cdar')
def caar(pair):
    if len(args) != 1:
        raise exception.ArgumentCountError('cdar', 'exactly one', len(args))
    if not args[0].isPair() or not args[0].car.isPair():
        raise exception.WrongArgumentTypeError('cdar', 'list', args[0])
    return pair.car.cdr

@primitive('cddr')
def caar(pair):
    if len(args) != 1:
        raise exception.ArgumentCountError('cddr', 'exactly one', len(args))
    if not args[0].isPair() or not args[0].cdr.isPair():
        raise exception.WrongArgumentTypeError('cddr', 'list', args[0])
    return pair.cdr.cdr

@primitive('set-car!')
def set_car_bang(*args):
    if not len(args) == 2:
        raise exception.ArgumentCountError('set-car!', 'exactly two', len(args))
    cons_pair, new_car = args[0], args[1]
    if not cons_pair.isPair():
        raise exception.WrongArgumentTypeError('set-car!', 'pair', cons_pair)
    cons_pair.car = new_car

@primitive('set-cdr!')
def set_cdr_bang(*args):
    if not len(args) == 2:
        raise exception.ArgumentCountError('set-cdr!', 'exactly two', len(args))
    cons_pair, new_cdr = args[0], args[1]
    if not cons_pair.isPair():
        raise exception.WrongArgumentTypeError('set-cdr!', 'pair', cons_pair)
    cons_pair.cdr = new_cdr

######################
#  Vector Functions  #
######################

@primitive('vector')
def vector(*args):
    return data.Vector(*args)

@primitive('make-vector')
def make_vector(*args):
    if len(args) == 1:
        if not args[0].isNumber():
            raise exception.WrongArgumentTypeError('make-vector', 'numerical type', args[0])
        else:
            arglist = [None] * args[0].val
            return data.Vector(*arglist)
    elif len(args) == 2:
        if not args[0].isNumber():
            raise exception.WrongArgumentTypeError('make-vector', 'numerical type', args[0])
        else:
            arglist = [args[1]] * args[0].val
            return data.Vector(*arglist)
    else:
        raise exception.ArgumentCountError('make-vector', 'one or two', len(args))

@primitive('vector-ref')
def vector_ref(*args):
    if len(args) != 2:
        raise exception.ArgumentCountError('vector-ref', 'exactly two', len(args))
    elif not args[0].isVector():
        raise exception.WrongArgumentTypeError('vector-ref', 'vector', args[0])
    elif not args[1].isNumber():
        raise exception.WrongArgumentTypeError('vector-ref', 'numerical type', args[1])
    else:
        return args[0].values.get(args[1].val)

@primitive('vector-set!')
def vector_set_bang(*args):
    if len(args) != 3:
        raise exception.ArgumentCountError('vector-set!', 'exactly three', len(args))
    else:
        vector, index, value = args
    if not vector.isVector():
        raise exception.WrongArgumentTypeError('vector-set!', 'vector', vector)
    elif not index.isNumber():
        raise exception.WrongArgumentTypeError('vector-set!', 'numerical type', index)
    else:
        vector.set(index.val, value)

#############
#  Streams  #
#############

@primitive('force')
def force(prom):
    if prom.forced:
        return prom.val
    else:
        prom.val = prom.expr.eval(prom.env)
        prom.forced = True
        return prom.val

@primitive('cons-stream')
def cons_stream(car, cdr):
    return ConsPair(car, data.Promise(cdr, env))

@primitive('stream-car')
def stream_car(stream):
    return stream.car

@primitive('stream-cdr')
def stream_cdr(stream):
    return force(stream.cdr)
