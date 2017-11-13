import time
from .common import BaseGame
from .common import Canvas
from .catcher import RGBRender
from .catcher import Ball
from .catcher import Tray


class Catcher(BaseGame):
    def __init__(self, level=0, width=24, height=24, seed=42,
                 internal_render=False):
        BaseGame.__init__(self, seed, internal_render)

        self.level = level
        self.width = width
        self.height = height
        self.actions = (-1, 0, 1)

        self.positive_reward = 1
        self.negative_reward = 0
        self._init()

    def _init(self):
        self.canvas = Canvas(self.width, self.height)
        self.tray = Tray(self.canvas.get_bounds())
        self.ball = Ball(self.canvas.get_bounds(), self.level, self.rng)

        if hasattr(self, "render_engine") and self.internal_render:
            self.render_engine.win.destroy()
        self.render_engine = RGBRender(self.canvas, self.ball, self.tray,
                                       self.internal_render)

        # self.render_engine=AsciiArtRender(self.canvas,self.ball,self.tray)

    def reset(self):
        self.tray.reset_position()
        self.ball.reset_position()

        return self.get_screen(), self.is_terminal(), self.get_reward()

    def display(self):
        if self.internal_render:
            self.render_engine.render()

    def step(self, action):
        self.ball.move_ball()
        self.tray.move_tray(self.actions[action])
        self.render_engine.update()

        return self.get_screen(), self.is_terminal(), self.get_reward()

    def get_reward(self):
        b_y, b_x = self.ball.get_position()
        t_y, t_x = self.tray.get_position()

        if not self.is_terminal():
            return 0
        else:
            if b_x < t_x.start or b_x > (t_x.stop-1):
                return self.negative_reward
            else:
                return self.positive_reward

    def is_terminal(self):
        b_y, b_x = self.ball.get_position()
        t_y, t_x = self.tray.get_position()

        return True if b_y == t_y else False
