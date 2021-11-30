import six
import sys
sys.modules['sklearn.externals.six'] = six
import mlrose
import numpy as np
import Travelling_Salesman


def main():
    # Create list of distances between pairs of cities
    dist_list = [(0, 1, 8.1), (0, 2, 6.0), (0, 3, 8.5), (0, 4, 13.1), (0, 5, 12.9),
                              (1, 2, 5.0), (1, 3, 7.2), (1, 4, 8.0),  (1, 5, 10.8),
                                           (2, 3, 3.7), (2, 4, 7.1),  (2, 5, 7.1),
                                                        (3, 4, 6.2),  (3, 5, 4.5),
                                                                      (4, 5, 4.7)]

    # Initialize fitness function object using dist_list
    best_state, best_fitness = Travelling_Salesman.get_optimal_path_and_best_fitness(dist_list, 6)

    print(best_state)
    print(best_fitness)

if __name__ == "__main__":
    main()