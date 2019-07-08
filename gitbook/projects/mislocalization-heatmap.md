# Mislocalization Heatmap

### General Math Concepts

#### Joint Distribution

The joint distribution of two random variables $$X$$ and $$Y$$ are written as follows.

$$
p(x,y)=p(\text{$X=x$ and $Y=y$})
$$

If they are independent,

$$
p(x, y) = p(x)p(y)
$$

If they are conditioned,

$$
p(x∣y)=p(X=x \mid Y=y)
$$

#### Theorem of Total Probability

$$
p(x) = \sum_y p(x \mid y)p(y) = \int p(x \mid y)p(y) dy
$$

#### Bayes' Rule

$$
p(x \mid y) = \frac{p(y \mid x) p(x)}{p(y)}
$$

Since we know $$x$$ and $$y$$ are conditioned on each other, we can use the theorem of total probability to express Bayes' rule.

In discrete form,

$$
p(x \mid y) = \frac{p(y \mid x)p(x)}{\sum_{x^\prime} p(y \mid x^\prime) p(x^\prime)}
$$

In integral form,

$$
p(x \mid y) = \frac{p(y \mid x)p(x)}{\int p(y \mid x^\prime) p(x^\prime) dx^\prime}
$$

#### Prior & Posterior Distribution

If $$x$$ is a quantity that we would like to infer from $$y$$, then

* $$p(x)$$ is called prior probability distribution.
* $$p(x \mid y)$$ is called posterior probability distribution over $$X$$.
* $$p(y \mid x)$$ is called generative model. 

In general $$Y$$ is called data, e.g. range finder laser measurements or control actions. 

### Glossary

* Let $$x_t$$ denote robot state at time $$t$$.
* Let $$u_t$$ denote control action we apply to a robot at time $$t$$. 
* Let $$z_t$$ denote measurement at time $$t$$.

#### State Transition Probability

State transition probability describes what is the likelihood of producing a new state $$x_t$$ given that previous state $$x_{t-1}$$ and control action $$u_t$$.

$$
p(x_t, \mid x_{t-1}, u_t)
$$

#### Measurement Probability

Measurement probability describes what is the likelihood of seeing a set of measurements, given the current state $$x_t$$. 

$$
p(z_t \mid x_t)
$$

#### Belief

A belief reflects the robot's internal knowledge about the state of the environment. A belief distribution assigns a probability to each possible hypothesis with regards to the true state. Belief distributions are posterior probabilities over state variables conditioned on the available data.

Using zero indices, a belief is described as follows.

$$
bel(x_t) = p(x_t \mid z_{0:t}. u_{0:t})
$$

For each time step, before we incorporate the measurement data, we would like to make a prediction. The prediction belief is described as follows.

$$
\overline{bel}(x_t) = p(x_t \mid z_{0:t-1}, u_{0:t})
$$

Calculating a belief from a prediction belief is called correction or measurement update.

$$
\text{measurement update}: \overline{bel}(x) \to bel(x_t)
$$

### Bayes Filter

The general Bayes filter involves two steps. 

1. Generate prediction of current state $$x_t$$ using previous state $$x_{t-1}$$ and control action $$u_t$$.
2. Perform correction, also known as measurement update, by incorporating $$z_t$$.

#### Prediction

Formally speaking, it is impossible to know the true state $$x_t$$, at best we can only describe what we know about the current state or previous state as a probability density function, denote as $$bel(x_t)$$.  

$$
\overline{bel}(x_t) = \int p(x_{t} \mid u_t, x_{t-1})\;bel(x_{t-1}) dx_{t-1} = \text{control\_update}(u_t, x_{t-1})
$$

Prediction step is also called **control update**.

#### Measurement Update

As noted before, the final belief function is a probability density function that tells you what is the probability for the random variable $$X$$ to take the value of $$x_t$$. 

$$
bel(x_t) = \frac{p(z_t \mid x_t)\;\overline{bel}(x_t)}{\int p(z_t \mid x^\prime_t)\;\overline{bel}(x^\prime_t)\; dx^\prime} = \text{measurement\_update}(z_t, x_t)
$$

### MCL Particle Filter

Monte Carlo Localization Particle Filter is an algorithm derived from the Bayes filter, suitable for representing beliefs that cannot be modeled by Gaussian or other parametric models.

> Parametric model is a class of probability distributions that has a finite number of parameters.

Particle filters represent beliefs by a cluster of particles. It usually involves 4 major steps.

1. Initialize a set of $$M$$ particles.
2. Iterate through each particle, for $$m = 1$$ to $$m = M$$.
   1. Perform control update on particle $$p_m$$.
   2. Perform measurement update on particle $$p_m$$.
   3. Compute weight $$w_m$$of the particle.
   4. Add $$p_m$$ to a sample set.
3. Iterate $$M$$ times.
   1. Draw $$p_m$$ from sample set with probability proportional to $$w_m$$ with replacement.
   2. Add $$p_m$$ to the final sample set.
4. Return final sample set, which should have length $$M$$.

Repeat step 2 to step 4 for subsequent control and measurement updates.

