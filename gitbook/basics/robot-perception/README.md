# Robot Perception

Environment measurement models comprise the second domain-specific model in probabilistic robotics, next to motion models. Measurement models describe the formation process by which sensor measurements are generated in the physical world. They explicitly model the noise in sensor measurements. Such models account for the inherent uncertainty in robot's sensors. 

Formally, the measurement model is defined as a conditional probability distribution $$p(z_t, \mid x_t, m)$$ where $$x_t$$ is the robot pose, $$z_t$$ is the measurement at time $$t$$, and $$m$$ is the map of the environment.

Probabilistic robotics accommodates inaccuracies of sensor models in the stochastic aspects. By modeling the measurement process as a conditional probability density, $$p(z_t \mid x_t)$$ instead of a deterministic function $$z_t = f(x_t)$$, the uncertainty in the sensor model can be accommodated in the non-deterministic aspects of the model.

Many sensors generate more than one numerical measurement value when queried. For example, cameras generate entire arrays of values like brightness, saturation, color and etc... We will denote the number of such measurement values within a measurement $$z_t$$ by $$K$$.

$$
z_t = \{ z_t^1, z_t^2, ... z_t^K\}
$$

We will use $$z_t^k$$ to refer to an individual measurement. The probability $$p(z_t \mid x_t, m)$$ is obtained as follows.

$$
p(z_t \mid x_t, m) = \prod_{k =1}^{K} p(z_t^k \mid x_t, m)
$$

Technically, this amounts to an _independence assumption_ between the noise in each individual measurement beam, just as our Markov assumption assumes independent noise over time. But in reality, this is not true, if a single measurement fails, it is likely that multiple other measurements will also fail due to some underlying hardware issue. 

To express the the process of generating measurements, we need to specify the environment in which a measurement is generated. A _map_ of the environment is a list of objects in the environment and their locations. Formally, a map is a list of objects in the environment with their properties. 

$$
m = \{ m_1, m_2, ..., m_N \}
$$

$$N$$ is the total number of objects in the environment, and each $$m_n$$ specifies a property. Maps are usually indexed in one of the two ways, known as _feature based_ and _location based_. In feature based maps, $$n$$ is a feature index. The value of $$m_n$$ contains the Cartesian location of the feature. In location based maps, the index $$n$$ corresponds to a specific location. In planar maps, it is common to denote a map element by $$m_{x, y}$$ instead of $$m_n$$.

