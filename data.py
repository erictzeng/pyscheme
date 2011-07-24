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

import util

class Callable(object):

    def apply(self, args, env):
        raise NotImplementedError


class SpecialForm(Callable):
    
    def __init__(self, name, proc):
        self.name = name
        self.proc = proc
        
    def apply(self, args, env):
        return self.proc(*args)


class Procedure(Callable):
    
    def apply(self, args, env):
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
    
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

    def _apply_evaluated(self, args):
        if len(args) != len(self.params):
            raise TypeError # TODO: fix
        env = env.Env(self.env)
        env.update(zip(self.params, args))
        self.body.eval(env)


class ConsPair(object):

    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __repr_no_parens__(self):
        if self.cdr == None:
            return repr(self.car)
        elif isinstance(self.cdr, ConsPair):
            return '%s %s' % (repr(self.car), self.cdr.__repr_no_parens__())
        else:
            return '%s . %s' % (repr(self.car), repr(self.cdr))

    def __repr__(self):
        if self.cdr == None:
            return repr(self.car)
        elif isinstance(self.cdr, ConsPair):
            return '(%s %s)' % (repr(self.car), self.cdr.__repr_no_parens__())
        else:
            return '(%s . %s)' % (repr(self.car), repr(self.cdr))

    def __str__(self):
        cdr = str(self.cdr)
        if cdr[0] == "(" and cdr[-1] == ")":
            cdr = " {0}".format(cdr[1:-1])
        else:
            cdr = " . {0}".format(cdr)
        return "({0}{1})".format(self.car, cdr.rstrip(" "))
    
    @staticmethod
    def list(*args):
        list = Nil()
        for item in reversed(args):
            list = ConsPair(Nil(), list)
            list.car = item
        return list
     
@util.singleton
class Nil(object):
    def __str__(self):
        return "()"

class Vector(object):
    
    def __init__(self):
        pass

    def init_with_length(self, length):
        self.LENGTH = length

    def init_with_vals(self, *args):
        self.values = args
        self.LENGTH = len(args)

    def init_with_initial_val(self, length, init_val):
        self.values = [init_val]*length
        self.LENGTH = length

    def vector_ref(self, index):
        if (index < 0) or (index >= self.LENGTH):
            raise IndexError("index out of bounds")
        else:
            return self.values[index]
    
    def vector_set_bang(self, index, new_val):
        if (index < 0) or (index >= self.LENGTH):
            raise IndexError("index out of bounds")
        else:
            self[index] = new_val
