import torch
import random
import numpy as np
from collections import deque
from Asteroids.game_logic import AsteroidsGame
from model import Linear_QNet, QTrainer
from utils import plot
import time
import os

MAX_MEM = 100_000_000
BATCH = 1000
LR = 0.01  # Learning Rate
EPSILON = 200
EPISODES = 200

file_name = "model1.pth"
file_path = f"models/{file_name}"


class Agent:
    def __init__(self) -> None:
        self.episodes = 0
        self.episilon = 0  # Exploration
        self.gamma = 0.9  # Discount
        self.memory = deque(maxlen=MAX_MEM)
        self.model = Linear_QNet(19, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.load_model()

    def get_state(self, game):
        return game.get_state()

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
        self.episilon = (EPSILON * 0.6) - self.episodes
        # [fwd,left,right,shoot]
        action = [0, 0, 0, 0]
        if random.randint(0, EPSILON) < self.episilon:
            move = random.randint(0, 3)
            action[move] = 1
        else:
            state0 = torch.tensor(old_state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            action[move] = 1

        return action

    def load_model(self):
        if os.path.isfile(file_path):
            print("Loading model...")
            self.model.load_state_dict(torch.load(file_path))
            self.model.eval()
            print("Model loaded.")

    def save_model(self):
        self.model.save(file_name=file_name)


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    steps = 0
    total_reward = 0
    agent = Agent()
    game = AsteroidsGame(True)
    game.step(action=[0, 0, 0, 0])
    print("Starting training...")

    while agent.episodes < EPISODES:
        old_state = agent.get_state(game)

        next_action = agent.get_action(old_state)

        reward, done, score = game.step(action=next_action)
        score = int(score)
        new_state = agent.get_state(game)

        # agent.train_short(old_state, next_action, reward, new_state, done)
        agent.memorize(old_state, next_action, reward, new_state, done)

        steps += 1

        if done:
            game.reset(True)
            agent.episodes += 1
            agent.train_long()

            if score > record:
                record = score

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.episodes
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

            print(f"Score: {score}\n" f"Steps: {steps}\n" f"Reward: {total_reward}\n")

            steps = 0
            total_reward = 0


if __name__ == "__main__":
    train()
