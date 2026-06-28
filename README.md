# PhaseBrick: Deep Q-Learning Breakout AI (FeroAero)

An implementation of a Deep Q-Network (DQN) agent named **FeroAero** designed to learn and master a custom, color-matching variant of the classic Breakout game built in Pygame.

## Project Overview
Unlike standard Breakout AIs that only track spatial coordinates, FeroAero must adapt to a dynamic dynamic color-matching economy. When the ball hits the paddle, it randomly changes color. Bricks only break when struck by a ball of a matching color. 

To solve this, the agent is upgraded with a 6-dimensional state space ("Color Vision") and trained using reinforcement learning to optimize tracking, survival, and color alignment.

---

## The Core Architecture

### 1. The Game Environment (`Phase_Brick.py`)
A custom-built Pygame implementation of Breakout featuring:
* Fully integrated physics, bounding boxes, and collision mechanics.
* A dynamic RGB tuple tracking array to map ball-to-brick color states.
* An optimized headless "dummy" rendering mode for high-velocity machine learning.

### 2. The Brain & Agent (`train_fero_aero.py`)
* **Neural Network:** A Deep Q-Network (DQN) built in PyTorch featuring 128 hidden nodes across dense layers to process complex spatial-color dimensions.
* **Optimization:** Adam optimizer paired with a Mean Squared Error (MSE) loss calculation loop.
* **Experience Replay:** A cyclic memory buffer (`deque`) that stores past frames to break data correlation and smooth out gradient updates.

---

## Balanced Reward Economy
To prevent the agent from getting trapped in local minimums (like running away or infinite stalling), the environment operates on a highly calibrated financial framework:

* **Survival (Catching Ball):** `+150.0`
* **Success (Matching Brick Hit):** `+100.0`
* **Distance Bonus:** Up to `+0.5` per frame based on proximity to the ball's X-axis (the tracking guide).
* **Failure (Dropping Ball):** `-1000.0`
* **Mismatch Penalty:** `-5.0` (Gently discourages wrong color choices).

---

## Acknowledgments & Development Note

This architecture was developed using AI-assisted engineering practices in collaboration with Google Gemini to optimize the high-performance Rust physics simulation, map corresponding multi-language state spaces, and design the decoupled Deep Q-Network pipeline.

It has been an absolute blast helping you wire up this high-speed engine, wrestle with Windows PowerShell wildcards, and beat back the GitHub 100MB file limits! Fero Aero is running on an incredibly sleek stack now.
