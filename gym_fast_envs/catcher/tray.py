import numpy as np


class Tray(object):
    def __init__(self, bounds):

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

    def get_position(self):
        return (self.y, range(self.x, self.x+self.width+1))

    def reset_position(self):
        self.x = int(np.floor((self.x_bounds[1] - self.width) / 2 - 1))
        self.y = self.y_bounds[0]
