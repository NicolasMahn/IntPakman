""" Classes for defining optimization problem objects."""

# Author: Nicolas Mahn
# Inspiration/Source: mlrose by Genevieve Hayes
# License: BSD 3 clause

import numpy as np
from sklearn.metrics import mutual_info_score
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree, depth_first_tree
from .fitness import TravellingSales


class TSPOpt:
    """Class for defining travelling salesperson optimisation problems with weights.

    Parameters
    ----------
    length: int
        Number of elements in state vector. Must equal number of nodes in the
        tour.

    fitness_fn: fitness function object, default: None
        Object to implement fitness function for optimization. If :code:`None`,
        then :code:`TravellingSales(coords=coords, distances=distances)` is
        used by default.

    maximize: bool, default: False
        Whether to maximize the fitness function.
        Set :code:`False` for minimization problem.

    coords: list of pairs, default: None
        Ordered list of the (x, y) co-ordinates of all nodes. This assumes
        that travel between all pairs of nodes is possible. If this is not the
        case, then use distances instead. This argument is ignored if
        fitness_fn is not :code:`None`.

    distances: list of triples, default: None
        List giving the distances, d, between all pairs of nodes, u and v, for
        which travel is possible, with each list item in the form (u, v, d).
        Order of the nodes does not matter, so (u, v, d) and (v, u, d) are
        considered to be the same. If a pair is missing from the list, it is
        assumed that travel between the two nodes is not possible. This
        argument is ignored if fitness_fn or coords is not :code:`None`.

    weights: TODO
    """

    def __init__(self, length, fitness_fn=None, maximize=False, coords=None,
                 distances=None, weights=None):

        i = 0
        while i > length - 1:
            weights.setdefault(i, 0)
            i += 1

        if (fitness_fn is None) and (coords is None) and (distances is None):
            raise Exception("""At least one of fitness_fn, coords and"""
                            + """ distances must be specified.""")
        elif fitness_fn is None:
            fitness_fn = TravellingSales(coords=coords, distances=distances, weights=weights)

        if length < 0:
            raise Exception("""length must be a positive integer.""")
        elif not isinstance(length, int):
            if length.is_integer():
                self.length = int(length)
            else:
                raise Exception("""length must be a positive integer.""")
        else:
            self.length = length

        self.state = np.array([0] * self.length)
        self.neighbors = []
        self.fitness_fn = fitness_fn
        self.fitness = 0
        self.population = []
        self.pop_fitness = []
        self.mate_probs = []
        self.keep_sample = []
        self.node_probs = np.zeros([self.length, self.length, self.length])
        self.parent_nodes = []
        self.sample_order = []
        self.mimic_speed = False

        if maximize:
            self.maximize = 1.0
        else:
            self.maximize = -1.0

    def adjust_probs(self, probs):
        """Normalize a vector of probabilities so that the vector sums to 1.

        Parameters
        ----------
        probs: array
            Vector of probabilities that may or may not sum to 1.

        Returns
        -------
        adj_probs: array
            Vector of probabilities that sums to 1. Returns a zero vector if
            sum(probs) = 0.
        """
        if np.sum(probs) == 0:
            adj_probs = np.zeros(np.shape(probs))

        else:
            adj_probs = probs / np.sum(probs)

        return adj_probs

    def best_child(self):
        """Return the best state in the current population.

        Returns
        -------
        best: array
            State vector defining best child.
        """
        best = self.population[np.argmax(self.pop_fitness)]

        return best

    def eval_fitness(self, state):
        """Evaluate the fitness of a state vector.

        Parameters
        ----------
        state: array
            State vector for evaluation.

        Returns
        -------
        fitness: float
            Value of fitness function.
        """
        if len(state) != self.length:
            raise Exception("state length must match problem length")

        fitness = self.maximize * self.fitness_fn.evaluate(state)

        return fitness

    def eval_mate_probs(self):
        """
        Calculate the probability of each member of the population reproducing.
        """
        pop_fitness = np.copy(self.pop_fitness)
        sum_fitness = np.sum(pop_fitness)

        # Set -1*inf values to 0 to avoid dividing by sum of infinity.
        # This forces mate_probs for these pop members to 0.
        pop_fitness[pop_fitness == -1.0 * np.inf] = 0

        if sum_fitness == 0:
            self.mate_probs = np.ones(len(pop_fitness)) / len(pop_fitness)
        elif self.maximize == 1:
            self.mate_probs = pop_fitness / sum_fitness
        # creates mate probability if fitness is negative
        # if fitness 0 mate probability will also be 0
        else:
            pop_fitness = [0 if x == 0 else sum_fitness / x for x in pop_fitness]
            self.mate_probs = pop_fitness / np.sum(pop_fitness)

    def get_fitness(self):
        """ Return the fitness of the current state vector.

        Returns
        -------
        self.fitness: float
            Fitness value of current state vector.
        """
        return self.fitness

    def get_keep_sample(self):
        """ Return the keep sample.

        Returns
        -------
        self.keep_sample: array
            Numpy array containing samples with fitness in the top keep_pct
            percentile.
        """
        return self.keep_sample

    def get_length(self):
        """ Return the state vector length.

        Returns
        -------
        self.length: int
            Length of state vector.
        """
        return self.length

    def get_mate_probs(self):
        """ Return the population mate probabilities.

        Returns
        -------
        self.mate_probs: array.
            Numpy array containing mate probabilities of the current
            population.
        """
        return self.mate_probs

    def get_maximize(self):
        """ Return the maximization multiplier.

        Returns
        -------
        self.maximize: int
            Maximization multiplier.
        """
        return self.maximize

    def get_pop_fitness(self):
        """ Return the current population fitness array.

        Returns
        -------
        self.pop_fitness: array
            Numpy array containing the fitness values for the current
            population.
        """
        return self.pop_fitness

    def get_population(self):
        """ Return the current population.

        Returns
        -------
        self.population: array
            Numpy array containing current population.
        """
        return self.population

    def get_state(self):
        """ Return the current state vector.

        Returns
        -------
        self.state: array
            Current state vector.
        """
        return self.state

    def random(self):
        """Return a random state vector.

        Returns
        -------
        state: array
            Randomly generated state vector.
        """
        state = np.random.permutation(self.length)

        return state

    def random_pop(self, pop_size):
        """Create a population of random state vectors.

        Parameters
        ----------
        pop_size: int
            Size of population to be created.
        """
        if pop_size <= 0:
            raise Exception("""pop_size must be a positive integer.""")
        elif not isinstance(pop_size, int):
            if pop_size.is_integer():
                pop_size = int(pop_size)
            else:
                raise Exception("""pop_size must be a positive integer.""")

        population = []
        pop_fitness = []

        for _ in range(pop_size):
            state = self.random()
            fitness = self.eval_fitness(state)

            population.append(state)
            pop_fitness.append(fitness)

        self.population = np.array(population)
        self.pop_fitness = np.array(pop_fitness)

    def reproduce(self, parent_1, parent_2, mutation_prob=0.1):
        """Create child state vector from two parent state vectors.

        Parameters
        ----------
        parent_1: array
            State vector for parent 1.

        parent_2: array
            State vector for parent 2.

        mutation_prob: float
            Probability of a mutation at each state element during
            reproduction.

        Returns
        -------
        child: array
            Child state vector produced from parents 1 and 2.
        """
        if len(parent_1) != self.length or len(parent_2) != self.length:
            raise Exception("""Lengths of parents must match problem length""")

        if (mutation_prob < 0) or (mutation_prob > 1):
            raise Exception("""mutation_prob must be between 0 and 1.""")

        # Reproduce parents
        if self.length > 1:
            _n = np.random.randint(self.length - 1)
            child = np.array([0] * self.length)
            child[0:_n + 1] = parent_1[0:_n + 1]

            unvisited = \
                [node for node in parent_2 if node not in parent_1[0:_n + 1]]
            child[_n + 1:] = unvisited
        elif np.random.randint(2) == 0:
            child = np.copy(parent_1)
        else:
            child = np.copy(parent_2)

        # Mutate child
        rand = np.random.uniform(size=self.length)
        mutate = np.where(rand < mutation_prob)[0]

        if len(mutate) > 0:
            mutate_perm = np.random.permutation(mutate)
            temp = np.copy(child)

            for i in range(len(mutate)):
                child[mutate[i]] = temp[mutate_perm[i]]

        return child

    def reset(self):
        """Set the current state vector to a random value and get its fitness.
        """
        self.state = self.random()
        self.fitness = self.eval_fitness(self.state)

    def set_population(self, new_population):
        """ Change the current population to a specified new population and get
        the fitness of all members.

        Parameters
        ----------
        new_population: array
            Numpy array containing new population.
        """
        self.population = new_population

        # Calculate fitness
        pop_fitness = []

        for i in range(len(self.population)):
            fitness = self.eval_fitness(self.population[i])
            pop_fitness.append(fitness)

        self.pop_fitness = np.array(pop_fitness)

    def set_state(self, new_state):
        """
        Change the current state vector to a specified value
        and get its fitness.

        Parameters
        ----------
        new_state: array
            New state vector value.
        """
        if len(new_state) != self.length:
            raise Exception("""new_state length must match problem length""")

        self.state = new_state
        self.fitness = self.eval_fitness(self.state)
