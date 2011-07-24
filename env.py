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

class Env(dict):
    
    def __init__(self, next):
        self.next = next

    def _find_env(self, key):
        env = self
        while env is not None:
            if dict.__contains__(env, key):
                return env
            else:
                env = env.next
        raise KeyError(key)

    def __getitem__(self, key):
        env = self._find_env(key)
        return dict.__getitem__(env, key)

    def __setitem__(self, key, value):
        env = self._find_env(key)
        dict.__setitem__(env, key, value)

    def __contains__(self, key):
        env = self
        while env is not None:
            if dict.__contain__(env, key):
                return True
            else:
                env = env.next
        return False

    def new_var(self, key, value):
        dict.__setitem__(self, key, value)


@util.singleton
class GlobalEnv(Env):
    
    def __init__(self):
        Env.__init__(self, None)
