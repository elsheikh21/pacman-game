import numpy as np
import gym
import time

env = gym.make('MyPacman-v0')
observations = env.reset()
env.render()

print("Action space is: {}".format(env.action_space))
print("State space is: {}".format(env.observation_space))

# First, we'll initialize the Q-table state space x 4 matrix of zeros
q_table = np.zeros([env.observation_space.n, env.action_space.n])

# Alpha (α): (the learning rate) should decrease as you continue to gain a
# larger and larger knowledge base.

# Gamma (γ): as you get closer and closer to the deadline, your preference
# for near-term reward should increase, as you won't be around long enough
# to get the long-term reward, which means your gamma should decrease.

# Epsilon (ϵ): as we develop our strategy, we have less need of exploration &
# more exploitation to get more utility from our policy,
# so as trials increase, epsilon should decrease.

# We decide whether to pick a random action or to exploit the
# already computed Q-values.
# This is done simply by using the epsilon, and comparing to
# random.uniform(0, 1)

alpha = 0.1
gamma = 0.6
epsilon = 0.1

utilities = []

for game in range(100):
    print("\n**************************************************************")
    utility = 0
    state = env.reset()
    for t in range(1000):
        print(
            "\n--- Step #{} - Game #{} ---\n".format(t, game))
        if (epsilon > np.random.uniform(0, 1)):
            random_action = True
            action = env.action_space.sample()
        else:
            # Exploit the learned value
            action = np.argmax(q_table[state])

        action = env.action_space.sample()
        next_state, reward, done, info = env.step(action)

        old_value = q_table[state, action]
        next_max = np.max(q_table[next_state])

        new_value = (1 - alpha) * old_value + alpha * \
            (reward + gamma * next_max)
        q_table[state, action] = new_value

        utility += reward

        state = next_state

        print("\n--- Utility (sum of rewards) = {} ---\n".format(str(utility)))
        print("--- Game Over = {} ---\n".format(str(done)))
        # env.render()
        time.sleep(1.0)
        # print("\n-------------------------------------------")
        if (done):
            print("Episode done after {} timesteps.\n".format(t+1))
            break
    print("**************************************************************\n")
    utilities.append(utility)

print(utilities.index(max(utilities)))
print(q_table)

# Evaluate agent's performance after Q-learning

episodes = 100
total_epochs = 0

for _ in range(episodes):
    state = env.reset()
    epochs, reward = 0, 0

    done = False

    while not done:
        action = np.argmax(q_table[state])
        state, reward, done, info = env.step(action)

        epochs += 1

    total_epochs += epochs

print(f"Results after {episodes} episodes:")
print(f"Average timesteps per episode: {total_epochs / episodes}")

# env.reset() Resets the environment and returns a random initial state.
# env.render() Renders one frame of the environment (to visualizing env)

# Action space: set of all the actions that agent can take in a given state.

# env.step(action): Step the environment by one timestep. Returns
# observation: Observations of the environment
# reward: If your action was beneficial or not
# done: Indicates if game terminated, also called one episode
# info: Additional info such as performance & latency for debugging


# Q-Learning Process
# Breaking it down into steps, we get

# 1. Initialize the Q-table by all zeros.
# 2. Start exploring actions: For each state, select any one among all
#   possible actions for the current state (S).
# 3. Travel to the next state (S') as a result of that action (a).
# 4. For all possible actions from the state (S')
#   select the one with the highest Q-value.
# 5. Update Q-table values using the equation.
# 6. Set the next state as the current state.
# 7. If goal state is reached, then end and repeat the process.

'''
After enough random exploration of actions, the Q-values tend to converge
serving our agent as an action-value function which it can exploit to pick the
most optimal action from a given state.

There's a tradeoff between exploration (choosing a random action) and
exploitation (choosing actions based on already learned Q-values).
We want to prevent the action from always taking the same route, and possibly
overfitting, so we'll be introducing another parameter called ϵ "epsilon"
to cater to this during training.

Instead of just selecting the best learned Q-value action, we'll sometimes
favor exploring the action space further. Lower epsilon value results in
episodes with more penalties (on average) which is obvious because we are
exploring and making random decisions.
'''
