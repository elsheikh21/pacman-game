import gym
import time

env = gym.make('MyPacman-v0')
observations = env.reset()

print("Action space is: {}".format(env.action_space))

for game in range(100):
    print("\n**************************************************************")
    state = env.reset()
    utility = 0
    for t in range(1000):
        print(
            "\n--- Step #{} - Episode #{} ---\n".format(t, game))
        action = env.action_space.sample()
        next_state, reward, done, info = env.step(action)
        utility += reward
        print("\n--- Utility (sum of rewards) = {} ---\n".format(str(utility)))
        print("--- Game Over = {} ---\n".format(str(done)))
        env.render()
        time.sleep(1.0)
        print("\n-------------------------------------------")
        if (done):
            print("Episode done after {} timesteps.\n".format(t+1))
            break
    print("**************************************************************\n")


# env.reset() Resets the environment and returns a random initial state.
# env.render() Renders one frame of the environment (to visualizing env)

# Action space: set of all the actions that agent can take in a given state.

# env.step(action): Step the environment by one timestep. Returns
    # observation: Observations of the environment
    # reward: If your action was beneficial or not
    # done: Indicates if game terminated, also called one episode
    # info: Additional info such as performance & latency for debugging
