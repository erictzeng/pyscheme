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
