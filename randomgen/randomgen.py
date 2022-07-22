import math
import random
import sys
from itertools import accumulate
from numbers import Number


class RandomGen(object):
    """Class implementing the pseudo random number generator"""

    # Values that may be returned by next_num()
    _random_nums: list[Number] = []

    # Probability of the occurence of random_nums
    _probabilities: list[float] = []

    # Accumulated probabilities
    _acc_prob: list[float] = []

    @classmethod
    def init_generator(cls, gen=None) -> None:
        """Class method to initialise the random generator. Each call creates the new generator.

        Args:
          dict: random_nums as keys and its probabilities as values.
        Raises:
          ValueError if the sum of probabilities does not equal to 1.
        Returns:
          None if success
        """
        if gen is None:
            gen = {}
        cls._random_nums = []
        cls._probabilities = []
        for key, value in gen.items():
            cls._random_nums.append(key)
            cls._probabilities.append(value)
        if not all(
            [
                isinstance(item, Number)
                for item in [*cls._random_nums, *cls._probabilities]
            ]
        ):
            raise ValueError("Found values which are not numeric")
        if not all([1 >= item >= 0 for item in cls._probabilities]):
            raise ValueError("Found probabilities outside [0,1] range")
        if not math.isclose(
            sum(cls._probabilities), 1.0, abs_tol=sys.float_info.epsilon
        ):
            raise ValueError("Provided probilities do not add up to 1")

        # helper list to keep the accumulated probabilities
        cls._acc_prob = list(accumulate(cls._probabilities))

    def next_num(self):
        """
        Returns one of the randomNums. When this method is called multiple times over a long period,
        it should return the numbers roughly with the initialized probabilities.

        The returned value is equivalent to:
        random.choices(self._random_nums, weights=self._probabilities)[0]

        """
        # let's generate a pseudo random number between 0 and 1 from the uniform distributon
        rand = random.random()
        # now, we iterate over random_nums, one of which will be returned
        for idx, num in enumerate(self._random_nums):
            # we check where `rand` fell into
            # thus, we compare a generated number to the cumulative probabilities calculated up to currently checked random_num
            if rand < self._acc_prob[idx]:
                # since `rand` is uniformly distributed, probability of returned num is proportional to the width of currently checked range
                # of the divided [0,1) range according to given probabilities
                return num
