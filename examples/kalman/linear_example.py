def update(x_mean, x_var, z_mean, z_var):
    mean = (z_var*x_mean + x_var*z_mean) / (x_var + z_var)
    var = 1/(1/x_var + 1/z_var)
    return mean, var


def predict(x_mean, x_var, u_mean, u_var):
    mean = x_mean + u_mean
    var = x_var + u_var
    return mean, var


def kalman_filter(x, Z, U, x_var=1, z_var=1, u_var=1):
    """Performs Kalman filter algorithm

    Args:
        x (float): Mean value of initial state
        Z (float[]): List of measurements
        U (float[]): List of controls
        x_var (float): Variance of initial state
        z_var (float): Variance of measurement
        u_var (float): Variance of control

    Returns:
        float: predicted mean of current state
        float: predicted variance of current state
    """
    if len(Z) != len(U):
        raise ValueError("measurements and controls are not same length")

    for i in range(len(Z)):
        x, x_var = update(x, x_var, Z[i], z_var)
        x, x_var = predict(x, x_var, U[i], u_var)

    return x, x_var


if __name__ == '__main__':
    Z, z_var = [5, 6, 7, 9, 10], 4
    U, u_var = [1, 1, 2, 1, 1], 2
    x, x_var = 0, 1000
    print(kalman_filter(x, Z, U, x_var, z_var, u_var))
