import numpy as np
import random
import os
import pickle

LEARN_RATE = 0.1
DISCOUNT = 0.95
START = 1.0
DECAY = 0.995
MIN = 0.05

def get_state(paddle_x, ball_x, ball_y, ball_velo_x, ball_velo_y):
    return{
        int(paddle_x // 40),
        int(ball_x // 40),
        int(ball_y // 40),
        1 if ball_velo_x > 0 else -1,
        1 if ball_velo_y > 0 else -1
    }

actions = [0, 1, 2]
q_table = {}

def get_q_value(state):
    if state not in q_table:
        q_table[state] = [0.0, 0.0, 0.0]
    return q_table[state]

for episode in range(5000):
    print(f"FeroAero is starting episode {episode}...")