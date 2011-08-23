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

def singleton(C):
    instances = {}
    def get_instance():
        if C not in instances:
            instances[C] = C()
        return instances[C]
    return get_instance

@singleton
class EvalStack:
    def __init__(self):
        self.stack = []

    def push(self, element):
        self.stack.append(element)

    def pop(self):
        return self.stack.pop()

    def do_useful(self):
        current = self.stack[-1]
        value = current.eval()
        if not value is None:
            if current.parent:
                current.parent.set_args(value, current.position)
            else:
                print value
            self.pop()
        else:
            return

    def print_stack_trace(self):
        print "Stack trace: (Most recent call first)"
        print "-------------------------------------"
        index = 0
        if self.isEmpty():
            print "No elements on stack"
        else:
            current = self.stack[-1]
            while not current is None:
                print "{0}\t{1}".format(index, current.datum)
                current = current.parent
                index += 1

    def clear_stack(self):
        self.stack = []

    def isEmpty(self):
        return not self.stack

class EvalCall:
    def __init__(self, datum, env, parent=None, position=0):
        self.datum = datum
        self.env = env
        self.parent = parent
        self.position = position

        self.value    = None
        self.elements = None

        if self.datum.isList() and self.datum.isPair():
            self.elements = [EvalElement(element, None, position) for position, element in enumerate(self.datum)]
        else:
            self.value = self.datum.eval(self)

    def eval(self):
        if not self.value is None:
            return self.value
        else:
            return self.datum.eval(self)
        
    def set_args(self, value, position):
        if position < 0:
            self.value = value
        else:
            self.elements[position].value = value
    
    def push_arg(self, position):
        EvalStack().push(EvalCall(self.elements[position].datum, self.env, self, position))

class EvalElement:
    def __init__(self, datum, value, position):
        self.datum    = datum
        self.value    = value
        self.position = position
