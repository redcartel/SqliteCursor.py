""" Singleton base class implementing the design pattern """


class Singleton:
    """ Singleton class """
    _instances = {}

    def __new__(cls, *args, **kwargs):
        """ Grab the existing instance of the class if it exists, otherwise
        create a new object. """
        if cls not in Singleton._instances:
            obj = object.__new__(cls)
            Singleton._instances[cls] = obj
        return Singleton._instances[cls]
