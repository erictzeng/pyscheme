def singleton(C):
    instances = {}
    def get_instance():
        if C not in instances:
            instances[C] = C()
        return instances[C]
    return get_instance

