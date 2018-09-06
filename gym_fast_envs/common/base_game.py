from numpy.random import RandomState


class BaseGame(object):
    """ Base Game

        Part interface, part object, can't decide.
    """

    def __init__(self, seed, show_screen):
        self.seed = seed
        self.show_screen = show_screen
        self.rng = RandomState(self.seed)

    def set_seed(self, seed):
        self.seed = seed
        self.rng = RandomState(self.seed)
        # reset the state of the game
        self._init()

    def reset(self):
        raise NotImplemented

    def get_action_set(self):
        return self.actions

    def get_screen_dims(self):
        return self.canvas.size

    def get_screen(self):
        return self.render_engine.get_screen()

    def step(self, action):
        raise NotImplemented

    def get_reward(self):
        raise NotImplemented

    def is_terminal(self):
        raise NotImplemented
