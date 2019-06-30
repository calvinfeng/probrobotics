# Grid and Monte Carlo

We will describe two localization algorithms that are capable of solving global localization problems.

* They can process raw sensor measurements. There is no need to extract features from sensor values.
* They are non-parametric.
* They can solve global localization and kidnapped robot problems.

The first approach is called _grid localization_. It uses a histogram filter to represent the posterior belief.  The second approach is called the _Monte Carlo localization_, arguably the most popular localization algorithm to date. It uses particle filters to estimate posteriors over robot poses. 



