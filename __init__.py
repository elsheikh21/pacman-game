from gym.envs.registration import register

register(
    id='MyPacman-v0',
    entry_point='my_pacman.envs:MyPacman',
)
