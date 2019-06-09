
# Recursive State Estimation

## Basic Concepts in Probability

Let $X$ denotes a random variable, then $x$ is a specific value that $X$ might assume.

$$
p(X = x) \;\text{denotes the probability of $X$ has the value of $x$}
$$

Therefore,

$$
\sum_{x} p(X = x) = 1
$$

All continuous random variables possess probability density function, **PDF**.

$$
p(x) = (2\pi\sigma^{2})^{-1/2} \exp{\frac{-1}{2}\frac{(x - \mu)^{2}}{\sigma^{2}}}
$$

We can abbreviate the equation as follows, because it is a normal distribution.

$$
N(x; \mu; \sigma^{2})
$$

However, in general, $x$ is not a scalar value, it is generally a vector. Let $\Sigma$ be a positive semidefinite and symmetric matrix, which is a **covariance matrix**.

$$
p(x) = det(2\pi\Sigma)^{-1/2} \exp{ \frac{-1}{2} (\vec{x} - \vec{\mu})^{T} \Sigma^{-1} (\vec{x} - \vec{\mu})}
$$

and

$$
\int p(x) dx = 1
$$

The joint distribution of two random variables $X$ and $Y$ can be described as folows.

$$
p(x, y) = p(\text{$X = x$ and $Y = y$})
$$

If they are independent, then

$$
p(x,y) = p(x)p(y)
$$

If they are conditioned, then

$$
p(x \mid y) = p(X=x \mid Y=y)
$$

If $p(y) > 0$, then

$$
p(x \mid y) = \frac{p(x, y)}{p(y)}
$$

**Theorem of Total Probability** states the following.

$$
p(x) = \sum_{y} p(x \mid y)p(y) = \int p(x \mid y)p(y)dy
$$

We can apply **Bayes Rule**. 

$$
p(x \mid y) = \frac{ p(y \mid x) p(x) }{ p(y) } = \frac{ p(y \mid x) p(x) } { \sum_{x`} p(y \mid x`) p(x`)}
$$

In integral form,

$$
\frac{ p(y \mid x) p(x) } { \int p(y \mid x`) p(x`) dx`}
$$

If $x$ is a quantity that we would like to inrefer from $y$, the probability $p(x)$ is referred as **prior probability distribution** and $y$ is called data, e.g. laser measurements. $p(x \mid y)$ is called **posterior probability distribution** over $X$.

In robotics, $p(y \mid x)$ is called **generative model**. Since $p(y)$ does not depend on $x$, $p(y)^{-1}$ is often written as a normalizer in Bayes rule variables.

$$
p(x \mid y) = \eta p(y \mid x) p(x)
$$

It is perfectly fine to to condition any of the rules on arbitrary random variables, e.g. the location of a robot can inferred from multiple sources of random measurements.

$$
p(x \mid y, z) = \frac{ p(x \mid x, z) p(y \mid z) }{ p(y \mid z) }
$$

for as long as $p(y \mid z) > 0$.

Similarly, we can condition the rule for combining probabilities of independent random variables on other variables.

$$
p(x, y \mid z) = p(x \mid z)p(y \mid z)
$$

However, conditional independence does not imply absolute indenpendence, that is

$$
p(x, y \mid z) = p(x \mid z)p(y \mid z) \neq p(x,y) = p(x)p(y)
$$

The converse is neither true, absolute independence does not imply conditional independence.

The expected value of a random variable is given by

$$
E[X] = \sum_{x} x p(x) = \int x p(x) dx
$$

Expectation is a linear function of a random variable, we have the following property.

$$
E[aX + b] = aE[X] + b
$$

Covariance measures the squared expected deviation from the mean. Therefore, square root of covariance is in fact variance, i.e. the expected deviation from the mean.

$$
Cov[X] = E[X - E[X]^{2} = E[X^{2}] - E[X]^2
$$

Finally, **entropy** of a probability distribution is given by the following expression. Entropy is the expected information that the value of $x$ carries. 

$$
H_{p}(x) = -\sum_{x} p(x) log_{2}p(x) = -\int p(x) log_{2} p(x) dx
$$

In the discrete case, the $-log_{2}p(x)$ is the number of bits required to encode x using an optimal encoding, assuming that $p(x)$ is the probability of observing $x$.

## Robot Environment Interaction

We need to define couple more terminology that will be used throughout the notebook here.

### State

Environments are characterized by state. We will denote state as $x$ and a state at time $t$ is denoted as $x_{t}$

### Environment Interaction

Perception is the process by which the robot uses its sensors to obtain information about the state of its environment. We can denote **measurement data** at time t as $z_{t}$. 

Control actions change the state of the world. Even if the robot does not perform any action itself, the state usually changes. For consistency, we will assume that robot always executes a control action, even if it chooses not to move any of its motors. **Control data** carry information about the change of state in the environment. We will denote it as $u_{t}$. The variable will always correspond to the change of state in the time interval $(t - 1; t]$.

If a state is complete, then it is a sufficient summary of all that happened in the previous time steps. We can express this idea through conditional independence.

$$
p(x_{t} \mid x_{0:t-1}, z_{1:t-1}, u_{1:t-1} = p(x_{t} \mid x_{t-1}, u{t})
$$

That is basically saying, if we know the everything so well, we can simply predict the current state by knowing the previous state and the control action that is going to influence it. Similarly we can predict measurement data by knowing the complete previous state and control action, because measurement data is merely a reflection of the current state. Knowledge of any other variables, such as past measurements, controls, or even past states, is irrelevant if $x_{t}$ is complete. 

$$
p(z_{t} \mid x_{0:t-1}, z_{1:t-1}, u_{1:t}) = p(z_{t} \mid x_{t})
$$

#### State Transition Probability

State transition probability specifies how environmental state evolves over time as a function of robot controls $u_{t}$.

$$
p(x_{t} \mid x_{t-1}, u_{t})
$$

#### Measurement Probability

Measurement probability specifies the probablistic law according to which measurements $z$ are generated from the environment state $x$.

$$
p(z_{t} \mid x_{t})
$$

The state at time $t$ is stochastically dependent on the state at time $t-1$ and the control $u_{t}$. The measurement depends stochastically on the state at time $t$. Such a temporal generative model is also known as **Hidden Markov Model**.

### Belief 

A belief reflects the robot's internal knowledge about the state of the environment. A belief distribution assigns a probability to each possible hypothesis with regards to the true state. Belief distributions are posterior probabilities over state variables conditioned on the available data.

$$
bel(x_{t}) = p(x_{t} \mid z_{1:t}, u_{1:t})
$$

The belief function above incorporates the current measurement data but sometimes we wish to make a prediction and compare it to the actual measurement data, such prediction is denoted as follows.

$$
\overline{bel(x_{t})} = p(x_{t} \mid z_{1:t-1}, u_{1:t})
$$

Calculating $bel(x_{t})$ from $\overline{bel(x_{t})}$ is called correction or measurement update.

## Bayes Filter

### Algorithm

The general Bayesian filter algorithm can be summarized as follows. 

```python
def new_belief(bel[x[t-1]], u[t], z[t]):
    for x_t in X:
        prediction = control_update(u[t], x[t-1])
        bel[x[t]] = measurement_update(z[t], x[t], prediction)

    return bel[x[t]]
```

The control update is calculated by the following equation.

$$
\text{control_update($u_{t}$, $x_{t-1}$)} = \overline{bel}(x_{t}) =  \int p(x_{t} \mid u_{t}, x_{t-1}) bel(x_{t-1}) dx_{t-1}
$$

The measurement update is calculated by the following equation.

$$
\text{measurement_update($z_{t}$, $x_{t}$)} = bel(x_{t}) = 
\frac{p(z_{t} \mid x_{t})\;\overline{bel}(x_{t})}
{\int p(z_{t} \mid x`_{t})\; \overline{bel}(x`_{t}) dx`_{t}} 
$$


### Numerical Example

#### Belief

Let's say we have a robot and it can estimate the state of a door using its camera. The state space for a door is binary, i.e. it is either open or closed. We begin with a uniform belief function, i.e. we assign equal probability to guess whether the door is open or closed.

$$
bel(X_{0} = \text{open}) = 0.5 \\
bel(X_{0} = \text{closed}) = 0.5
$$

#### Measurement

Robot's sensor is noisy, we need to characterize it by some conditional probabilities.

$$
p(Z_{t} = \text{open} \mid X_{t} = open) = 0.6 \\
p(Z_{t} = \text{closed} \mid X_{t} = open) = 0.4 \\
p(Z_{t} = \text{open} \mid X_{t} = closed) = 0.2 \\
p(Z_{t} = \text{closed} \mid X_{t} = closed) = 0.8
$$

The robot is relatively reliable in detecting a closed door which makes a lot of sense. It is a lot easier to develop an algorithm to detect that the door is closed. On the other hand, we have a 40% chance to make a wrong detection when the door is actually open.

#### Control

Robot's action is also probablistic, we **cannot** make the assumption that when the robot tries to open a door, the door will always end up in open state. We have to continue to use conditional probabilities to describe the action outcome.

$$
p(X_{t} = \text{open} \mid U_{t} = \text{push}, X_{t-1} = \text{open}) = 1 \\
p(X_{t} = \text{closed} \mid U_{t} = \text{push}, X_{t-1} = \text{open}) = 0 \\
p(X_{t} = \text{open} \mid U_{t} = \text{push}, X_{t-1} = \text{closed}) = 0.8 \\
p(X_{t} = \text{closed} \mid U_{t} = \text{push}, X_{t-1} = \text{closed}) = 0.2
$$


Another possibility is that the robot does nothing. 

$$
p(X_{t} = \text{open} \mid U_{t} = \text{null}, X_{t-1} = \text{open}) = 1 \\
p(X_{t} = \text{closed} \mid U_{t} = \text{null}, X_{t-1} = \text{open}) = 0 \\
p(X_{t} = \text{open} \mid U_{t} = \text{null}, X_{t-1} = \text{closed}) = 0 \\
p(X_{t} = \text{closed} \mid U_{t} = \text{null}, X_{t-1} = \text{closed}) = 1
$$

#### Calculate New Belief

Our state space is discrete, either *open* or *closed*, either *push* or *null*. We can use a summation instead of integral to calculate our control update. Let's say the robot is performing a *null* action.

$$
\overline{bel}(x_{1}) = \sum_{x_{0}} p(x_{1} \mid u_{1}, x_{0}) bel(x_{0})
$$

That is equivalent to

$$
\overline{bel}(x_{1}) = p(x_{1} \mid \text{null, $x_{0}$=open}) \; bel(\text{$x_{0}$=open}) + p(x_{1} \mid \text{null, $x_{0}$=closed})\; bel(\text{$x_{0}$=closed})
$$

Now we can consider the two potential value for $x_{1}$, which is either *open* or *closed*.

$$
\overline{bel}(\text{open}) = p(\text{open} \mid \text{null, $x_{0}$=open}) \; bel(\text{$x_{0}$=open}) + p(\text{open} \mid \text{null, $x_{0}$=closed}) \; bel(\text{$x_{0}$=closed}) = (1)(0.5) + (0)(0.5) = 0.5 \\
\overline{bel}(\text{closed}) = p(\text{closed} \mid \text{null, $x_{0}$=open}) \; bel(\text{$x_{0}$=open}) + p(\text{closed} \mid \text{null, $x_{0}$=closed}) \; bel(\text{$x_{0}$=closed}) = (0)(0.5) + (1)(0.5) = 0.5
$$

The fact that the $\overline{bel}(x_{1})$ is equal to the prior belief $bel(x_{0})$ should not be surprising to us, because a *null* action should not change the state of the world. Once we incorporate our measurement update, then our new belief will become more accurate reflection of the true state.

Let's first calculate our normalizer factor.

$$
\eta = \sum_{x_{1}} p(z_{1} \mid x_{1}) \overline{bel}(x_{1}) = \\
p(z_{1}=\text{open} \mid x_{1}=\text{open}) \; \overline{bel}(open) + 
p(z_{1}=\text{open} \mid x_{1}=\text{closed}) \; \overline{bel}(closed) = (0.6)(0.5) + (0.2)(0.5) = 0.4
$$

Now there are two possible states, given that $z_{t}$ is a given here, just like $u_{t}$. We assume that $z_{t} = \text{open}$.

- Robot sensed the door is opened and it is actually open
- Robot sensed the door is opened but it is actually closed

Then our new belief will become

$$
bel(X_{1} = \text{open}) = (0.6)(0.5) / 0.4 = 0.75 \\
bel(X_{1} = \text{closed}) = (0.2)(0.5) / 0.4 = 0.25 
$$

Now for the second state, if we decide to apply $u_{2} = \text{push}$ and $z_{2} = \text{open}$, then we get the following control updates.

$$
\overline{bel}(X_{2} = \text{open}) = (1)(0.75) + (0.8)(0.25) = 0.95 \\
\overline{bel}(X_{2} = \text{closed}) = (0)(0.75) + (0.2)(0.25) = 0.05
$$

Again measurement updates again.

$$
bel(X_{2} = \text{open}) = \eta(0.6)(0.95) = 0.983 \\
bel(X_{2} = \text{closed}) = \eta(0.2)(0.05) = 0.017
$$

It seems impressive that we have a 98.3% of confidence that the door is opened after the robot sensed that the door is opened twice and performed one push control action. However, if this is a mission critical scenario, 1.7% chance of screwing up is still very significant.

### Mathematical Derivation


