class Callable(object):
    pass


class Primitive(Callable):
    
    def __init__(self, name, proc):
        self.name = name
        self.proc = proc

    def apply(self, args, env):
        args = [arg.eval(env) for arg in args]
        return self.proc(*args)

    def __str__(self):
        return "#[subr {0}]".format(self.name)

class ConsPair(object):
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

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
