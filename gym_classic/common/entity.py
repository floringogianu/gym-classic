""" Entity """


class Entity:
    """ The base class for all the game entities besides `Canvas`
    """
    def __init__(self, bounds, size, position, color, code):
        self.__bounds = bounds
        self.__size = size
        self.__color = color
        self.__position = position
        self.__code = code

    @property
    def bounds(self):
        return self.__bounds

    @property
    def size(self):
        return self.__size

    @property
    def color(self):
        return self.__color

    @property
    def code(self):
        return self.__code

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
