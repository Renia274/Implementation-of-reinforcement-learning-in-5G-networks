# Implementation-of-reinforcement-learning-in-5G-networks


This repository contains an implementation of reinforcement learning algorithms in order to optimize a 5G network. The goal of this project is to use Reinforcement Learning(RL) to improve network performance, such as reducing latency and maximizing throughput, in dynamic and complex 5G environments.

Installation and Usage

To install and use this code, follow these steps:

    Clone the repository to your local machine
    Install the required dependencies (listed in requirements.txt)
    Run the code using the command python main.py

Once the code is running, you can adjust the RL parameters and network settings as needed to optimize performance.

Algorithm and Network Description

We implemented a Q-Learning to optimize network performance. The agent interacts with the environment by selecting actions that maximize its expected reward. The network architecture consists of a number of nodes, each representing a 5G base station. The agent observes the current state of the network, such as transmited power, and takes actions to adjust the transmitted power to the base station to improve network performance.

