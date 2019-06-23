# Particle Filter

The particle filter is just like histogram filter, it approximate the posterior by a finite number of parameters. However, they differ in the way these parameters are generated, and in which they populate the state space. The key idea of the particle filter is to represent the posterior $$bel(x_t)$$by a set of random state samples drawn from this posterior. Such representation is approximate, but it is non-parametric, and therefore can represent a much broader space of distributions than, for example, Gaussian. Another advantage of the sample based representation is its ability to model nonlinear transformations of random variables.

In particle filter, the samples of a posterior distribution are called _particles_. 

$$
\chi_t = x_t^1, x_t^2, ..., x_t^M
$$

Each particle $$x_t^m$$ is a concrete instantiation of the state at time $$t$$. In other words, a particle is a hypothesis as to what the true world state may be at time $$t$$. Here $$M$$ denotes the number of particles in the particle set $$\chi_t$$. 

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

#### Details

1. We generate a hypothetical state $$x_t^m$$based on the particle from previous time step and the control at current time step.The set of particles obtained from the first for loop is filter's representation of $$\overline{bel}(x_t)$$.
2. The $$w$$ is known as the importance factor or particle scores. Importance factors are used to incorporate measurements. The importance is the probability of the measurement $$z_t$$ under the particle $$x_t^m$$.
3. The real trick occurs here which is the re-sampling portion. The algorithm draws with replacement $$M$$ particles from the temporary set $$\overline{\chi}_t$$. The probability of drawing each particle is given by its importance weight. Re-sampling transforms a particle set into another particle set of the same size. By incorporating the importance weights into the re-sampling process, the distribution of the particles change.

The re-sampling step is a probabilistic implementation of the Darwinian idea of _survival of the fittest_. It refocuses the particle set to region in state space with high posterior probability. By doing so, it focuses the computational resources of the filter algorithm to regions in the state space where they matter the most. 





