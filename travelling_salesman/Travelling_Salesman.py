import six
import sys

from travelling_salesman import mltulip
import numpy as np

sys.modules['sklearn.externals.six'] = six

POP_SIZE = 1000
MUTATION_PROB = 0.2
MAX_ATTEMPTS = 200
MAX_ITERS = np.inf
RANDOM_STATE = 42
MAXIMIZE = False

def get_tsp_result_without_prio(dist_list: list, length: int, state=True, fitness=False, curve=False):

    prio_list = dict()
    for i in range(length):
        prio_list[i] = 0

    return get_tsp_result(dist_list, prio_list, state=state, fitness=fitness, curve=curve, )

def get_tsp_result(dist_list: list, prio_list: dict, state=True, fitness=False, curve=False):
    """
    This method starts the evolutionary algorithm which solves the travelling sales person
    param:dist_list a dict of all distances between all destinations
    param:prio_list a dict of all priorities of destinations
    """

    #print(prio_list)

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
        else:
            return best_state, fitness_curve

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
