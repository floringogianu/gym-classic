""" Kind of a Facade over each game implementation. Not sure if it is required
    nowdays.
"""
from PIL import Image

import numpy as np
import gym
from gym import spaces
from gym_classic import get_game_module


class ClassicMDP(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, **kwargs):

        game_module = get_game_module(kwargs['game_module'])
        print(f'Initialising {kwargs["game_id"]}.')

        kwargs.pop('game_module')
        kwargs.pop('game_id')

        self.game = game_module(**kwargs)

        self._action_set = self.game.get_action_set()
        self.action_space = spaces.Discrete(len(self._action_set))
        self.screen_width, self.screen_height = self.game.get_screen_dims()
        shape = (self.screen_width, self.screen_height, 3)
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=shape, dtype=np.uint8)
        self.viewer = None


    def step(self, action):
        observation, terminal, reward = self.game.step(action)
        return observation, reward, terminal, {}


    def _get_image(self):
        w, h = self.game.render_engine.width, self.game.render_engine.height
        img = self.game.render_engine.get_screen()
        img = Image.fromarray(img, 'RGB')
        img = img.resize((w, h), resample=Image.NEAREST)
        return img


    @property
    def _n_actions(self):
        return len(self._action_set)


    def reset(self):
        observation, _, _ = self.game.reset()
        return observation


    def render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return

        img = self._get_image()

        if mode == 'rgb_array':
            return img

        # TODO: replace this ImageViewer
        elif mode == 'human':
            from gym.envs.classic_control import rendering
            if self.viewer is None:
                self.viewer = rendering.SimpleImageViewer()
            self.viewer.imshow(np.array(img))


    def _seed(self, seed):
        self.game.set_seed(seed)
