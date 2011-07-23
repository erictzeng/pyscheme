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
