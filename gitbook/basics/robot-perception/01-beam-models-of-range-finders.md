# Beam Models of Range Finders

Ranger finders measure the range to nearby objects. Range may be measured along a beam, which is a good model of the workings of laser range finders, or within a cone, which is the preferable model of ultrasonic sensors.

## Measurement Algorithm

Our model incorporates four types of measurement errors, all of which are essential to making this model work. 

1. Small measurement noise
2. Errors due to unexpected objects
3. Errors due to failures to detect objects
4. Random unexplained noise

The desired model $$p(z_t \mid x_t, m)$$is a mixture of four densities, each of which corresponds to a particular type of error.

### 1. Correct range with local measurement noise

Let us use $$z_t^{k*}$$ to denote the true range of the object measured by $$z_t^{k}$$. In location-based maps, the true range can be determined using ray casting. In feature-based maps, it is usually obtained by searching for the closest feature within a measurement cone.  The measurement noise is usually modeled by a Gaussian with mean $$z_t^{k*}$$and standard deviation $$\sigma_{hit}$$.  We will denote the Gaussian by $$p_{hit}$$. 

The values measured by range sensor are limited to the interval $$[0, z_{max}]$$, where $$z_{max}$$ denotes the maximum sensor range. The measurement probability within the sensor range is given by the following.

$$
p_{hit}(z_t^k \mid x_t, m) = \eta\; N(z_t^k, \text{mean}=z_t^{k*}, \text{std} = \sigma_{hit}^2)
$$

For measurements outside of the sensor range, we can simply write,

$$
p_{hit}( z_t^k \mid x_t, m) = 0
$$

The true value is calculated from $$x_t$$ and $$m$$ via ray casting. The function $$N$$ denotes the uni-variate normal distribution. The normalizer is evaluated to the following.

$$
\eta^{-1} = \int_0^{z_{max}} N(z_t^k, \text{mean} = z_t^{k*}, \text{std} = \sigma^2_{hit}) \; dz_t^k
$$

The standard deviation is an intrinsic noise parameter of the measurement model. This varies from device to device.

### 2. Unexpected objects

Environments of mobile robots are dynamic, where as maps are static. As a result, objects not contained in the map can cause range finders to produce surprisingly short ranges. One way to deal with such objects is to treat them as part of the state vector and estimate their location. Another much simpler approach is to treat them as sensor noise. The object is that closer to the sensor is more likely to measure than the object that is further away. We can describe this situation with an exponential distribution.

$$
p_{short}(z_t^k \mid x_t, m) = \eta \; \lambda_{short}e^{-\lambda_{short}z_t^k}
$$

Again, if the measurement is out of range, we can simply write,

$$
p_{short}(z_t^k \mid x, m) = 0
$$

If we take the integral and we will find the normalizer is given by the following.

$$
\eta = \frac{1}{1 - e^{-\lambda_{short} z_t^{k*}}}
$$

### 3. Failures

Sometimes, obstacles are missed altogether. A typical result of sensor failure is a max-range measurement. The sensor returns its maximum allowable value $$z_{max}$$ because there is material that absorbs laser light beams. We will model this failure with a point-mass distribution centered at $$z_{max}$$.

$$
p_{max}(z_t^k \mid x_t, m) = 1 \;\text{if}\; z = z_{max}
$$

Technically, $$p_{max}$$ does not possess a probability density function. It seems more like a Dirac-Delta function.

#### 4. Random measurements

Finally, range finders occasionally produce entirely unexplainable measurements. Keep things simple, we will use a uniform distribution spread over the entire sensor measurement range.

$$
p_{rand}(z_t^k \mid x_t, m) = \frac{1}{z_{max}}
$$

## Beam Model Algorithm

These four different distributions are now mixed by a weighted average, defined by the parameters $$z_{hit}$$, $$z_{short}$$, $$z_{max}$$, and $$z_{rand}$$. 

$$
z_{hit} + z_{short} + z_{max} + z_{rand} = 1
$$

$$
p(z_t^k \mid x_t, m) = \begin{vmatrix}
z_{hit} \\ z_{short} \\ z_{max} \\ z_{rand}
\end{vmatrix}^{-1} \begin{vmatrix}
p_{hit}(z_t^k \mid x_t, m) \\ 
p_{short}(z_t^k \mid x_t, m) \\ 
p_{max}(z_t^k \mid x_t, m) \\ 
p_{rand}(z_t^k \mid x_t, m)
\end{vmatrix}
$$

The resulting density is a linear combination of the four different error density. The algorithm will be implemented as follows.

```text
q = 1
for k = 1 to K:
    compute true_z[t][k] for measurement z[t][k] using ray casting
    p = z_hit * p_hit + z_short * p_short + z_max * p_max + z_rand * p_rand
    q = q * p

return q
```

### Adjusting Parameters

We have a set of parameters, the four mixing parameters

$$
\{ z_{hit}, z_{short}, z_{max}, z_{rand} \}
$$

and the other two parameters.

$$
\{ \sigma_{hit}^2, \lambda_{short}\}
$$

We will refer the whole set as $$\Theta$$. We will learn these parameters from actual data. This is achieved by maximizing the likelihood of a reference data set $$Z = \{ z_i \}$$ with associated positions $$X = \{ x_i \}$$ and map $$m$$, where each $$z_i$$ is an actual measurement, $$x_i$$ is the pose at which the measurement was taken. The likelihood of data is given by the following. 

$$
p(Z \mid X, m, \Theta)
$$

Our goal is to identify intrinsic parameters that maximize this likelihood. 

```text
until convergence:
    for i, z in Z:
        norm = p_hit(z) + p_short(z) + p_max(z) + p_rand(z)
        norm = 1/norm
        calculate true_z
        e_hit[i] = norm * p_hit(z)
        e_short[i] = norm * p_short(z)
        e_max[i] = norm * p_max(z)
        e_rand[i] = norm * p_rand(z)
    
    z_hit = norm(Z)^-1 * sum(e_hit)
    z_short = norm(Z)^-1 * sum(e_short)
    z_max = norm(Z)^-1 * sum(e_max)
    z_rand = norm(Z)^-1 * sum(e_rand)
    
    sigma = compute_sigma(e_hit, Z, true_Z)
    lambda = compute_lambda(e_short, Z)
```

The $$\sigma_{hit}$$ computation can be described as follows.

$$
\sigma_{hit} = \sqrt{\frac
{\sum_i e_{i, hit}(z_i - z_i^*)^2}
{\sum_i e_{i, hit}}
}
$$

The $$\lambda_{short}$$ computation can be described as follows.

$$
\lambda_{short} = \frac{\sum_i e_{i, short}}{\sum_i e_{i, short} z_i}
$$

