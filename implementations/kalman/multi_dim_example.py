import numpy as np

# State transition matrix A, acting on state
A = np.array([
    [1.0, 1.0],
    [0.0, 1.0]
])

# Control input matrix B, acting on control (set to identity matrix)
B = np.array([
    [1.0, 0.0],
    [0.0, 1.0]
])

# Measurement probability matrix
C = np.array([
    [1, 0]
])


def update(x, x_cov, u, u_cov):
    """
    u_cov is the control or process noise
    """
    mean = np.dot(A, x) + np.dot(B, u)
    cov = np.dot(np.dot(A, x_cov), A.T) + u_cov
    return mean, cov


def predict(x, x_cov, z, z_cov):
    K = np.dot(x_cov, C.T) / (np.dot(np.dot(C, x_cov), C.T) + z_cov)
    mean = x + K * (z - C.dot(x))
    i = np.identity(C.shape[0])
    cov = (i - K.dot(C)).dot(x_cov)
    return mean, cov


def kalman_filter(x, Z, U, x_cov, z_cov, u_cov):
    """Performs Kalman filter algorithm

    Args:
        x (float): Mean value of initial state
        Z (float[]): List of measurements
        U (float[]): List of controls
        x_cov (float): Coariance of initial state
        z_cov (float): Coariance of measurement
        u_cov (float): Covariance of control

    Returns:
        float: predicted mean of current state
        float: predicted variance of current state
    """
    if len(Z) != len(U):
        raise ValueError("measurements and controls are not same length")

    for i in range(len(U)):
        x, x_cov = update(x, x_cov, U[i], u_cov)
        x, x_cov = predict(x, x_cov, Z[i], z_cov)

    return x, x_cov


x = np.array([
    [0],
    [0],
])

x_cov = np.array([
    [1000.0, 0.0],
    [0.0, 1000.0],
])

U = [
    np.array([[0], [0]]),
    np.array([[0], [0]]),
    np.array([[0], [0]]),
]


u_cov = np.array([
    [0.0, 0.0],
    [0.0, 0.0],
])

# Mesaurement is 1, 2, 3
Z = [
    np.array([[1]]),
    np.array([[2]]),
    np.array([[3]]),
]

z_cov = np.array([
    [1],
])

mean, cov = kalman_filter(x, Z, U, x_cov, z_cov, u_cov)
print('mean', mean)
print('cov', cov)
