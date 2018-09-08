""" Blind Cliff Walk """

from gym_fast_envs.common import BaseGame
from gym_fast_envs.common import Canvas
from gym_fast_envs.common import Entity
from gym_fast_envs.common import RGBRender
from gym_fast_envs.common import SymbolicRender


class Agent(Entity):
    """ The hero in our story. In this case a pixel moving mostly to the right.
    """

    def __init__(self, bounds, size=(1, 1), initial_xy=(0, 0),
                 color=(231, 56, 133), code=1):
        Entity.__init__(self, bounds, size, initial_xy, color, code=code)


    def update(self, action):
        """ Updates the agent's position."""
        if action == -1 or self.position == self.bounds:
            self.position = (0, 0)
        else:
            self.position = (0, self.position[1] + action)

    def reset(self):
        """ Reset the agent to its initial position."""
        self.position = (0, 0)


class BlindCliffWalk(BaseGame):
    """ Blind Cliff Walking, as described in Prioritized Experience Replay.

        In BCW there are two available actions in each state:
            - `good`, allows the user to transition towards the goal
            - `wrong`, moves the agent to s0 and terminates the game

        There is only one reward of 1 when transitioning from the last state to
        the first. All other rewards are 0 everywhere.

        The `good` and `wrong` actions have their semantics switched
        alternatively in each other state so that a linear estimator cannot
        learn to generalize over actions.

        Full details in the paper: https://arxiv.org/pdf/1511.05952.pdf


        # self.s0_code = (55, 82, 159)
        # self.s0_code = (107, 113, 126)
        # self.sN_code = (175, 213, 170)
    """

    def __init__(self, N=8, seed=42, show_screen=False, symbolic_state=True):
        BaseGame.__init__(self, seed, show_screen)

        self.symbolic_state = symbolic_state

        self.canvas = canvas = Canvas(width=N, height=1)
        self.agent = agent = Agent(self.canvas.bounds)

        self.render_engine = RGBRender('BlindCliffWalk', self.canvas,
                                       [self.agent], self.show_screen)
        if self.symbolic_state:
            self.symbolic_render_engine = SymbolicRender(canvas, [agent])

        self._is_blind = True
        self._last_action = False
        self._step_cnt = 0

        self.actions = {0: -1, 1: 1}
        self._swapped_actions = {0: 1, 1: -1}

        self._init()


    def _init(self):
        if hasattr(self, "render_engine") and self.show_screen:
            self.render_engine.win.destroy()
        self.render_engine = RGBRender('BlindCliffWalk', self.canvas,
                                       [self.agent], self.show_screen)

    def reset(self):
        self._last_action = False
        self._step_cnt = 0
        self.agent.reset()
        self.render_engine.update()
        if self.symbolic_state:
            self.symbolic_render_engine.update()

        return self.get_screen(), self.is_terminal(), self.get_reward()


    def _swapped(self, action):
        """ Swappes `good` and `bad` actions every other state """
        if self._step_cnt % 2 == 0:
            return self._swapped_actions[action]
        return self.actions[action]


    def step(self, action):
        """ Increments the state of the world.
            Args:
                action (int): Input in the [0, len(self.actions)] range.

            If `is_blind` it swappes `good` with `bad` actions every other
            state so that a linear estimator can't generalize over actions.
        """
        act = self._swapped(action) if self._is_blind else self.actions[action]
        self._last_action = True if act == 1 else False

        self.agent.update(act)
        self.render_engine.update()
        if self.symbolic_state:
            self.symbolic_render_engine.update()

        self._step_cnt += 1

        return self.get_screen(), self.is_terminal(), self.get_reward()


    def is_terminal(self):
        return True if self.agent.position == (0, 0) else False


    def get_reward(self):
        return 1 if self.is_terminal() and self._last_action else 0


    def get_screen(self):
        if self.symbolic_state:
            return self.symbolic_render_engine.get_screen()
        return self.render_engine.get_screen()


    def display(self):
        """ Uses the interna rendering engine to open a window and display
            the current frame.
        """
        if self.show_screen:
            self.render_engine.render()
