import random
from .common import BaseGame
from .common import Canvas
from .sanity_checker import RGBRender


class SanityChecker(BaseGame):
    def __init__(self, level=0, width=24, height=24, seed=42,
                 internal_render=False):
        BaseGame.__init__(self, seed, internal_render)

        self.actions = (0, 1)

        self.width = width
        self.height = height
        self.step_cnt = 0
        self.max_step = 35
        self._init()

    def _init(self):
        self.step_cnt = 0
        self.canvas = Canvas(self.width, self.height)

        if hasattr(self, "render_engine") and self.internal_render:
            self.render_engine.win.destroy()
        self.render_engine = RGBRender(self.canvas, self.internal_render)

    def reset(self):
        self.step_cnt = 0
        if hasattr(self, "render_engine") and self.internal_render:
            self.render_engine.win.destroy()
        self.render_engine = RGBRender(self.canvas, self.internal_render)
        return self.get_screen(), self.is_terminal(), self.get_reward()

    def display(self):
        if self.internal_render:
            self.render_engine.render()

    def step(self, action):
        self.render_engine.update()
        self.step_cnt += 1
        return self.get_screen(), self.is_terminal(), self.get_reward()

    def get_reward(self):
        return self.step_cnt

    def is_terminal(self):
        step = self.step_cnt
        if random.randint(17, self.max_step) < step or step >= self.max_step:
            return True
        else:
            return False
