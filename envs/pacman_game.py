import gym

env = gym.make('MyPacman-v0')
observations = env.reset()

for t in range(1000):
    action = env.action_space.sample()
    observation, reward, game_over, grid = env.step(action)
    env.render()

    if game_over:
        print("Done in {} timesteps. Reward: {}".format(t+1), reward)
        break
    if (reward == 1000):
        print("Congrats!")
