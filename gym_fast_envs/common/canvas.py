""" Canvas object
"""


class Canvas:
    """ The background on which all the other objects are painted.
    """

    def __init__(self, width, height, color=(242, 242, 242), code=0):
        self.__width = width
        self.__height = height
        self.__color = color
        self.__code = code

    @property
    def bounds(self):
        """ Return bounds of canvas in numpy row-major order.
        """
        return (self.__height-1, self.__width-1)

    @property
    def size(self):
        """ Return size of canvas in numpy row-major order.
        """
        return (self.__height, self.__width)

    @property
    def color(self):
        """ Return the color of the canvas.
        """
        return self.__color

    @property
    def code(self):
        """ Return the symbolic encoding of the canvas.
        """
        return self.__code
