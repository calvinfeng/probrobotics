# Basic Concepts in Probability

Let $$X$$ denotes a random variable, then $$x$$ is a specific value that $$X$$ might assume.

$$
p(X = x) \;\text{denotes the probability of $X$ has the value of $x$}
$$

Therefore,

$$
\sum_{x} p\,(X = x) = 1
$$

All continuous random variables possess probability density function, **PDF**.

$$
p\,(x) = (2\pi\sigma^{2})^{-1/2} \exp{\frac{-1}{2}\frac{(x - \mu)^{2}}{\sigma^{2}}}
$$

We can abbreviate the equation as follows, because it is a normal distribution.

$$
N(x; \mu; \sigma^{2})
$$

However, in general, $$x$$ is not a scalar value, it is generally a vector. Let $$\Sigma$$ be a positive semi-definite and symmetric matrix, which is a **covariance matrix**.

$$
p\,(x) = det(2\pi\Sigma)^{-1/2} \exp{ \frac{-1}{2} (\vec{x} - \vec{\mu})^{T} \Sigma^{-1} (\vec{x} - \vec{\mu})}
$$

and

$$
\int p\,(x)\,dx = 1
$$

The joint distribution of two random variables $$X$$ and $$Y$$ can be described as follows.

$$
p\,(x, y) = p\,(\text{$X = x$ and $Y = y$})
$$

If they are independent, then

$$
p\,(x,y) = p(x)p(y)
$$

If they are conditioned, then

$$
p\,(x \mid y) = p\,(X=x \mid Y=y)
$$

If $$p(y) > 0$$, then

$$
p\,(x \mid y) = \frac{p\,(x, y)}{p(y)}
$$

**Theorem of Total Probability** states the following.

$$
p\,(x) = \sum_{y} p\,(x \mid y)p(y) = \int p\,(x \mid y)p(y)dy
$$

We can apply **Bayes Rule**.

$$
p\,(x \mid y) = \frac{ p\,(y \mid x) p(x) }{ p(y) } = \frac{ p\,(y \mid x) p(x) } { \sum_{x`} p\,(y \mid x`) p(x`)}
$$

In integral form,

$$
\frac{ p\,(y \mid x) p(x) } { \int p\,(y \mid x`) p(x`) dx`}
$$

If $$x$$ is a quantity that we would like to inrefer from $$y$$, the probability $$p(x)$$ is referred as **prior probabilitydistribution** and $$y$$ is called data, e.g. laser measurements. $$p(x \mid y)$$ is called **posterior probability distribution** over $$X$$.

In robotics, $$p(y \mid x)$$ is called **generative model**. Since $$p(y)$$ does not depend on $$x$$, $$p(y)^{-1}$$ is often written as a normalizer in Bayes rule variables.

$$
p\,(x \mid y) = \eta p\,(y \mid x) p(x)
$$

It is perfectly fine to to condition any of the rules on arbitrary random variables, e.g. the location of a robot can inferred from multiple sources of random measurements.

$$
p\,(x \mid y, z) = \frac{ p\,(x \mid x, z) p\,(y \mid z) }{ p\,(y \mid z) }
$$

for as long as $$p\,(y \mid z) > 0$$.

Similarly, we can condition the rule for combining probabilities of independent random variables on other variables.

$$
p\,(x, y \mid z) = p\,(x \mid z)p\,(y \mid z)
$$

However, conditional independence does not imply absolute independence, that is

$$
p\,(x, y \mid z) = p\,(x \mid z)p\,(y \mid z) \neq p(x,y) = p(x)p(y)
$$

The converse is neither true, absolute independence does not imply conditional independence.

The expected value of a random variable is given by

$$
E[X] = \sum_{x} x p(x) = \int x p(x) dx
$$

Expectation is a linear function of a random variable, we have the following property.

$$
E[aX + b] = aE[X] + b
$$

Covariance measures the squared expected deviation from the mean. Therefore, square root of covariance is in fact variance, i.e. the expected deviation from the mean.

$$
Cov[X] = E[X - E[X]^{2} = E[X^{2}] - E[X]^2
$$

Finally, **entropy** of a probability distribution is given by the following expression. Entropy is the expected information that the value of $$x$$ carries.

$$
H_{p}(x) = -\sum_{x} p(x) log_{2}p(x) = -\int p(x) log_{2} p(x) dx
$$

In the discrete case, the $$-log_{2}p(x)$$ is the number of bits required to encode x using an optimal encoding, assuming that $$p(x)$$ is the probability of observing $$x$$ .

**Theorem of Total Probability** states the following.

$$
p(x) = \sum_{y} p(x \mid y)p(y) = \int p(x \mid y)p(y)dy
$$

We can apply **Bayes Rule**.

$$
p(x \mid y) = \frac{ p(y \mid x) p(x) }{ p(y) } = \frac{ p(y \mid x) p(x) } { \sum_{x`} p(y \mid x`) p(x`)}
$$

In integral form,

$$
\frac{ p(y \mid x) p(x) } { \int p(y \mid x`) p(x`) dx`}
$$

If $$x$$ is a quantity that we would like to infer from $$y$$, the probability $$p(x)$$ is referred as **prior probability distribution** and $$y$$ is called data, e.g. laser measurements. $$p(x \mid y)$$ is called **posterior probability distribution** over $$X$$.

In robotics, $$p(y \mid x)$$ is called **generative model**. Since $$p(y)$$ does not depend on $$x$$, $$p(y)^{-1}$$ is often written as a normalizer in Bayes rule variables.

$$
p\,(x \mid y) = \eta p(y \mid x) p(x)
$$

It is perfectly fine to to condition any of the rules on arbitrary random variables, e.g. the location of a robot can inferred from multiple sources of random measurements.

$$
p\,(x \mid y, z) = \frac{ p(x \mid x, z) p(y \mid z) }{ p(y \mid z) }
$$

for as long as $$p\,(y \mid z) > 0$$.

Similarly, we can condition the rule for combining probabilities of independent random variables on other variables.

$$
p\,(x, y \mid z) = p(x \mid z)p(y \mid z)
$$

However, conditional independence does not imply absolute indenpendence, that is

$$
p\,(x, y \mid z) = p(x \mid z)p(y \mid z) \neq p(x,y) = p(x)p(y)
$$

The converse is neither true, absolute independence does not imply conditional independence.

The expected value of a random variable is given by

$$
E[X] = \sum_{x} x p(x) = \int x p(x) dx
$$

Expectation is a linear function of a random variable, we have the following property.

$$
E[aX + b] = aE[X] + b
$$

Covariance measures the squared expected deviation from the mean. Therefore, square root of covariance is in fact variance, i.e. the expected deviation from the mean.

$$
Cov[X] = E[X - E[X]^{2} = E[X^{2}] - E[X]^2
$$

Finally, **entropy** of a probability distribution is given by the following expression. Entropy is the expected information that the value of $$x$$ carries.

$$
H_{p}(x) = -\sum_{x} p(x) log_{2}p(x) = -\int p(x) log_{2} p(x) dx
$$

In the discrete case, the $$-log_{2}p(x)$$ is the number of bits required to encode x using an optimal encoding, assuming that $$p(x)$$ is the probability of observing $$x$$.

