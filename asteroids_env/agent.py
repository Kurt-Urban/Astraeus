import torch
import random
import numpy as np
from collections import deque
from Asteroids.game_logic import AsteroidsGame
from model import Linear_QNet, QTrainer
from utils import plot
import os

MAX_MEM = 1_000_000
BATCH = 10000
LR = 0.001
GAMMA = 0.99
EPSILON = 100
EPISODES = 1000
EPSILON_MIN = 0.05
N_TRANSITIONS_BETWEEN_UPDATES = 64


file_name = "model1.pth"
file_path = f"models/{file_name}"


class Agent:
    def __init__(self) -> None:
        self.episodes = 0
        self.epsilon = 0  # Exploration
        self.gamma = GAMMA  # Discount
        self.memory = deque(maxlen=MAX_MEM)
        self.model = Linear_QNet(22, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

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

    def get_action(self, old_state):
        self.epsilon = max((EPSILON - self.episodes) / EPSILON, EPSILON_MIN)
        # [fwd,left,right]
        action = [0, 0, 0]
        if np.random.uniform(0, 1) < self.epsilon:
            move = random.randint(0, 2)
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
    total_reward = 0
    agent = Agent()
    game = AsteroidsGame(True)
    game.step(action=[0, 0, 0, 0])
    print("Starting training...")

    steps = 0
    while agent.episodes <= EPISODES:

        old_state = agent.get_state(game)

        next_action = agent.get_action(old_state)

        reward, done, score = game.step(action=next_action)
        steps += 1
        score = int(score)
        total_reward += reward
        new_state = agent.get_state(game)
        agent.memorize(old_state, next_action, reward, new_state, done)

        if steps % N_TRANSITIONS_BETWEEN_UPDATES == 0:
            agent.train_long()

        if done:
            game.reset(True)

            if score > record:
                record = score

            agent.episodes += 1
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.episodes
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

            print(
                f"Episode: {agent.episodes}\n"
                f"Score: {score}\n"
                f"Steps: {steps}\n"
                f"Reward: {total_reward}\n"
                f"Mean: {plot_mean_scores[-1]}\n"
            )

            steps = 0
            total_reward = 0


if __name__ == "__main__":
    train()
