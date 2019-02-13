import gym
import time
import numpy as np
import matplotlib.pyplot as plt
from game_logic import (map_states, get_state_mapping)


def train_agent(iterations=1000, verbose=False,
                epsilon=0.1, gamma=0.6, alpha=0.1):
    '''
    RL task, where agent's doing Q-learning
    '''
    # Used for plotting purposes
    utilities = []
    action_space = env.action_space
    obs_space = env.observation_space
    if(verbose):
        print(f"\nAction space: {action_space} & State space: {obs_space} \n")

    # Define Q-Learning attributes
    '''
    action_size = action_space.n
    state_size = obs_space.n
    q_table = np.zeros([state_size, action_size], dtype=np.float)
    '''
    # retraining the trained model
    q_table = np.load('q_table.npy')

    # for states mapping
    states_list = map_states()

    iterations += 1
    for game in range(1, iterations):
        utility, epochs = 0, 0
        state = env.reset()
        done = False
        # epsilon greedy experimentation strategy
        # decay_rate = 1 / game
        # epsilon *= decay_rate
        while not done:
            if np.random.uniform(0, 1) < epsilon:
                # Explore action space
                action = env.action_space.sample()
            else:
                # Exploit learned values
                action = np.argmax(q_table[state])

            state_idx, next_state, reward, done = env.step(action)
            next_state_idx = get_state_mapping(next_state, states_list)

            old_val = q_table[state_idx, action]
            next_max = np.max(q_table[next_state_idx])

            new_val = (1 - alpha) * old_val + alpha * \
                (reward + gamma * next_max)
            q_table[state_idx, action] = new_val

            utility += reward

            state = next_state_idx
            epochs += 1
            time.sleep(0.1)

            if (done):
                break

        print(f"--- Game = {game} --- Utility = {utility} ---")
        utilities.append(utility)

        if game % 100 == 0:
            print_out(utilities, q_table)

    return q_table, utilities


def print_out(utilities, q_table):
    '''
    Plot the agent's utilities and penalties throughout learning phase
    '''
    with open('output.txt', 'w') as f:
        max_idx = utilities.index(max(utilities))
        print(utilities[max_idx], file=f)
        print(q_table, file=f)
    print('[INFO] data is saved to output.txt')


def plot(utilities):
    plt.plot(utilities)
    plt.title('Utilities variation while learning')
    plt.xlabel('Number of iterations')
    plt.ylabel('Utilities')
    # Show the plot
    plt.show()


def evaluate_performance(episodes, q_table):
    '''
    Evaluate agent's performance after Q-learning
    '''

    total_epochs = 0
    # for states mapping
    states_list = map_states()

    for episode in range(episodes):
        state = env.reset()
        epochs, reward = 0, 0

        done = False
        utility = 0
        count = 0

        while not done:
            count += 1
            action = np.argmax(q_table[state])
            _, next_state, reward, done = env.step(action)
            next_state_idx = get_state_mapping(next_state, states_list)
            utility += reward
            epochs += 1
            env.render()
            state = next_state_idx

        print(f"Game {episode} is over after {count} with {utility} pts.\n")

        total_epochs += epochs

        print(f"Results after {episodes} episodes:")
        print(f"Average timesteps per episode: {total_epochs / episodes}")
        print(f"Utility: {utility}")


# Define the environment
env = gym.make('MyPacman-v0')
state = env.reset()

# if we want to skip the training part just load .npy file
# pretrained_q_table = np.load('q_table.npy')


q_table, utilites = train_agent(iterations=1000, verbose=False,
                                epsilon=0.1, gamma=0.6, alpha=0.1)

# Saving q_table for further use
np.save('q_table.npy', q_table)

plot(utilites)

evaluate_performance(episodes=100, q_table=q_table)
