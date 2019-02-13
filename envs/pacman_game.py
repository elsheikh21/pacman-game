import gym
import time


def random_agent():
    for game in range(100):
        print("\n************************************************************")
        _ = env.reset()
        utility = 0
        for t in range(1000):
            print(f"\n--- Step #{t} - Episode #{game} ---\n")
            action = env.action_space.sample()
            _, _, reward, done = env.step(action)
            utility += reward
            print(f"\n--- Utility (sum of rewards) = {utility} ---\n")
            print(f"--- Game Over = {done} ---\n")
            env.render()
            time.sleep(1.0)
            print("\n-------------------------------------------")
            if (done):
                print("Episode done after {} timesteps.\n".format(t+1))
                break
        print("**************************************************************\n")


# Define environment
env = gym.make('MyPacman-v0')
observations = env.reset()

random_agent()
