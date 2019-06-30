# Monte Carlo Localization

## Algorithm

MCL \(_Monte Carlo Localization_\) is applicable to both local and global localization problem. It represents the belief $$bel(x_t)$$by particles.  The algorithm itself is basically a small modification of the previous particle filter algorithm we have discussed.

$$
\overline{\chi}_t = \chi_t = \emptyset
$$

$$
\text{for $m=1$ to $M$ do:} \\ x^m_t = \text{sample\_motion\_model}(u_t, x^m_{t-1}) \\
w^m_t = \text{measurement\_model}(z_t, x_t^m, m) \\
\overline{\chi}_t = \overline{\chi}_t + \langle x^m_t, w^m_t\rangle \\
\text{endfor}
$$

$$
\text{for $m=1$ to $M$ do:} \\
\text{draw $i$ with probability} \propto w^i_t \\
\text{add $x^i_t$ to $\chi_t$} \\
\text{endfor} \\\;\\
\text{return $\chi_t$}
$$

The algorithm is obtained by substituting the appropriate probabilistic model and perceptual model into the particle filter algorithm. MCL represents the belief by a set of $$M$$ particles where $$\chi_t = \{ x^1_t, x^2_t, ..., x^M_t\}$$. The motion model takes a control command and produces a new state. The measurement model assigns importance weight to the particle based on the likelihood of measurement given the new predicted state and map environments, i.e. the landmarks. The two motion and measurement models can be implemented by any motion/measurement models described in **Robot Perception** section.

## Properties

MCL can approximate almost any distribution of practical importance. Increasing the total number of particles increases the accuracy of the approximation. The number of particles $$M$$ is a parameter that enables the user to trade off the accuracy of the computation and the computational resources necessary to run MCL. A common strategy for setting $$M$$ is to keep sampling until the next pair of $$u_t$$ and $$z_t$$ has arrived.

## Random Particle Augmented MCL

MCL, in its present form, solves the global localization problem but cannot recover from robot kidnapping p failures. We can solve this problem by introducing random particles to the set on every iteration. The question is how many random particles to add and when to add?

 One idea is to add particle based on some estimate of the localization performance. We need to monitor the probability of sensor measurements.

$$
p(z_t \mid z_{1:t-1}, u_{1:t}, m)
$$

And relate it to the average measurement probability. By definition, an importance weight is a stochastic estimate of this probability. The average value approximates the desired probability as stated above.

$$
\frac{1}{M}\sum_{m=1}^{M} w^m_t \approx p(z_t \mid z_{1:t-1}, u_{1:t}, m)
$$

There exist multiple reasons why the measurement probability may be low. The amount of sensor noise might be unnaturally high, or the particles may still be spread out during a global localization phase. For these reasons, it is a good idea to maintain a short-term average of the measurement likelihood, and relate it to the long-term average when determining the number of random samples.

$$
\text{static $\omega_{slow}$ $\omega_{fast}$} \\ 
\overline{\chi}_t = \chi_t = \emptyset \\\;\\
$$

$$
\text{for $m=1$ to $M$ do:} \\ x^m_t = \text{sample\_motion\_model}(u_t, x^m_{t-1}) \\
w^m_t = \text{measurement\_model}(z_t, x_t^m, m) \\
\overline{\chi}_t = \overline{\chi}_t + \langle x^m_t, w^m_t\rangle \\
\omega_{avg} = w_{avg} + \frac{w^m_t}{M} \\
\text{endfor}
$$

$$
\omega_{slow} = \omega_{slow} + \alpha_{slow}(\omega_{avg} - \omega_{slow}) \\
\omega_{fast} = \omega_{fast} + \alpha_{fast}(\omega_{avg} - \omega_{fast})
$$

$$
\text{for $m=1$ to $M$ do:} \\
\text{with probability $max\{0.0, 1.0 - \frac{\omega_{fast}}{\omega_{slow}}\}$: add random particle to set} \\
\text{ else: draw $i$ with probability} \propto w^i_t \\ 
\text{add $x^i_t$ to $\chi_t$} \\
\text{endfor} \\\;\\
\text{return $\chi_i$}
$$

The algorithm requires that $$0 \leq \alpha_{slow} \ll \alpha_{fast}$$. The parameters $$\alpha_{fast}$$ and $$\alpha_{slow}$$ are decay rates for the exponential filters that estimate the long-term and short-term averages respectively. During the re-sampling process, a random sample is added with the following probability.

$$
max\{ 0.0, 1.0 - \frac{\omega_{fast}}{\omega_{slow}}\}
$$

Otherwise, the re-sampling proceeds in the familiar way. The probability of adding a random sample takes into consideration the divergence between the short-term and long-term average of the measurement likelihood. If the short-term likelihood is better or equal to the long-term likelihood, no random sample is added. However, if the short-term likelihood is much worse than the long-term one, random samples are added in proportion to the quotient of these values. In this way, a sudden decay in measurement likelihood induces an increased number of random samples. 



