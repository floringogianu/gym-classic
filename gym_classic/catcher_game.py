from .common import BaseGame
from .common import Canvas
from .common import RGBRender
from .catcher import Ball
from .catcher import Tray


class Catcher(BaseGame):
    def __init__(self, level=0, width=24, height=24, variable_length=False,
                 seed=42, show_screen=False):
        BaseGame.__init__(self, seed, show_screen)

        self.level = level
        self.width = width
        self.height = height
        self.variable_length = variable_length
        self.actions = (-1, 0, 1)

        self.positive_reward = 1
        self.negative_reward = 0

        self._init()


    def _init(self):
        self.canvas = Canvas(self.width, self.height)
        self.tray = Tray(self.canvas.bounds)
        self.ball = Ball(self.canvas.bounds, self.level, self.variable_length,
                         self.rng)

        if hasattr(self, "render_engine") and self.show_screen:
            self.render_engine.win.destroy()

        self.render_engine = RGBRender('Catcher', self.canvas,
                                       [self.ball, self.tray],
                                       self.show_screen)

    def reset(self):
        self.tray.reset_position()
        self.ball.reset_position()
        self.render_engine.update()

        return self.get_screen(), self.is_terminal(), self.get_reward()

    def display(self):
        if self.show_screen:
            self.render_engine.render()

    def step(self, action):
        self.ball.move_ball()
        self.tray.move_tray(self.actions[action])
        self.render_engine.update()

        return self.get_screen(), self.is_terminal(), self.get_reward()

    def get_reward(self):
        _, b_x = self.ball.position
        _, t_x = self.tray.position

        if not self.is_terminal():
            return 0

        if b_x < t_x.start or b_x > (t_x.stop-1):
            return self.negative_reward

        return self.positive_reward

    def is_terminal(self):
        b_y, _ = self.ball.position
        t_y, _ = self.tray.position

        return True if b_y == t_y else False
