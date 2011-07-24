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
