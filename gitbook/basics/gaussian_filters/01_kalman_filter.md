# Kalman Filter

### Linear Gaussian Systems

The Kalman filter implements belief computational for continuous state. It is not applicable to discrete or hybrid state spaces. The filter represents belief by moments parameterization. At time $$t$$, the belief is represented by the mean $$\mu_{t}$$ and the covariance $$\Sigma_{t}$$. Posteriors are Gaussian if the following three properties hold in addition to Markov assumption. 

#### 1. Linear Transition

The state transition probability $$p(x_{t} \mid u_{t}, x_{t-1})$$ must be a linear function in its arguments with added Gaussian noises.

$$
\tag{1} x_{t} = A_{t}x_{t-1} + B_{t}u_{t} + \epsilon_{t}
$$

The state and control are vectors. In our notation, they are vertical vectors.

$$
x_{t} = \begin{vmatrix}
x_{t}[0] \\ x_{t}[1] \\ x_{t}[2] \\ ... \\ x_{t}[n-1]  
\end{vmatrix}
\quad
u_{t} = \begin{vmatrix}
u_{t}[0] \\ u_{t}[1] \\ u_{t}[2] \\ ... \\ u_{t}[m-1]  
\end{vmatrix}
$$

Here $$A_{t}$$ and $$B_{t}$$ are matrices. $$A_{t}$$ is of size n by n and $$B_{t}$$ is of size n by m. The dimension of state vector is n and the dimension of control vector is m. The random variable $$\epsilon_{t}$$ has the same dimension as the state vector. Its mean is zero and its covariance will be denoted as $$R_{t}$$. It is there to modifies the uncertainty introduced by the state transition. The mean of the posterior state is given by equation 1 and covariance by $$R_{t}$$.

$$
p(x_{t} \mid u_{t}, x_{t-1}) = det(2\pi R_{t})^{-0.5} \; \exp\left[
\frac{-1}{2} (x_{t} - A_{t}x_{t-1} - B_{t}u_{t})^{T} R_{t}^{-1} (x_{t} - A_{t}x_{t-1} - B_{t}u_{t})
\right]
$$

#### 2. Linear Measurement

The measurement probability $$p(z_{t} \mid x_{t})$$ must also be linear with added Gaussian noise.

$$
\tag{2} z_{t} = C_{t}x_{t} + \delta_{t}
$$

Here $$C_{t}$$is a matrix of size k by n where k is the dimension of the measurement vector. The $$\delta$$ describes the measurement noise. The distribution of noise is a multivariate Gaussian with zero mean and covariance of $$Q_{t}$$. 

$$
p(z_{t}\mid x_{t}) = det(2\pi Q_{t})^{-0.5} \exp
\left[
\frac{-1}{2}(z_{t} - C_{t}x_{t})^{T}Q_{t}^{-1}
(z_{t} - C_{t}x_{t})
\right]
$$

#### 3. Normal Belief

The initial belief $$bel(x_{0})$$ must be normally distributed with mean $$\mu_{0}$$ and covariance $$\Sigma_{0}$$.

$$
bel(x_{0})= p(x_{0}) = det(2\pi\Sigma_{0})^{-0.5} \exp\left[
\frac{-1}{2}(x_{0} - \mu_{0})^{T} \Sigma_{0}^{T} (x_{0} - \mu_{0})
\right]
$$

### Kalman Filter Algorithm

Given arguments $$\mu_{t-1}$$, $$\Sigma_{t-1}$$, $$u_{t}$$, and $$z_{t}$$, we have the following update rules.

$$
\tag{3a} \overline{\mu_{t}} = A_{t}\mu_{t-1} + B_{t}u_{t} \\
\overline{\Sigma_{t}} = A_{t}\Sigma_{t-1}A_{t-1}^{T} + R_{t}
$$

The predicted belief $$\overline{\mu_{t}}$$ and $$\overline{\Sigma_{t}}$$ are calculated to represent the belief $$\overline{bel}(x_{t})$$, one time step later, but before incorporating the measurement $$z_{t}$$.

$$
\tag{3b} K_{t} = \frac{\overline{\Sigma}_{t} C_{t}^{T} }{C_{t}\overline{\Sigma}C_{t}^{T} + Q_{T}}
$$

Before we perform the measurement update, we need to compute Kalman gain from equation 3b, which specifies the degree to which the measurement is incorporated into the new state estimate. Then we use the gain to get the new state.

$$
\tag{3c} \mu_{t} = \overline{\mu_{t}} + K_{t}(z_{t} - C_{t}\overline{\mu_{t}}) \\
\Sigma_{t} = (I - K_{t}C_{t})\overline{\Sigma_{t}}
$$

The key concept here is innovation, which is the difference between the actual measurement and expected measurement, denoted by $$z_{t} - C_{t}\overline{\mu_{t}}$$ .

