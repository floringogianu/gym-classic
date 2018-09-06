import numpy as np


class Tray(object):
    def __init__(self, bounds, color=(55, 82, 159)):
        self.__color = color

        self.width = 2 if bounds[1] <= 24 else int(np.floor(bounds[1] / 8))
        self.x_bounds = (0, bounds[1])
        self.y_bounds = (bounds[0], bounds[0])  # stays at the bottom

        self.x = int(np.floor(self.x_bounds[1] / 2 - self.width))
        self.y = self.y_bounds[0]


    def move_tray(self, action):
        if action == -1:
            self.x = max(self.x - 1, 0)
        elif action == 1:
            self.x = min(self.x + 1, self.x_bounds[1] - self.width)


    def reset_position(self):
        self.x = int(np.floor((self.x_bounds[1] - self.width) / 2 - 1))
        self.y = self.y_bounds[0]


    @property
    def position(self):
        return (self.y, range(self.x, self.x+self.width+1))


    @property
    def color(self):
        return self.__color
