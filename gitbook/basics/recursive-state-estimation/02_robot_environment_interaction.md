# Robot Environment Interaction

We need to define couple more terminology that will be used throughout the notebook here.

## State

Environments are characterized by state. We will denote state as $$x$$ and a state at time $$t$$ is denoted as $$x_{t}$$.

## Environment Interaction

Perception is the process by which the robot uses its sensors to obtain information about the state of its environment. We can denote **measurement data** at time t as $$z_{t}$$.

Control actions change the state of the world. Even if the robot does not perform any action itself, the state usually changes. For consistency, we will assume that robot always executes a control action, even if it chooses not to move any of its motors. **Control data** carry information about the change of state in the environment. We will denote it as $$u_{t}$$. The variable will always correspond to the change of state in the time interval $$(t - 1; t]$$.

If a state is complete, then it is a sufficient summary of all that happened in the previous time steps. We can express this idea through conditional independence.

$$
p(x_{t} \mid x_{0:t-1}, z_{1:t-1}, u_{1:t-1} = p(x_{t} \mid x_{t-1}, u{t})
$$

That is basically saying, if we know the everything so well, we can simply predict the current state by knowing the previous state and the control action that is going to influence it. Similarly we can predict measurement data by knowing the complete previous state and control action, because measurement data is merely a reflection of the current state. Knowledge of any other variables, such as past measurements, controls, or even past states, is irrelevant if $$x_{t}$$ is complete.

$$
p(z_{t} \mid x_{0:t-1}, z_{1:t-1}, u_{1:t}) = p(z_{t} \mid x_{t})
$$

### State Transition Probability

State transition probability specifies how environmental state evolves over time as a function of robot controls $$u_{t}$$.

$$
p(x_{t} \mid x_{t-1}, u_{t})
$$

### Measurement Probability

Measurement probability specifies the probablistic law according to which measurements $$z$$ are generated from the environment state $$x$$.

$$
p(z_{t} \mid x_{t})
$$

The state at time $$t$$ is stochastically dependent on the state at time $$t-1$$ and the control $$u_{t}$$. The measurement depends stochastically on the state at time $$t$$. Such a temporal generative model is also known as **Hidden Markov Model**.

### Belief

A belief reflects the robot's internal knowledge about the state of the environment. A belief distribution assigns a probability to each possible hypothesis with regards to the true state. Belief distributions are posterior probabilities over state variables conditioned on the available data.

$$
bel(x_{t}) = p(x_{t} \mid z_{1:t}, u_{1:t})
$$

The belief function above incorporates the current measurement data but sometimes we wish to make a prediction and compare it to the actual measurement data, such prediction is denoted as follows.

$$
\overline{bel(x_{t})} = p(x_{t} \mid z_{1:t-1}, u_{1:t})
$$

Calculating $$bel(x_{t})$$ from $$\overline{bel(x_{t})}$$ is called correction or measurement update.
