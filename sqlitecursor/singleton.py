""" Singleton base-class """

class Singleton:
    """ Singleton class """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_singleton_instance'):
            obj = object.__new__(cls)
            cls._singleton_instance = obj
        return cls._singleton_instance
