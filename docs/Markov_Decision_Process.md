# Introduction

Agent makes its decisions based on the basis of a signal from the environment known as "state".
State is basically whatever information of the environment that is available to the agent, if this signal retains all the info about the environment then it is called a "Markov"

> Markov Signal: Signal that retained all the relevant information about environment.

> Markov property is important, because, decisions and values are assumed to be a function only of the current state.

---

## Markov Decision Property

So any RL task satisfying Markov property, is known as **Markov Decision Property** or **MDP**.

Since we are working with dynamic systems, we need to model. They are modeled as follows:

1. **X** set of states
2. **A** Actions
3. **γ** Transition function
   - Deterministic
     - γ(state-x, action-a) = new-state-x'
     - Reward(state-x, action-a) = r ∈ ℝ
   - Non Deterministic
     - γ(state-x, action-a) = 2 ^ state-x
   - Stochastic
     - γ(state-x, action-a) = P(new-state-x'|state-x, action-a), Probability distribution over the states
4. **Z** Set of Observations

But the good thing is that the states are fully observable, so we do not care that much for the environment being deterministic or not.

> MDP can be parameterized by -> <X, A, γ, Z>

Almost all RL algorithms, are based on estimating value functions, functions of states that estimate "how good" it is for the agent to be in a given state or "how good" to perform a specific action in a given state.

"how good" is defined in terms of future rewards that are expected. Of course, value functions are defined w.r.t particular policies.

Policy (π), mapping from states (s ∈ S), and actions (a ∈ A(s)), to the probability [π(s, a)] of taking action (a) when in state (s).
