# Histogram Filter

Histogram filters decompose the state space into finitely many regions and represent the cumulative posterior for each region by a single probability value. When applied to finite spaces, they are called **discrete Bayes filters**; when applied to continuous spaces, they are known as **histogram filters**.

## Discrete Bayes Filter

We use discrete Bayes filter when the problem has finite state spaces, where random variable $$X_t$$ can take on finitely many values, like a door is open or closed. Let the variables $$x_i$$ and $$x_k$$ denote individual states, of which there may only be finitely many. The belief at time $$t$$ is an assignment of a probability to each state $$x_k$$, denoted $$p_{k, t}$$. 

$$
\tag{1} \text{for all $k$ do:}\\\;\\
\overline{p}_{k, t} = \sum_i p(X_t = x_k \mid u_t, X_{t-1} = x_i) p_{i, t-1} \\
p_{k, t} = \eta\; p(z_t \mid X_t = x_k)\overline{p}_{k, t} \\\;\\
\text{endfor and return $p_{k,t}$}
$$

The input to the algorithm is a discrete probability distribution $$p_{k, t}$$, along with the most recent control $$u_t$$ and measurement $$z_t$$. The first step is to calculate the prediction, the belief for the new state based on the control alone. The second step is to incorporate the measurement and update the new belief. This is exactly identical to the Bayes filter except that the integral has been replaced by a discrete sum.

## Histogram Filter

We want to use discrete Bayes filters as an approximate inference tool for continuous state spaces, this brings us to the histogram filter. Histogram filter decomposes a continuous state space into finitely many bins or regions.

$$
\text{dom}(X_t) = x_{1, t} \cup x_{2, t} \cup ... \cup x_{K, t}
$$

Here $$X_t$$ is the familiar random variable describing the state of the robot at time $$t$$. The function $$\text{dom}(X_t)$$ denotes the state space, which is the universe of possible values that $$X_t$$ might assume. A straightforward decomposition of a continuous state space is a multi-dimensional grid, where each $$x_{k,t}$$ is a grid cell. 

If the state is truly discrete, the conditional probabilities are well-defined, and the algorithm can be implemented as equation \(1\). In continuous state space, one is usually given the densities $$p(x_t \mid u_t, x_{t-1})$$ and $$p(z_t \mid x_t)$$ which are defined for individual states and not for the regions in the state space. We need to perform an approximation for the region by taking the mean state in $$x_{k, t}$$.

$$
\hat{x}_{k, t} = \frac{1}{\lvert x_{k,t}\rvert}\int_{x_{k,t}} x_t \;dt
$$

Now we have it.

$$
\tag{1} \text{for all $k$ do:}\\\;\\
\overline{p}_{k, t} = \sum_i \eta \; \lvert x_{k,t}\rvert \; p(\hat{x}_{k, t} \mid u_t, \hat{x}_{i, t-1}) p_{i, t-1} \\
p_{k, t} = \eta\; p(z_t \mid \hat{x}_{i, t-1})\overline{p}_{k, t} \\\;\\
\text{endfor and return $p_{k,t}$}
$$

## Decomposition Techniques

Decomposition techniques of continuous state spaces come in two basic flavors, _static_ and _dynamic_. State technique rely on a fixed decomposition that is chosen in advance. Dynamic technique adapt the decomposition to the specific shape of the posterior distribution. State techniques are usually easier to implement, but they can be wasteful with regards to computational resource.

