from numpy import array, dot, identity, linalg


# State transition matrix A, acting on state
A = array([
    [1.0, 1.0],
    [0.0, 1.0]
])


# Control input matrix B, acting on control (set to identity matrix)
B = array([
    [1.0, 0.0],
    [0.0, 1.0]
])


# Measurement probability matrix
C = array([
    [1, 0]
])


def predict_new_belief(x, x_cov, u, u_cov):
    """
    u_cov is the control or process noise
    """
    x = dot(A, x) + dot(B, u)
    x_cov = dot(dot(A, x_cov), A.T) + u_cov
    return x, x_cov


def incorporate_measurement(x, x_cov, z, z_cov):
    S = dot(dot(C, x_cov), C.T) + z_cov
    K = dot(dot(x_cov, C.T), linalg.inv(S))

    x = x + dot(K, z - C.dot(x))
    x_cov = dot(identity(2) - dot(K, C), x_cov)
    return x, x_cov


def kalman_filter(x, x_cov, U, u_cov, Z, z_cov):
    """Performs Kalman filter algorithm

    Args:
        x (np.array): Mean value of initial state
        x_cov (np.array): Coariance of initial state
        U (list[np.array]): List of controls
        u_cov (np.array): Covariance of control
        Z (list[np.array]): List of measurements
        z_cov (np.array): Coariance of measurement

    Returns:
        float: predicted mean of current state
        float: predicted variance of current state
    """
    if len(Z) != len(U):
        raise ValueError("measurements and controls are not same length")

    for i in range(len(U)):
        x, x_cov = predict_new_belief(x, x_cov, U[i], u_cov)
        x, x_cov = incorporate_measurement(x, x_cov, Z[i], z_cov)

    return x, x_cov


x = array([
    [0],
    [0],
])

x_cov = array([
    [1000.0, 0.0],
    [0.0, 1000.0],
])

# No external control command
U = array([
    [[0], [0]],
    [[0], [0]],
    [[0], [0]],
])

# u_cov is usually denoted as R which represents the control covariance/uncertainty
u_cov = array([
    [0.0, 0.0],
    [0.0, 0.0],
])

# Mesaurement is 1, 2, 3
Z = array([  
    [[1]],
    [[2]],
    [[3]],
])

# z_cov is usually denoted as Q which represents the measurement covariance/uncertainty
z_cov = array([
    [1],
])

mean, cov = kalman_filter(x, x_cov, U, u_cov, Z, z_cov)
print('mean\n', mean)
print('cov\n', cov)
