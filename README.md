RandomGen
=========

This package allows to generate the pseudo random numbers from a given sample with the given discrete probability distribution.

# Algorithm

It makes use of discrete sampling method. The algorithm is the following:
- read and validate the input numbers and its probabilities
- generate the discrete cumulative distribution, i.e. divide the [0,1] range according to the given probabilities into _buckets_
- generate the pseudo random number x from the uniform distribution in [0,1)
- loop over the input sample and cumulative distribution, comparing the generated number x with the current value from the cumulative distribtion
- return the number from the input when the generated number x is smaller than the value from the cumulative distribtion, i.e. check into which _bucket_ x falls into

Essentially, the functionality of this package is equivalent to:
```py
import random
random.choices(random_nums, weights=probabilities)[0]
```

# Usage:

- First, install the package:
```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install .
```
- To generate the single number:
```python
>>> from randomgen.RandomGen import RandomGen
>>>
>>> generator = {-1: 0.01, 0: 0.3, 1: 0.58, 2: 0.1, 3: 0.01}
>>> RandomGen.init_generator(generator)
>>> RandomGen().next_num()
1 # example!
```

- To generate a larger sample, run e.g.:
```python
>>> results = []
>>> sample = 1_000
>>> for _ in range(sample):
...     results.append(RandomGen().next_num())
...
```
- Then, you can check the results:
```python
>>> from collections import Counter
>>> experiment = {num: count/sample for num, count in Counter(results).items()}
>>> compare = {num: [theory, experiment[num]] for num, theory in generator.items()}
>>> from pprint import pprint
>>> pprint(compare) # just an example!
{-1: [0.01, 0.015],
 0: [0.3, 0.313],
 1: [0.58, 0.582],
 2: [0.1, 0.085],
 3: [0.01, 0.005]}
```

# Development:

This code makes use of [Poetry](https://python-poetry.org/) to build, test, and package the project.

## Testing

To run the tests:
```bash
poetry run pytest .
```
Warning! One of the tests _may_ fail due to nature of probability!

## Code quality

The code is formatted using [black](https://black.readthedocs.io/en/stable/). Imports are sorted with [isort](https://github.com/PyCQA/isort). The code is linted with [mypy](http://mypy-lang.org/). All those tools run with [pre-commit](https://pre-commit.com/).
