# Extended Kalman Filter

The problem with standard Kalman filter is that it assumes linear state transitions and measurements. In reality, state transitions and measurements are rarely linear, e.g. a robot that moves with constant transnational and rotational velocity will move in a circular path, which is not linear. The _extended Kalman filter_ relaxes the linearity assumption.

We suppose that state transition probability and measurement probability are governed by nonlinear functions. 

$$
x_{t} = g(u_{t}, x_{t-1}) + \epsilon_{t} \\\;\\
z_{t} = h(x_{t}) + \delta_{t}
$$

The function $$g$$replaces the matrices $$A_{t}$$ and $$B_{t}$$, and the function $$h$$ replaces the matrix $$C_{t}$$. Unfortunately, with arbitrary non-linear functions, the belief is no longer a Gaussian. In fact, performing the belief update exactly is usually impossible in this case. The EKF \(extended Kalman filter\) needs to calculate a Gaussian approximation to the true belief via Monte Carlo methods. 

## Linearization

The key idea underlying the EKF approximation is called **linearization**.  If we were to use Monte Carlo methods, we'd have to pass hundred thousands of points to $$g$$followed by the computation of their mean and covariance. This is extremely inefficient. We need a way to hack around it and approximates $$g$$ and $$h$$ as linear functions using first order Taylor expansion. 

### Taylor Expansion

Taylor expansion constructs a linear approximation to a function $$g$$ from $$g$$'s value and slope. The slope is given by the following expression.

$$
g\prime(u_{t}, x_{t-1}) = \frac{\partial g}{\partial x_{t-1}}
$$

The value and slope of $$g$$are dependent on the arguments $$u_{t}$$ and $$x_{t-1}$$. We should choose the most probable states to perform Taylor expansion with. Since the most probable state of $$X_{t}$$ is $$\mu_{t-1}$$, $$g$$ is approximated by its values at $$\mu_t{-1}$$ and $$u_{t}$$. 

$$
g(u_{t}, x_{t-1}) \approx g(u_{t}, \mu_{t-1}) + g\prime(u_{t}, \mu_{t-1})(x_{t-1} - \mu_{t-1}) = g(u_{t}, \mu_{t-1}) + G_{t}(x_{t-1} - \mu_{t-1})
$$

Notice that $$G_{t}$$ is a n by n matrix, with n denoting the dimension of the state. This matrix is often called the Jacobian. The value of Jacobian is dependent on $$u_{t}$$ and $$\mu_{t-1}$$, hence the matrix is time dependent. EKF implements the exact same linearization for the measurement function $$h$$. The calculation must perform after prediction state, hence $$\overline{\mu}_{t}$$.

$$
h(x_{t}) \approx h(\overline{\mu}_{t}) + h\prime(\overline{\mu}_{t})(x_{t} - \overline{\mu}_{t}) = h(\overline{\mu}_{t}) + H_{t}(x_{t} - \overline{\mu}_{t})
$$

## EKF Algorithm

Now if we put everything together, we have the EKF algorithm. Equation \(1\) performs the prediction steps.

$$
\tag{1} \overline{\mu}_{t} = g(u_{t}, \mu_{t-1}) \\\;\\
\overline{\Sigma}_{t} = G_{t}\Sigma_{t-1}G^{T}_{t} + R_{r}t
$$

Equation \(2\) performs the Kalman gain calculation.

$$
\tag{2} K_{t} = \overline{\Sigma}_{t}H_{t}^{T}(H_{t}\overline{\Sigma}H_{t}^{T} + Q_{t})^{-1}
$$

Equation \(3\) performs the measurement incorporation steps.

$$
\mu_{t} = \overline{\mu}_{t} + K_{t}(z_{t} - h(\overline{\mu}_{t})) \\\;\\
\Sigma_{t} = (I - K_{t}H_{t})\overline{\Sigma}_{t}
$$

Finally,

$$
\text{return}\;\mu_{t}, \Sigma_{t}
$$

