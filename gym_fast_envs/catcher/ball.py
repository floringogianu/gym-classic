import numpy as np


class Ball(object):
    def __init__(self, bounds, level, rng):
        self.rng = rng

        self.x_bounds = (0, bounds[1])
        self.y_bounds = (0, bounds[0])

        self.x = int(np.floor(self.x_bounds[1] / 2))
        self.y = 0                                  # always starts at the top

        self.level = level
        self.angle = int(self.rng.choice([-1, 1]) * np.floor(self.level / 2))
        self.att_prob = self.level/10

    def move_ball(self):
        self.y += 1
        if self.rng.uniform() < 1 - self.att_prob:
            self.x += self.angle
        else:
            # attenuate angle
            self.x += self.angle + 1 if self.angle < 0 else self.angle - 1

        if self.x >= self.x_bounds[1]:
            self.x = self.x_bounds[1]
            self.angle = -self.angle
        elif self.x < 2 and self.angle <= 0:
            self.x = 0
            self.angle = -self.angle

    def get_position(self):
        return (self.y, self.x)

    def reset_position(self):
        self.x = self.rng.choice(self.x_bounds[1])
        self.y = 0                                  # always starts at the top
