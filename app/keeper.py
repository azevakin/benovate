class Keeper(object):
    _instances = []

    def __init__(self):
        self._instances.append(self)

    @classmethod
    def list_instances(cls):
        return cls._instances
