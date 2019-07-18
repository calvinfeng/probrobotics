# Particle Filter

The particle filter is just like histogram filter, it approximate the posterior by a finite number of parameters. However, they differ in the way these parameters are generated, and in which they populate the state space. 

The key idea of the particle filter is to represent the posterior $$bel(x_t)$$by a set of random state samples drawn from this posterior. Such representation is approximate, but it is non-parametric, and therefore can represent a much broader space of distributions than, for example, Gaussian. Another advantage of the sample based representation is its ability to model nonlinear transformations of random variables.

In particle filter, the samples of a posterior distribution are called _particles_. 

$$
\chi_t = x_t^1, x_t^2, ..., x_t^M
$$

Each particle $$x_t^m$$ is a concrete instantiation of the state at time $$t$$. In other words, a particle is a hypothesis as to what the true world state may be at time $$t$$. Here $$M$$ denotes the number of particles in the particle set $$\chi_t$$. 

## Algorithm

$$
\text{initialize $\overline{\chi}  = \chi = \emptyset$ to be an empty set}\\\;\\
\text{for $m=1$ to $M$ do:} \\
\text{sample $x_t^m$ from} \; p(x_t \mid u_t, x_{t-1}^m) \\
w_t^m = p(z_t \mid x_t^m) \\
\overline{\chi}_t = \overline{\chi}_t + \langle x_t^m, w_t^m \rangle \\
\text{endfor}\\\;\\
\text{for $m=1$ to $M$ do:}\\
\text{draw $i$ with probability $\propto w_t^i$} \\
\text{add $x_t^i$  to $\chi_t$}\\
\text{endfor} \\\;\\
\text{return $\chi_t$}
$$

The intuition behind particle filter is to approximate the belief $$bel(x_t)$$ by the set of particles $$\chi_t$$. Ideally, the likelihood for a state hypothesis $$x_t$$ to be included in the particle set shall be proportional to its Bayes filter posterior $$bel(x_t)$$. 

Just like all other Bayes filter algorithm, the particle filter algorithm constructs the new belief recursively from the previous belief one time step earlier. Since the beliefs are represented by a set of particles, the filter constructs the new particle set recursively from the previous particle set.

## Details

### Step One 

$$
\text{for $m=1$ to $M$ do:}\\\quad
\text{sample $x^m_t$ from } p(x_t\mid u_t, x^m_{t-1})
$$

We generate a hypothetical state $$x_t^m$$based on the particle from previous time step and the control at current time step.The set of particles obtained from the first for loop is filter's representation of $$\overline{bel}(x_t)$$.

```python
class Particle:
    def move(self, turn, forward):
        if forward < 0:
            raise ValueError('robot cant move backwards')         
        
        # turn, and add randomness to the turning command
        theta = self.theta + float(turn) + random.gauss(0.0, self.turn_noise)
        theta %= 2 * math.pi
        
        # Move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (math.cos(theta) * dist)
        y = self.y + (math.sin(theta) * dist)
        x %= world_size    # cyclic truncate
        y %= world_size
        
        # Create new particle and return it
        p = Particle()
        p.set(x, y, theta)
        p.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return p
```

Notice that `move` produces a new particle state, it is equivalent to produce a new state given the control which is `turn` and `forward`, and previous state, which is `(self.x, self.y, self.theta)`.

### Step Two

$$
w_t^m = p(z_t \mid x_t^m) \\
\overline{\chi}_t = \overline{\chi}_t + \langle x_t^m, w_t^m \rangle  \\
\text{endfor}
$$

The $$w$$ is known as the importance factor or particle scores. Importance factors are used to incorporate measurements. The importance is the probability of the measurement $$z_t$$ under the particle $$x_t^m$$. We compute the particle weight \(importance\) and then add the new particle and its weight to the prediction set, denoted as $$\overline{\chi}_t$$.

```python
class Particle:
    def importance_weight(self, measurement):
        # The likelihood of a measurement gives the important weight.
        prob = 1.0;
        for i in range(len(landmarks)):
            dist = math.sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= gaussian(dist, self.sense_noise, measurement[i])
        return prob
```

### Step Three

$$
\text{for $m=1$ to $M$ do:}\\
\text{draw $i$ with probability $\propto w_t^i$} \\
\text{add $x_t^i$  to $\chi_t$}\\
\text{endfor}
$$

The real trick occurs here which is the re-sampling portion. The algorithm draws with replacement $$M$$ particles from the temporary set $$\overline{\chi}_t$$. The probability of drawing each particle is given by its importance weight. Re-sampling transforms a particle set into another particle set of the same size. By incorporating the importance weights into the re-sampling process, the distribution of the particles change.

The re-sampling step is a probabilistic implementation of the Darwinian idea of _survival of the fittest_. It refocuses the particle set to region in state space with high posterior probability. By doing so, it focuses the computational resources of the filter algorithm to regions in the state space where they matter the most. 

```python
samples = []
for i in range(N):
    samples.append(Particle())

# update particles
for i in range(N):
    samples[i] = samples[i].move(0.1, 5)
    samples[i].set_noise(0.05, 0.05, 5.0)

# calcualte weights
weights = []
for i in range(N):
    weights.append(samples[i].importance_weight(measurements))

weights = np.array(weights)
weights = weights/np.sum(weights)

resamples = []
for i in range(N):
    resamples.append(np.random.choice(samples, p=weights))
```

## Mathematical Derivation

Think of particles as samples of state sequences. One sequence can be described as follows.

$$
x_{0:t}^m = x_0^m, x_1^m , ..., x_t^m
$$

Particle filter calculates the posterior over all state sequences.

$$
bel(x_{0:t}) = p(x_{0:t} \mid u_{1:t}, z_{1:t})
$$

> Notice that only state has value at $$t=0$$ because first control action and measurement data are applied at $$t = 1$$.

Using the same technique from Bayes' filter derivation.

$$
p(x_{0:t} \mid z_{1:t}, u_{1:t}) = \eta\;p(z_t \mid x_{0:t}, z_{1,t-1}, u_{1:t}) \; p(x_{0:t} \mid z_{1, t-1}, u_{1:t})
$$

Apply Markov assumption, that $$x_t$$ is complete and no variables prior to $$x_t$$ may influence the stochastic evolution of future states. \(not yet completed\)

$$
\text{Markov} \to  \eta\;p(z_t \mid x_{t}) \; p(x_{0:t} \mid z_{1, t-1}, u_{1:t}) \\ = \eta\; p(z_t \mid x_t)\; p(x_t \mid x_{0:t-1}, z_{1:t-1}, u_{1:t})\; p(x_{0:t-1} \mid z_{1:t-1}, u_{1:t}) \\= \eta\; p(z_t \mid x_t) \; p(x_t \mid x_{t-1}, u_t) \; p(x_{0:t-1} \mid z_{1:t-1}, u_{1:t-1})
$$





