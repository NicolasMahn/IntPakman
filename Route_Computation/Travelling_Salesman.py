import six
import sys

from Route_Computation import mltulip
import numpy as np

sys.modules['sklearn.externals.six'] = six

POP_SIZE = 300
MUTATION_PROB = 0.02
MAX_ATTEMPTS = 200
MAX_ITERS = np.inf
RANDOM_STATE = 42
MAXIMIZE = False


def get_tsp_result_without_prio(dist_list: list, length: int, state=True, fitness=False, curve=False):
    """
    This method opens get_tsp_result() with an empty prio_list
    :param dist_list: a dict of all distances between all destinations
    :param length: the number of
    :param state: if True the best state of the TSP will be returned
    :param fitness: if True the best Fitness, meaning the lowest cumulative node cost, will be returned
    :param curve: if True the best Fitness of each iteration will be returned as a list
    """

    prio_list = dict()
    for i in range(length):
        prio_list[i] = 0

    return get_tsp_result(dist_list, prio_list, state=state, fitness=fitness, curve=curve)


def get_tsp_result(dist_list: list, prio_list: dict, state=True, fitness=False, curve=False):
    """
    This method starts the evolutionary algorithm which solves the travelling sales person
    :param dist_list: a dict of all distances between all destinations
    :param prio_list: a dict of all priorities of destinations
    :param state: if True the best state of the TSP will be returned
    :param fitness: if True the best Fitness, meaning the lowest cumulative node cost, will be returned
    :param curve: if True the best Fitness of each iteration will be returned as a list
    """

    problem_fit = mltulip.TSPOpt(length=len(prio_list),
                                 maximize=MAXIMIZE,
                                 distances=dist_list,
                                 weights=prio_list)

    if curve:
        best_state, best_fitness, fitness_curve = mltulip.genetic_alg(problem_fit,
                                                                      pop_size=POP_SIZE,
                                                                      mutation_prob=MUTATION_PROB,
                                                                      max_attempts=MAX_ATTEMPTS,
                                                                      max_iters=MAX_ITERS, curve=True,
                                                                      random_state=RANDOM_STATE)
        if fitness and state:
            return best_state, best_fitness, fitness_curve
        elif fitness:
            return best_fitness, fitness_curve
        elif state:
            return best_state, fitness_curve
        else:
            return fitness_curve

    else:
        best_state, best_fitness = mltulip.genetic_alg(problem_fit,
                                                       pop_size=POP_SIZE,
                                                       mutation_prob=MUTATION_PROB,
                                                       max_attempts=MAX_ATTEMPTS,
                                                       max_iters=MAX_ITERS,
                                                       random_state=RANDOM_STATE)
        if fitness and state:
            return best_state, best_fitness
        elif fitness:
            return best_fitness
        else:
            return best_state
