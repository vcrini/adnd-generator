#!/usr/bin/python
# -*- coding: utf-8 -*-
import random


def rnd(n=1, n_faces=6, plus=0):
    """
    >>> rnd(1,1)
    1
    >>> rnd(1,1,1)
    2
    """

    s = random.randint(1, n_faces) + plus
    if n > 1:
        for _ in range(n - 1):
            s += random.randint(1, n_faces)
    return s


def rnd2(
    tot=4,
    waste=1,
    n_faces=6,
    plus=0,
    ):
    """
....In order to drop waste result from tot rolls (e.g  rnd(4,1,6) rolls 4d6 and drops the lowest one before summing
....>>> rnd2(4,1,1)
....3
...."""

    x = [rnd(1, n_faces) for _ in range(0, tot)]
    x.sort(reverse=True)
    return reduce(lambda a, b: a + b, x[0:tot - waste])


def random_pick(some_list, probabilities):
    assert len(some_list) == len(probabilities)
    assert 0 <= min(probabilities) and max(probabilities) <= 1
    assert abs(sum(probabilities) - 1.0) < 1.0e-5
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for (item, item_probability) in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    return item


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # print """ Random dice roll. Usage

    # import random
    #
    # rnd(number or rolls, dice faces,plus modifier)
    #
    #
    # es.
    # rnd(1,6)    --> number between 1 and 6 (1d6)
    # rnd(2,6+13) --> 2d6+13
    # """
