import torch
import random
import numpy as np
from collections import deque
from Asteroids.game_logic import AsteroidsGame
from model import Linear_QNet, QTrainer
from utils import plot
import os

MAX_MEM = 1_000_000_000
BATCH = 1000
LR = 0.001
GAMMA = 0.99
EPSILON = 100
EPISODES = 1000
EPSILON_MIN = 0.05
N_TRANSITIONS_BETWEEN_UPDATES = (
    32  # introduced this to make periodic updates sampled from replay memory
)


file_name = "model1.pth"
file_path = f"models/{file_name}"


class Agent:
    def __init__(self) -> None:
        self.episodes = 0
        self.epsilon = 0  # Exploration
        self.gamma = 0.9  # Discount
        self.memory = deque(maxlen=MAX_MEM)
        self.model = Linear_QNet(10, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        # self.load_model()  # I wouldn't load completely overfit models from previous runs that didnt work!

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
        self.epsilon = max(
            (EPSILON - self.episodes) / EPSILON, EPSILON_MIN
        )  # modified this to be in [0, 1]
        # [fwd,left,right,shoot]
        action = [0, 0, 0, 0]
        if np.random.uniform(0, 1) < self.epsilon:
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
    total_reward = 0
    agent = Agent()
    game = AsteroidsGame(True)
    game.step(action=[0, 0, 0, 0])
    state_stack = list()
    print("Starting training...")

    def update_state_stack():
        state_stack.append(agent.get_state(game))
        state_stack.pop(0)

    steps = 0
    while agent.episodes <= EPISODES:
        if agent.episodes == 1:
            for _ in range(3):
                state_stack.append(agent.get_state(game))
        else:
            update_state_stack()

        old_state = state_stack

        next_action = agent.get_action(old_state)

        reward, done, score = game.step(action=next_action)
        steps += 1
        score = int(score)
        total_reward += reward
        update_state_stack()
        new_state = state_stack
        agent.memorize(old_state, next_action, reward, new_state, done)

        # train from replay memory every so often
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
