# Gaussian Filters

We are going to introduce an important family of recursive state estimators,
collectively called **Gaussian filters**. Gaussian techniques all share the
basic idea that beliefs are represented by multivariate normal distributions.

$$
p(x) = det(2\pi\Sigma)^{-0.5} \exp\left(\frac{-1}{2}(x-\mu)^{T}\Sigma^{-1}(x-\mu)\right)
$$

The density over the variable $$x$$ is characterized by two sets of parameters.
The mean $$\mu$$ and covariance matrix $$\Sigma$$. Gaussians are unimodal; they
possess a single maximum. This may be suitable for some problems but may not be
appropriate for problems that exist many distinct hypotheses. 

## Parameterization

The parameterization of a Gaussian by its mean and covariance is called the
_moments parametrization_. This is because the mean and covariance are the first
and second moments of a probability distribution. There is an alternative
parameterization called _canonical parameterization_ which will be discussed
later.
