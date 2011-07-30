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

import locale
locale.setlocale(locale.LC_ALL, "")

import util
import env
import exception
        
class SchemeDatum(object):
    def eval(self, env):
        raise NotImplementedError
    
    def __nonZero__(self):
        return True

    def isPair(self):
        return False

    def isList(self):
        return False

    def isNumber(self):
        return False

    def copy(self):
        return self

    def isVector(self):
        return False

    def isIdentifier(self):
        return False

class Callable(SchemeDatum):
    def apply(self, env, args):
        raise NotImplementedError


class SpecialForm(Callable):   
    def __init__(self, name, proc):
        self.name = name
        self.proc = proc
        
    def apply(self, env, args):
        return self.proc(env, *args)


class Procedure(Callable):
    def apply(self, env, args):
        args = [arg.eval(env) for arg in args]
        return self._apply_evaluated(args)
    
    def _apply_evaluated(self, args):
        raise NotImplementedError


class Primitive(Procedure):
    def __init__(self, name, proc):
        self.name = name
        self.proc = proc

    def _apply_evaluated(self, args):
        return self.proc(*args)

    def __str__(self):
        return "#[subr {0}]".format(self.name)


class Lambda(Procedure):
    def __init__(self, env, params, body):
        self.env = env
        self.body = body
        self.raw_params = params
        self.params = []
        self.rest_params = False

        while params.isPair():
            self.params.append(params.car)
            params = params.cdr
        if not params == Nil():
            self.params.append(params)
            self.rest_params = True

    def _apply_evaluated(self, args):
        new_env = env.Env(self.env)
        if not self.rest_params:
            if len(args) != len(self.params):
                raise exception.ArgumentCountError('lambda', len(self.params), len(args))
            else:
                new_env.update(zip(map(str, self.params), args))
        else:
            if len(args) < len(self.params) - 1:
                raise exception.ArgumentCountError('lambda', '{0} or more'.format(len(self.params) - 1), len(args))
            else:
                new_env.update(zip(map(str, self.params[:-1]), args[:len(self.params)-1]))
                new_env.update([(str(self.params[-1]), reduce(lambda accum, next: ConsPair(next, accum), args[len(self.params)-1:], Nil()))])
        for expr in self.body[:-1]:
            expr.eval(new_env)
        return self.body[-1].eval(new_env)

    def __repr__(self):
        return "[Lambda {0}]".format(self.raw_params)
                

class ConsPair(SchemeDatum):
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __repr__(self):
        return str(self)

    def __str__(self):
        cdr = str(self.cdr)
        if cdr[0] == "(" and cdr[-1] == ")":
            cdr = " {0}".format(cdr[1:-1])
        else:
            cdr = " . {0}".format(cdr)
        return "({0}{1})".format(self.car, cdr.rstrip(" "))

    def eval(self, env):
        oper = self.car.eval(env)
        args = []
        current = self.cdr
        while not current == Nil():
            args.append(current.car)
            current = current.cdr
        return oper.apply(env, args)

    def __iter__(self):
        def iterator():
            current = self
            while not current == Nil():
                yield current.car
                current = current.cdr
        return iterator()

    def isPair(self):
        return True

    def isList(self):
        return self.cdr.isList()

    def copy(self):
        return ConsPair(self.car.copy(), self.cdr.copy())

@util.singleton
class Nil(SchemeDatum):
    def __repr__(self):
        return "()"

    def __iter__(self):
        def generator():
            return
            yield
        return generator()

    def isList(self):
        return True
    
    def eval(self, env):
        return self

class Vector(SchemeDatum):
    def __init__(self, *args):
        self.values = list(args)
        self.length = len(args)

    def get(self, index):
        if index >= self.length:
            raise IndexOutOfBoundsError(self, index, self.length)
    
    def set(self, index, value):
        if index >= self.length:
            raise IndexOutOfBoundsError(self, index, self.length)
        else:
            self.values[index] = value

    def __str__(self):
        display = ""
        for value in self.values:
            display += str(value) + " " if value else "#[unbound] "
        return "#({0})".format(display.rstrip(" "))

    def isVector(self):
        return True
        

class IntLiteral(SchemeDatum):
    def __init__(self, val):
        self.val = val

    def eval(self, env):
        return self

    def __add__(self, num):
        return IntLiteral(self.val + num.val)

    def __sub__(self, num):
        return IntLiteral(self.val - num.val)

    def __mul__(self, num):
        return IntLiteral(self.val * num.val)
    
    def __div__(self, num):
        return IntLiteral(self.val / num.val)

    def __neg__(self):
        return IntLiteral(-self.val)

    def __str__(self):
        if env.GlobalEnv()['pretty-print']:
            return locale.format('%d', self.val, True)
        else:
            return str(self.val)

    def __eq__(self, num):
        return isinstance(num, IntLiteral) and self.val == num.val

    def __repr__(self):
        return "[IntLiteral {0}]".format(self.val)

    def isNumber(self):
        return True

class Identifier(SchemeDatum):
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        return env[self.name]

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "[Identifier {0}]".format(self.name)

    def isIdentifier(self):
        return True

class Boolean(SchemeDatum):
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        return self

    def __str__(self):
        return self.value

    def __repr__(self):
        return "[Boolean {0}]".format(self.value)

    def __nonzero__(self):
        return self.value == '#t'


class Promise(SchemeDatum):
    def __init__(self, expr, env):
        self.expr = expr
        self.env = env
        self.forced = False
        self.val = None
        
    def eval(self, env):
        return self
