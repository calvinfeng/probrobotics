# Extended Kalman Filter

The problem with standard Kalman filter is that it assumes linear state transitions and measurements. In reality, state transitions and measurements are rarely linear, e.g. a robot that moves with constant transnational and rotational velocity will move in a circular path, which is not linear. The _extended Kalman filter_ relaxes the linearity assumption.

We suppose that state transition probability and measurement probability are governed by nonlinear functions. 

$$
x_{t} = g(u_{t}, x_{t-1}) + \epsilon_{t} \\\;\\
z_{t} = h(x_{t}) + \delta_{t}
$$

The function $$g$$replaces the matrices $$A_{t}$$ and $$B_{t}$$, and the function $$h$$ replaces the matrix $$C_{t}$$. Unfortunately, with arbitrary non-linear functions, the belief is no longer a Gaussian. In fact, performing the belief update exactly is usually impossible in this case. The EKF \(extended Kalman filter\) needs to calculate a Gaussian approximation to the true belief via Monte Carlo methods. 

The key idea underlying the EKF approximation is called **linearization**.  If we were to use Monte Carlo methods, we'd have to pass hundred thousands of points to $$g$$followed by the computation of their mean and covariance. This is extremely inefficient. We need a way to hack around it and approximates $$g$$ and $$h$$ as linear functions using first order Taylor expansion. 

