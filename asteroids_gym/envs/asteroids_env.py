import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame

from Asteroids.game_logic import AsteroidsGame as Ast


class AsteroidsEnv(gym.Env):
    def __init__(self, render_mode="human"):
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window_size = (800, 600)

        self.action_space = spaces.Discrete(2, start=0)
        self.observation_space = spaces.Discrete(49, start=0)

        self.window = None
        self.clock = None
        self.game = Ast()

    def _get_obs(self):
        obs = {}
        return obs

    def step(self, action):

        obs = self._get_obs()

        terminated = self.game.game_over

        reward = 1

        info = {"score": self.game.score}

        return obs, reward, terminated, False, info

    def reset(self, seed=None):
        super().reset(seed=seed)

        self.game.reset()

        obs = self._get_obs()
        info = {"score": self.game.score}

        return obs, info

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
