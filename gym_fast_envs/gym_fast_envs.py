import gym
from gym import spaces
from gym_fast_envs import get_game_module


class FastEnvs(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, game_name='Catcher', display_screen=False,
                 level=2, width=24, height=24, seed=42, variable_length=False):

        game_module = get_game_module(game_name)
        if game_name is 'Catcher':
            self.game = game_module(level, width, height,
                                    variable_length=variable_length)
        else:
            self.game = game_module(level, width, height)
        print("Building %s: level=%d, size=%dpx." % (game_name, level, width))

        self._action_set = self.game.get_action_set()
        self.action_space = spaces.Discrete(len(self._action_set))
        self.screen_width, self.screen_height = self.game.get_screen_dims()
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(self.screen_width, self.screen_height, 3))
        self.viewer = None

    def _step(self, action):
        observation, terminal, reward = self.game.step(action)
        return observation, reward, terminal, {}

    def _get_image(self):
        return self.game.get_screen()

    @property
    def _n_actions(self):
        return len(self._action_set)

    def _reset(self):
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(self.screen_width, self.screen_height, 3))
        observation, _, _ = self.game.reset()
        return observation

    def _render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return
        img = self._get_image()
        if mode == 'rgb_array':
            return img
        elif mode == 'human':
            from gym.envs.classic_control import rendering
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(img)

    def _seed(self, seed):
        self.game.set_seed(seed)
