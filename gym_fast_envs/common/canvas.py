class Canvas(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_bounds(self):
        """ Return bounds of canvas in numpy row-major order.
        """
        return (self.height-1, self.width-1)

    def get_size(self):
        """ Return size of canvas in numpy row-major order.
        """
        return (self.height, self.width)
