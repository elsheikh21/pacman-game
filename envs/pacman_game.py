import gym
import time

env = gym.make('MyPacman-v0')
observations = env.reset()

for i_episode in range(10):
    print("******************************************************************")
    observation = env.reset()
    for t in range(100):
        print("\n--- Step number " + str(t) + " - " +
              " Episode number " + str(i_episode) + " --- \n")
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        print("Utility(sums of rewards) = " + str(reward))
        print("Done = " + str(done))
        env.render()
        time.sleep(1.3)
        print("-------------------------------------------")
        if (done):
            print("Episode finished after {} timesteps".format(t+1))
            break
    print("******************************************************************")
