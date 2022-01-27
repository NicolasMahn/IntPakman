import sys
sys.path.append('C:\\Users/nicol/PycharmProjects/IntPakman/Route_Computation')
import Travelling_Salesman


def main():
    prio_list = {0: 0,
                 1: 0,
                 2: 0,
                 3: 1,
                 4: 0,
                 5: 0}

    # Create list of distances between pairs of cities/destinations
    dist_list = [(0, 1, 8.1), (0, 2, 6.0), (0, 3, 8.5), (0, 4, 13.1), (0, 5, 12.9),
                 (1, 2, 5.0), (1, 3, 7.2), (1, 4, 8.0), (1, 5, 10.8),
                 (2, 3, 3.7), (2, 4, 7.1), (2, 5, 7.1),
                 (3, 4, 6.2), (3, 5, 4.5),
                 (4, 5, 4.7)]

    # Initialize fitness function object using dist_list and amount of cities/destinations
    best_state = Travelling_Salesman.get_tsp_result_without_prio(dist_list, 6)
    print(best_state)

    best_state, best_fitness, fitness_curve = Travelling_Salesman.get_tsp_result(dist_list, prio_list, simple_prio=True,
                                                                                 fitness=True, curve=True)

    print(best_state)
    print(best_fitness)
    print(fitness_curve)


if __name__ == "__main__":
    main()
