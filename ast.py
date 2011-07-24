class IntLiteral(object):
    
    def __init__(self, val):
        self.val = val

    def eval(self, env):
        return self.val

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return "[IntLiteral {0}]".format(self.val)


class Identifier(object):
    
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        return env[self.name]

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "[Identifier {0}]".format(self.name)


class ExpList(object):
    
    def __init__(self, *items):
        self.items = items
    
    def eval(self, env):
        oper = self.items[0].eval(env)
        return oper.apply(self.items[1:], env)
        
    def __str__(self):
        items_str = ' '.join(str(node) for node in self.items)
        return "({0})".format(items_str)

    def __repr__(self):
        items_str = ' '.join(str(node) for node in self.items)
        return "[ExpList {0}]".format(items_str)


class Boolean(object):
    
    def __init__(self, value):
        self.val = value
        
    def eval(self, env):
        return self.val

    def __str__(self):
        return "({0})".format(self.val)

    def __repr__(self):
        return "[Boolean {0}]".format(self.val)
