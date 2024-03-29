# Bayes Filters

## Algorithm

The general Bayesian filter algorithm can be summarized as follows.

```python
def new_belief(x[t-1], u[t], z[t]):
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
{\int p(z_{t} \mid x^\prime_{t})\; \overline{bel}(x^\prime_{t}) dx^\prime_{t}}
$$

## Numerical Example

### Belief

Let's say we have a robot and it can estimate the state of a door using its camera. The state space for a door is binary, i.e. it is either open or closed. We begin with a uniform belief function, i.e. we assign equal probability to guess whether the door is open or closed.

$$
bel(X_{0} = \text{open}) = 0.5 \\
bel(X_{0} = \text{closed}) = 0.5
$$

### Measurement

Robot's sensor is noisy, we need to characterize it by some conditional probabilities.

$$
p\,(Z_{t} \mid X_{t}) = \text{measurement probability}
$$

| Measurement Z | State X | Measurement Probability |
| :--- | :--- | :--- |
| Open | Open | 0.6 |
| Closed | Open | 0.4 |
| Open | Closed | 0.2 |
| Closed | Closed | 0.8 |

The robot is relatively reliable in detecting a closed door which makes a lot of sense. It is a lot easier to develop an algorithm to detect that the door is closed. On the other hand, we have a 40% chance to make a wrong detection when the door is actually open.

### Control

Robot's action is also probabilistic, we **cannot** make the assumption that when the robot tries to open a door, the door will always end up in open state. We have to continue to use conditional probabilities to describe the action outcome.

$$
p\,(X_{t} \mid X_{t-1}, U_{t}) = \text{state transition probability}
$$

| State X | Previous State X | Control | State Transition Probability |
| :--- | :--- | :--- | :--- |
| Open | Open | Push | 1 |
| Closed | Open | Push | 0 |
| Open | Closed | Push | 0.8 |
| Closed | Closed | Push | 0.2 |

Another possibility is that the robot does nothing and performs null control.

| State X | Previous State X | Control | State Transition Probability |
| :--- | :--- | :--- | :--- |
| Open | Open | Null | 1 |
| Closed | Open | Null | 0 |
| Open | Closed | Null | 0 |
| Closed | Closed | Null | 1 |

#### Calculate New Belief

Our state space is discrete, either _open_ or _closed_, either _push_ or _null_. We can use a summation instead of integral to calculate our control update. Let's say the robot is performing a _null_ action.

$$
\overline{bel}(x_{1}) = \sum_{x_{0}} p(x_{1} \mid u_{1}, x_{0})\, bel(x_{0})
$$

That is equivalent to

$$
\overline{bel}(x_{1}) = p(x_{1} \mid \text{null, $x_{0}$=open}) \, bel(\text{$x_{0}$=open}) + p(x_{1} \mid \text{null, $x_{0}$=closed})\,bel(\text{$x_{0}$=closed})
$$

Now we can consider the two potential value for $$x_{1}$$, which is either _open_ or _closed_.

$$
\overline{bel}(\text{open}) = p(\text{open} \mid \text{null, $x_{0}$=open}) \; bel(\text{$x_{0}$=open}) + p(\text{open} \mid \text{null, $x_{0}$=closed}) \; bel(\text{$x_{0}$=closed}) \\= (1)(0.5) + (0)(0.5) = 0.5
$$

$$
\overline{bel}(\text{closed}) = p(\text{closed} \mid \text{null, $x_{0}$=open}) \; bel(\text{$x_{0}$=open}) + p(\text{closed} \mid \text{null, $x_{0}$=closed}) \; bel(\text{$x_{0}$=closed}) \\= (0)(0.5) + (1)(0.5) = 0.5
$$

The fact that the $$\overline{bel}(x{1})$$ _is equal to the prior belief_ $$bel(x{0})$$ should not be surprising to us, because a _null_ action should not change the state of the world. Once we incorporate our measurement update, then our new belief will become more accurate reflection of the true state.

Let's first calculate our normalizer factor.

$$
\eta = \sum_{x_{1}} p(z_{1} \mid x_{1}) \overline{bel}(x_{1}) \\=
p(z_{1}=\text{open} \mid x_{1}=\text{open}) \; \overline{bel}(open) + 
p(z_{1}=\text{open} \mid x_{1}=\text{closed}) \; \overline{bel}(closed) \\= (0.6)(0.5) + (0.2)(0.5) = 0.4
$$

Now there are two possible states, given that $$z_{t}$$ is a given here, just like $$u_{t}$$. We assume that $$z_{t} = \text{open}$$.

* Robot sensed the door is opened and it is actually open
* Robot sensed the door is opened but it is actually closed

Then our new belief will become

$$
bel(X_{1} = \text{open}) = (0.6)(0.5) / 0.4 = 0.75 \\
bel(X_{1} = \text{closed}) = (0.2)(0.5) / 0.4 = 0.25
$$

Now for the second state, if we decide to apply $$u_{2} = \text{push}$ and $z_{2} = \text{open}$$, then we get the following control updates.

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

We need to show that the posterior distribution $$p(x_{t} \mid z_{1:t}, u_{1:t})$$can be calculated from the corresponding posterior distribution one time step earlier, $$p(x_{t-1} \mid z_{1:t-1}, u_{1:t-1})$$ in order to prove the correctness of Bayes filter algorithm by induction. Let's assume that we correctly initialized the prior belief $$bel(x_{0})$$ at time $$t = 0$$ and state $$X$$is complete.

Applying Bayes rule on $$p(x_{t} \mid z_{1:t}, u_{1:t})$$

$$
\tag{1} p(x_{t} \mid z_{1:t}, u_{1:t}) = \frac
{p(z_{t} \mid x_{t}, z_{1:t-1}, u_{1:t-1})\;p(x_{t} \mid z_{1:t-1}, u_{1:t})}
{p(z_{t} \mid z_{1:t-1}, u_{1:t})}
$$

We can find the normalizer $$\eta$$ by integrating over all the possible $$x_{t}$$ values, just like we did before in example above. Now we can exploit the fact that $$x_{t-1}$$ is complete. We are interested in predicting the measurement values. There are no past measurement or control would provide us additional information. This can be expressed by the following conditional independence.

$$
\tag{1a} p(z_{t} \mid x_{t}, z_{1:t-1}, u_{1:t}) = p(z_{t} \mid x_{t})
$$

Then we can simplify the the equation 1 as follows.

$$
\tag{2} p(x_{t} \mid z_{1:t}, u_{1:t}) = \eta \; p(z_{t} \mid x_{t}) \; p(x_{t} \mid z_{1:t-1}, u_{1:t})
$$

Hence the new belief is

$$
\tag{3} bel(x_{t}) = \eta\; p(z_{t}\mid x_{t}) \; \overline{bel}(x_{t})
$$

We need to expand the terms in $$\overline{bel}(x_{t})$$.

$$
\tag{4} \overline{bel}(x_{t}) = \int p(x_{t} \mid x_{t-1}, z_{1:t-1}, u_{1:t}) \; p(x_{t-1} \mid z_{1:t-1}, u_{1:t})\;dx_{t-1}
$$

Once again, we we exploit the assumption that our state is complete. This implies if we know $$x_{t-1}$$, past measurements and controls convey no information regarding the state $$x_{t}$$.

$$
\tag{4a} p(x_{t} \mid x_{t-1}, z_{1:t-1}, u_{1:t}) = p(x_{t} \mid x_{t-1}, u_{t})
$$

Now we just need to substitute equation 4a into equation 4 to get the final recursive update equation. Also note that control $$u_{t}$$can be safely omitted from the set of conditional variables for randomly chosen controls.

$$
\tag{5} \overline{bel}(x_{t}) = \int p(x_{t} \mid x_{t-1}, u_{t}) \; p(x_{t-1} \mid z_{1:t-1}, u_{1:t-1})\;dx_{t-1}
$$

To summarize, the Bayes filter algorithm calculates the posterior over the state $$x_{t}$$conditioned on measurement and control data up to time $$t$$. The derivation assumes that the world is Markov, that is, the state is complete. Any concrete implementation of this algorithm requires three probability distributions.

1. Initial belief $$p(x_{0})$$
2. Measurement probability $$p(z_{t} \mid x_{t})$$
3. State transition probability $$p(x_{t} \mid u_{t}, x_{t-1})$$

### The Markov Assumption

The Markov assumption postulates that past and future data re independent if one knows the current state $$x_{t}$$ and it must be complete. The problem is that in real world application, we have no way to know the complete state at any given time. There are many factors that may induce violations of the Markov assumption.

* Unmodeled dynamics in the environment are not included in the state, e.g. moving people
* Inaccuracies in the probabilistic models and distributions
* Approximation errors
* Software variables in the robot control software

There are many algorithms and techniques derived from the Bayes filter. Each of them relies on a different assumptions regarding the measurement, state transition probabilities, and the initial belief. The assumptions give rise to different computational characteristics.

* Computational efficiency
* Accuracy of approximation
* Ease of implementation

