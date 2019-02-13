# Introduction

Reinforcement Learning (RL), is basically all about learning what to do. More formally, it is a computational approach for understanding and automating goal directed learning and decision making.

<ins>How?</ins>

Agent learns from direct interactions with the environment, without relying on exemplary supervision or complete models of the environment.
By mapping situations into actions, to maximize the reward signal, so it is a goal directed agent.
In order to do so, the agent must be able to sense the environment to an some extent, and must be able to take actions affecting the environment. As well as, having a goal.

> Agent: must have
>
> 1. Sensation
> 2. Actions
> 3. Goal

So, in every state the agent must pick the action that maximizes its utility? or try to exploit new options that might and might not maximize its reward, this is debatable.

Apart from the agent and environment, we need to specify 4 main sub elements

1. _Policy:_ defines the agent's way of behaving at a given time, can be thought of as a rule that tells the agent what to do.
2. _Reward Function:_ maps from state-action pair to a number, representing the agents goal. As mentioned earlier, the agent's sole goal is to maximize its reward, not to mention that, it might be perceived as function identifying the good and bad.
3. _Value Function:_ defines what is good for the long run, expected accumulated reward after few steps or after going down a certain path.
4. _Environment Model_

We can also sum this up as follows

> formal framework defining the interaction between agent and environment in terms of states, actions, and rewards

Most relevant is the formalism of Markov decision processes([MDP](Markov_Decision_Process.md))
