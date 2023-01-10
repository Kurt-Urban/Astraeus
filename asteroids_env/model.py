import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import os


class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size) -> None:
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, hidden_size)
        self.linear3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = self.linear3(x)
        return x

    def save(self, file_name="model.pth"):
        model_folder_path = "./models"
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, lr, gamma) -> None:
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, states, actions, rewards, next_states, dones):
        states = torch.tensor(states, dtype=torch.float)
        actions = torch.tensor(actions, dtype=torch.int64)
        rewards = torch.tensor(rewards, dtype=torch.float).unsqueeze(-1)
        next_states = torch.tensor(next_states, dtype=torch.float)
        dones = torch.tensor(dones, dtype=torch.bool).unsqueeze(-1)

        # current q values (gather does weird indexing, this is just Q(state)[action], sadly
        # self.model(states)[actions] doesn't behave as you would expect)
        q_vals = self.model(states).gather(
            index=torch.argmax(actions, dim=-1).unsqueeze(1), dim=1
        )

        # expected q values
        with torch.no_grad():  # .no_grad() is important so that no gradients get propagated through the td-target
            next_q_vals = torch.max(self.model(next_states), dim=-1)[0].unsqueeze(-1)

            td_target = rewards + self.gamma * next_q_vals * (
                ~dones
            )  # *(~dones) kills the summand in each index
            # automatically! x*(~True)=0 and x*(~False)=x

        self.optimizer.zero_grad()
        loss = self.criterion(
            q_vals, td_target
        )  # penalize the difference between td-target and predicted q_values
        loss.backward()

        self.optimizer.step()
