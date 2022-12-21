import torch
import random
import numpy as np
from collections import deque
from Asteroids.game_logic import AsteroidsGame
from model import Linear_QNet, QTrainer
from utils import plot
import time

MAX_MEM = 100_000
BATCH = 1000
LR = 0.001  # Learning Rate


class Agent:
    def __init__(self) -> None:
        self.episodes = 0
        self.episilon = 0  # Exploration
        self.gamma = 0.9  # Discount
        self.memory = deque(maxlen=MAX_MEM)
        self.model = Linear_QNet(7, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        return [
            game.in_danger(),
            game.near_objects(),
            game.aiming_at_target(),
            game.distance_to_target(),
            game.distance_to_next_target(),
            game.next_target_angle(),
            game.ship_angle(),
        ]

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long(self):
        if len(self.memory) > BATCH:
            mini_sample = random.sample(self.memory, BATCH)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)

        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, old_state):
        self.episilon = 25 - self.episodes
        # [fwd,left,right,shoot]
        action = [0, 0, 0, 0]
        if random.randint(0, 200) < self.episilon:
            move = random.randint(0, 3)
            action[move] = 1
        else:
            state0 = torch.tensor(old_state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            action[move] = 1

        return action


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = AsteroidsGame()
    game.step(action=[0, 0, 0, 0])

    while agent.episodes < 50:
        old_state = agent.get_state(game)

        next_action = agent.get_action(old_state)

        reward, done, score = game.step(action=next_action)
        score = int(score)
        new_state = agent.get_state(game)

        agent.train_short(old_state, next_action, reward, new_state, done)
        agent.memorize(old_state, next_action, reward, new_state, done)

        time.sleep(1 / 60)

        if done:
            game.reset()
            agent.episodes += 1
            agent.train_long()

            if score > record:
                record = score

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.episodes
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == "__main__":
    train()
