import math
import random
from collections import Counter, defaultdict

import pytest

from randomgen import RandomGen, __version__


def test_version():
    assert __version__ == "0.1.0"


def generate_random_valid_input():
    """Helper to generate random, valid input"""
    probs = [random.random() for _ in range(1, random.randint(1, 100))]
    probs = [prob / sum(probs) for prob in probs]
    return {random.random(): prob for prob in probs}


# test cases with valid inputs
# - probabilities add up to 1
# - probabilities in [0,1]
valid_generators = [
    {-1: 0.01, 0: 0.3, 1: 0.58, 2: 0.1, 3: 0.01},
    {-1: 1.0},
    {-1: 1.0, 1: 0.0},
    {-1: 1.0, 1: 0.0, 2: 0},
    {-1: 0.5, 1: 0.5},
    {-1: 0.5, 1: 0.5, 2: 0.0},
    {5.4: 0.3, 2.67: 0.4, 1.12: 0.1, 4.678: 0.15, 0: 0.05},
    generate_random_valid_input(),
]

# test cases with invalid inputs
# - probabilities do not add up to 1
# - probabilities not in [0,1]
# - random_nums or probabilities not numeric
invalid_generators = [
    {},
    {-1: 0.01, 0: 0.3, 1: 0.58, 2: 0.1, 3: 0.1},
    {-1: 0.01, 0: 0.5, 1: 0.58, 2: -0.1, 3: 0.01},
    {-1: 0.01, 0: 0.3, 1: "0.58", 2: 0.1, 3: 0.01},
    {-1: 0.01, 0: 0.3, 1: 0.58, 2: 0.1, "3": 0.01},
]


@pytest.mark.parametrize("invalid", invalid_generators)
def test_invalid_input(invalid):
    # expect Errors if the input is invalid
    with pytest.raises(ValueError):
        RandomGen.init_generator(invalid)


@pytest.mark.parametrize("valid", valid_generators)
def test_valid_input(valid):
    # if valid input, we expect None to be returned
    assert RandomGen.init_generator(valid) == None


@pytest.mark.parametrize("valid", valid_generators)
def test_next_num(valid):
    # make sure that we always return something from the generated input ...
    RandomGen.init_generator(valid)
    # ... except for numbers with 0 probability
    impossible = [num for num, prob in valid.items() if math.isclose(prob, 0)]
    for _ in range(100):
        num = RandomGen().next_num()
        assert num in valid
        assert num not in impossible


@pytest.mark.parametrize("generator", [valid_generators[0]])
def test_statistical_pragmatic(generator):
    """Run the statistical test of the generator.
    Warning! This test can fail due to stochastic nature of probability!
    This is not really a unit test, but more a pragmatic verification
    if the produced output is sensible. The idea is that, in general,
    when we increase the number of generated numbers we converge to the
    given probabilities. However, it may fluctuate, leading to failure of this test.
    Proper way would be to perform statistical verification of the hypothesis.
    """
    RandomGen.init_generator(generator)
    results = {}
    compare = defaultdict(list)
    for sample in [
        23,
        1047,
        1_002_037,
    ]:  # randomly chosen sample size, separated significantly to 'help' the test to pass
        results[sample] = []
        for _ in range(sample):
            results[sample].append(RandomGen().next_num())

        for key, val in Counter(results[sample]).items():
            compare[key].append(val / sample)
        for key in generator:
            if key not in Counter(results[sample]):
                compare[key].append(0)
    for num, freqs in compare.items():
        for idx, freq in enumerate(freqs):
            if idx + 1 < len(freqs):
                assert abs(freq - generator[num]) > abs(freqs[idx + 1] - generator[num])
