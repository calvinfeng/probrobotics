# Likelihood Fields for Range Finders

### Limitations of Beam Models

The beam-based model exhibits a _lack of smoothness_. In cluttered environments with many small obstacles, the distribution of $$p(z_t^k \mid x_t, m)$$ can be very unsmooth in $$x_t$$. That means the measurement model is highly discontinuous which leads to two problematic consequences.

1. Any approximate belief representation runs the danger of missing the correct state, as nearby states might have drastically different posterior likelihoods. 
2. Hill-climbing methods for finding the most likely state are prone to local minima, due to the large number of local maxima in such unsmooth models. 

### Likelihood Fields

An alternative model to overcome above limitations is the use of likelihood fields. The resulting posteriors of likelihood field computation are much smoother even in cluttered space. The key idea is to first project the endpoints of a sensor scan $$z_t$$ into the global coordinate space of the map. 

Let $$x_t = \langle x, y, \theta \rangle^T$$ denote a robot pose at time $$t$$. Let $$\langle x_{k, sensed}, y_{k, sensed} \rangle$$ denote the relative location of the sensor in the robot's fixed local coordinate system. Let $$\theta_{k, sensed}$$ denote the angular orientation of the sensor beam relative to the robot's heading direction.

$$
\begin{vmatrix}
x_{z_t^k} \\ y_{z_t^k}
\end{vmatrix}   = 
\begin{vmatrix}
x \\ y 
\end{vmatrix} +
\begin{vmatrix}
\cos{\theta} & -\sin{\theta} \\
\sin{\theta} & \cos{\theta}
\end{vmatrix}
\begin{vmatrix}
x_{k, sensed} \\ y_{k, sensed}
\end{vmatrix} +
z_k^t \begin{vmatrix}
\cos{\theta + \theta_{k, sensed}} \\
\sin{\theta + \theta_{k, sensed}}
\end{vmatrix}
$$

If the range sensor takes on its maximum value, these coordinates have no meaning in the physical world. The likelihood field measurement model simply discards these readings.

### Measurement Noises

Noise arising from the measurement process is modeled using Gaussian. This involves finding the nearest obstacles in the map. Let $$dist$$ denote the Euclidean distance between the measurement coordinates $$(x_{z^k_t}, y_{z^k_t})^T$$ and the nearest object in the map $$m$$. Then the probability of a sensor measurement is given by the zero-centered Gaussian, which captures the sensor noise.

$$
p_{hit}(z^k_t \mid x_t, m) = \epsilon_{\sigma_{hit}}(dist)
$$

If the measurement is perfectly accurate, the variance will be zero and the probability of $$dist=0$$ will be 1, which is 100%. However, that never happens in practice.

### Failures

As before, we assume that the max-range readings have a distinct large likelihood. This is modeled by a point mass distribution. That means if we receive a max reading, we know for sure $$p_{max} = 1$$, that there is a reading failure.

### Unexplained Random Measurements

As like before, we will use a uniform distribution to describe $$p_{rand}$$. Regardless the reading, there is a uniform likelihood that there is a random error.

### Algorithm

Therefore, we can summarize the the model with the following algorithm.

$$
p(z^k_t \mid x_t, m) = z_{hit}p_{hit} + z_{rand}p_{rand} + z_{max}p_{max}
$$

$$
q = 1 \\\;\\
\text{for all $k$ do:} \\
\text{if $z^k_t \neq z_{max}$:} \\
x_{z^k_t} = x + x_{k, sensed}\cos{\theta} - y_{k, sensed} \sin{\theta} + z^k_t \cos{(\theta + \theta_{k, sensed})} \\
y_{z^k_t} = y + y_{k, sensed} \cos{\theta} + x_{k, sensed} \sin{\theta} + z^k_t \sin{(\theta + \theta_{k, sensed})} \\
dist = \min_{x^`, y^`} \sqrt{(x_{z^k_t} - x^`)^2 + (y_{z^k_t} - y^`)^2} \mid  x^`, y^` \text{occupied in map} \\
q = q * (z_{hit} * p_{hit}(dist, \sigma_{hit}) + \frac{z_{rand}}{z_{max}})
\\\;\\
\text{return $q$}
$$



###  

