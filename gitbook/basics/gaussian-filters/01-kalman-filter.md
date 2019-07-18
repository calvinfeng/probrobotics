# Kalman Filter

## Linear Gaussian Systems

The Kalman filter implements belief computational for continuous state. It is not applicable to discrete or hybrid state spaces. The filter represents belief by moments parameterization. At time $$t$$, the belief is represented by the mean $$\mu_{t}$$ and the covariance $$\Sigma_{t}$$. Posteriors are Gaussian if the following three properties hold in addition to Markov assumption. 

### 1. Linear Transition

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

### 2. Linear Measurement

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

### 3. Normal Belief

The initial belief $$bel(x_{0})$$ must be normally distributed with mean $$\mu_{0}$$ and covariance $$\Sigma_{0}$$.

$$
bel(x_{0})= p(x_{0}) = det(2\pi\Sigma_{0})^{-0.5} \exp\left[
\frac{-1}{2}(x_{0} - \mu_{0})^{T} \Sigma_{0}^{T} (x_{0} - \mu_{0})
\right]
$$

## Kalman Filter Algorithm

Given arguments $$\mu_{t-1}$$, $$\Sigma_{t-1}$$, $$u_{t}$$, and $$z_{t}$$, we have the following update rules.

$$
\tag{3a} \overline{\mu_{t}} = A_{t}\mu_{t-1} + B_{t}u_{t} \\\;\\
\overline{\Sigma_{t}} = A_{t}\Sigma_{t-1}A_{t-1}^{T} + R_{t}
$$

The predicted belief $$\overline{\mu_{t}}$$ and $$\overline{\Sigma_{t}}$$ are calculated to represent the belief $$\overline{bel}(x_{t})$$, one time step later, but before incorporating the measurement $$z_{t}$$.

$$
\tag{3b} K_{t} = \overline{\Sigma}_{t} C_{t}^{T} (C_{t}\overline{\Sigma}C_{t}^{T} + Q_{T})^{-1}
$$

Before we perform the measurement update, we need to compute Kalman gain from equation 3b, which specifies the degree to which the measurement is incorporated into the new state estimate. Then we use the gain to get the new state.

$$
\tag{3c} \mu_{t} = \overline{\mu_{t}} + K_{t}(z_{t} - C_{t}\overline{\mu_{t}}) \\\;\\
\Sigma_{t} = (I - K_{t}C_{t})\overline{\Sigma_{t}}
$$

The key concept here is innovation, which is the difference between the actual measurement and expected measurement, denoted by $$z_{t} - C_{t}\overline{\mu_{t}}$$ .

### Code Example

For simplicity sake, I will omit the time dependence for transformation matrices. Let's define three matrices `A`, `B`, and `C` using `numpy` . Note that `A` is the state transition model or function, `B` is the control input model, and `C` is the observation model. 

```python
A = np.array([[1.0, 1.0], [0.0, 1.0]])
B = np.array([[1.0, 0.0], [0.0, 1.0]])
C = np.array([[1.0, 0.0]])
```

If we were to express them in matrix form, they would look like the following.

$$
A = \begin{vmatrix}
1.0 & 1.0 \\ 0.0 & 1.0
\end{vmatrix}
\\\;\\
B = \begin{vmatrix}
1.0 & 0.0 \\ 0.0 & 1.0
\end{vmatrix}
\\\;\\
C = \begin{vmatrix}
1.0 & 0.0
\end{vmatrix}
$$

Suppose our robot is at coordinate $$(0.0, 0.0)$$ initially and we don't apply any external control to it. Let's denote `x` to be $$\mu$$, `x_cov` to be $$\Sigma$$, `u` to be $$u$$, and `u_cov` to be $$R$$.

```python
x = np.array([[0.0], [0.0]])
x_cov = np.array([[1000.0, 0.0], [0.0, 1000.0]])
u = np.array([[0.0], [0.0]])
u_cov = np.array([[0.0, 0.0], [0.0, 0.0]])
```

$$
\mu = \begin{vmatrix}
0 \\ 0
\end{vmatrix}
\;
\Sigma = \begin{vmatrix}
1000.0 & 0.0 \\ 0.0 & 1000.0
\end{vmatrix}
\\\;\\
u = \begin{vmatrix}
0.0 \\ 0.0
\end{vmatrix}\;
R = \begin{vmatrix}
0.0 & 0.0 \\ 0.0 & 0.0
\end{vmatrix}
$$

Let `Z` to be $$(z_{0}, z_{1}, z_{2}, ...)$$and `z_cov` to be $$Q$$.

```python
Z = [np.array([[1]]), np.array([[2]]), np.array([[3]])
z_cov = np.array([[1]])
```

$$
z_{0} = \begin{vmatrix} 1 \end{vmatrix} \; z_{1} = \begin{vmatrix} 2 \end{vmatrix} etc...\\\;\\
Q = \begin{vmatrix} 0 \end{vmatrix}
$$

Now we can put everything together and construct a Kalman filter algorithm.

```python
def predict_new_belief(x, x_cov, u, u_cov):
    x = dot(A, x) + dot(B, u)
    x_cov = dot(dot(A, x_cov), A.T) + u_cov
    return x, x_cov


def incorporate_measurement(x, x_cov, z, z_cov):
    S = dot(dot(C, x_cov), C.T) + z_cov
    K = dot(dot(x_cov, C.T), linalg.inv(S))

    x = x + dot(K, z - C.dot(x))
    x_cov = dot(identity(2) - dot(K, C), x_cov)
    return x, x_cov


for i in range(len(Z)):
    x, x_cov = predict_new_belief(x, x_cov, u, u_cov)
    x, x_cov = incorporate_measurement(x, x_cov, Z[i], z_cov)
```

