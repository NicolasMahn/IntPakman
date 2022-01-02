import six
import sys

sys.modules['sklearn.externals.six'] = six
import mltulip
import numpy as np

POP_SIZE = 200
MUTATION_PROB = 0.2
MAX_ATTEMPTS = 100
MAX_ITERS = np.inf
RANDOM_STATE = 42
MAXIMIZE = False


def get_tsp_result(dist_list: list, prio_list: dict, state=True, fitness=False, curve=False):
    """
    This method starts the evolutionary algorithm which solves the travelling sales person
    param:dist_list a dict of all distances between all destinations
    param:prio_list a dict of all priorities of destinations
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
        else:
            return best_state, fitness_curve

    else:
        best_state, best_fitness = algorythm.genetic_alg(problem_fit,
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
