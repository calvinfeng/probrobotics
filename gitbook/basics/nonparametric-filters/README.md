# Nonparametric Filters

Non-parametric filters do not rely on a fixed functional form of the posterior, such as Gaussian. Instead, they approximate posteriors by a finite number of values, each roughly corresponding to a region in state space. There are two non-parametric approaches for approximating posteriors over continuous spaces with finitely many values. 

### Histogram & Particle Filters

Histogram filters decompose the state space into finitely many regions, and represent the posterior by a histogram. A histogram assigns each region a single cumulative probability; they are best thought of as piece wise constant approximations to a continuous density. Particle filters represent the posteriors by finitely many samples. 

Both techniques do not make strong parametric assumptions on the posterior density. They are well-suited to represent complex multi-modal beliefs. However, the representational power of these techniques comes at the price of added computational complexity. Fortunately, both techniques make it possible to adapt the number of parameters to the complexity of the posterior. Techniques that can adapt the number of parameters to represent the posterior online are called **adaptive**. They are called **resource-adaptive** if they can adapt based on the computational resources available for belief computation. 

