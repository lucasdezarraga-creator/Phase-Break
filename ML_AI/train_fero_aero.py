import numpy as np
import random
import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque

# Setup path to find Phase_Brick (Adjust if your folder structure is different)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Phase_Brick import PhaseBricks

# --- HYPERPARAMETERS ---
LEARN_RATE = 0.001
DISCOUNT = 0.99
EPSILON_START = 1.0
EPSILON_DECAY = 0.996  # Decays smoothly to give the network time to learn
EPSILON_MIN = 0.02
MEMORY_SIZE = 10000
BATCH_SIZE = 64

# --- NEURAL NETWORK BRAIN ---
class DQNBrain(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQNBrain, self).__init__()
        # Dense layers to process spatial relations smoothly
        self.fc1 = nn.Linear(state_size, 64)
        self.fc2 = nn.Linear(64, 64)
        self.output_layer = nn.Linear(64, action_size)
        
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.output_layer(x)

# --- TRAINING AGENT ---
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=MEMORY_SIZE)
        self.epsilon = EPSILON_START
        
        # Initialize Neural Network and Optimizer
        self.model = DQNBrain(state_size, action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=LEARN_RATE)
        self.loss_fn = nn.MSELoss()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice([0, 1, 2]) # Explore randomly
        
        # Exploit: Turn state into a PyTorch Tensor and predict the best move
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            q_values = self.model(state_tensor)
        return torch.argmax(q_values).item()

    def replay(self):
        if len(self.memory) < BATCH_SIZE:
            return

        # Sample a random batch of past memories to learn from
        minibatch = random.sample(self.memory, BATCH_SIZE)
        
        states = torch.FloatTensor([m[0] for m in minibatch])
        actions = torch.LongTensor([m[1] for m in minibatch]).unsqueeze(1)
        rewards = torch.FloatTensor([m[2] for m in minibatch])
        next_states = torch.FloatTensor([m[3] for m in minibatch])
        dones = torch.FloatTensor([m[4] for m in minibatch])

        # Get current predictions
        current_q = self.model(states).gather(1, actions).squeeze(1)
        
        # Calculate maximum expected future rewards
        next_q = self.model(next_states).max(1)[0].detach()
        target_q = rewards + (DISCOUNT * next_q * (1 - dones))

        # Perform Backpropagation (Gradient Descent)
        loss = self.loss_fn(current_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

def get_normalized_state(paddle_x, ball_x, ball_y, ball_velo_x, ball_velo_y):

    return np.array([
        paddle_x / 1280.0,
        ball_x / 1280.0,
        ball_y / 720.0,
        1.0 if ball_velo_x > 0 else -1.0,
        1.0 if ball_velo_y > 0 else -1.0
    ], dtype=np.float32)

env = PhaseBricks()
agent = DQNAgent(state_size=5, action_size=3)

for episode in range(5000):
    total_reward = 0
    done = False
    
    consecutive_paddle_hits = 0
    
    raw_state = env.reset()
    state = get_normalized_state(*raw_state)
    
    while not done:
        action = agent.choose_action(state)
        next_raw_state, reward, done = env.step(action)
        next_state = get_normalized_state(*next_raw_state)
        
        reward -= 0.005  
        
        agent.remember(state, action, reward, next_state, done)
        
        agent.replay()
        
        state = next_state
        total_reward += reward
        
    if agent.epsilon > EPSILON_MIN:
        agent.epsilon *= EPSILON_DECAY

    if episode % 10 == 0:
        print(f"Episode: {episode} | Score: {total_reward:.2f} | Exploration Bias: {agent.epsilon:.2f}")