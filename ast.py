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
