import numpy as np
import random
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Phase_Brick import PhaseBricks

LEARN_RATE = 0.1
DISCOUNT = 0.95
START = 1.0
DECAY = 0.995
MIN = 0.05

def get_state(paddle_x, ball_x, ball_y, ball_velo_x, ball_velo_y):
    return(
        int(paddle_x // 40),
        int(ball_x // 40),
        int(ball_y // 40),
        1 if ball_velo_x > 0 else -1,
        1 if ball_velo_y > 0 else -1
    )

actions = [0, 1, 2]
q_table = {}

def get_q_value(state):
    if state not in q_table:
        q_table[state] = [0.0, 0.0, 0.0]
    return q_table[state]

env = PhaseBricks()
epsilon = START

for episode in range(5000):
    print(f"FeroAero is starting episode {episode}...")

    total_reward = 0
    done = False

    raw_state = env.reset()
    state = get_state(*raw_state)

    while not done:
        if random.random() < epsilon:
            action = random.choice(actions)
        else:
            q_vals = get_q_value(state)
            action = np.argmax(q_vals)

        next_raw_state, reward, done = env.step(action)
        next_state = get_state(*next_raw_state)

        old_q_values = get_q_value(state)
        next_q_values = get_q_value(next_state)

        old_q_values[action] = old_q_values[action] + LEARN_RATE * (reward + DISCOUNT* max(next_q_values) - old_q_values[action])

        q_table[state] = old_q_values
        state = next_state
        total_reward += reward

    if epsilon > MIN:
        epsilon *= DECAY

    if episode % 50 == 0:
        print(f"Episode: {episode} | Total Accumulated Score: {total_reward:.2f} | Exploration Bias: {epsilon:.2f}")

print("Training finished! FeroAero has conquered the simulation matrix.")
    