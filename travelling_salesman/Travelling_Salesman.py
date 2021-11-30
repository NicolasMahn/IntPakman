import six
import sys
sys.modules['sklearn.externals.six'] = six
import mlrose
import numpy as np

def get_optimal_path_and_best_fitness(dist_list, destination_amount, pop_size=200, mutation_prob=0.2, max_attempts=100,
                                      max_iters=np.inf, curve=False, random_state=42, maximize=False):

    problem_fit = mlrose.TSPOpt(length=destination_amount,
                                fitness_fn=mlrose.TravellingSales(distances=dist_list),
                                maximize=maximize)

    if curve:
        best_state, best_fitness, fitness_curve = mlrose.genetic_alg(problem_fit, pop_size=pop_size,
                                                      mutation_prob=mutation_prob, max_attempts=max_attempts,
                                                      max_iters=max_iters, curve=True, random_state=random_state)
        return best_state, best_fitness, fitness_curve
    else:
        best_state, best_fitness = mlrose.genetic_alg(problem_fit, pop_size=pop_size, mutation_prob=mutation_prob,
                                                      max_attempts=max_attempts, max_iters=max_iters, curve=curve,
                                                      random_state=random_state)
        return best_state, best_fitness

def get_optimal_path(dist_list, destination_amount, pop_size=200, mutation_prob=0.2,  max_attempts=100,
                     max_iters=np.inf, curve=False, random_state=42, maximize=False):
    if curve:
        best_state, best_fitness, fitness_curve = get_optimal_path_and_best_fitness(dist_list, destination_amount,
                                                                                    pop_size, mutation_prob,
                                                                                    max_attempts, max_iters, curve,
                                                                                    random_state, maximize)
        return best_state, fitness_curve
    else:
        best_state, best_fitness = get_optimal_path_and_best_fitness(dist_list, destination_amount, pop_size,
                                                                     mutation_prob, max_attempts, max_iters, curve,
                                                                     random_state, maximize)
        return best_state


def get_optimal_fitness(dist_list, destination_amount, pop_size=200, mutation_prob=0.2, max_attempts=100,
                        max_iters=np.inf, curve=False, random_state=42, maximize=False):
    if curve:
        best_state, best_fitness, fitness_curve = get_optimal_path_and_best_fitness(dist_list, destination_amount,
                                                                                    pop_size, mutation_prob,
                                                                                    max_attempts, max_iters, curve,
                                                                                    random_state, maximize)
        return best_fitness, fitness_curve
    else:
        best_state, best_fitness = get_optimal_path_and_best_fitness(dist_list, destination_amount, pop_size,
                                                                     mutation_prob, max_attempts, max_iters, curve,
                                                                     random_state, maximize)
        return best_fitness