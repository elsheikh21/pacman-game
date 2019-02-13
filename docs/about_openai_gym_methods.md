# Different methods used from openai gym

- env.reset() Resets the environment and returns a random initial state.

- env.render() Renders one frame of the environment (to visualizing env)

- env.step(action): Step the environment by one timestep. Returns
  observation: Observations of the environment
  reward: If your action was beneficial or not
  done: Indicates if game terminated, also called one episode
  info: Additional info such as performance & latency for debugging
