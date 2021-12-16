""" Classes for defining optimization problem objects."""

# Author: Nicolas Mahn
# Inspiration/Source: mlrose by Genevieve Hayes
# License: BSD 3 clause

import numpy as np
from sklearn.metrics import mutual_info_score
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree, depth_first_tree
from .fitness import TravellingSales



class TSPOptWithWeights:
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

    def best_neighbor(self):
        """Return the best neighbor of current state.

        Returns
        -------
        best: array
            State vector defining best neighbor.
        """
        fitness_list = []

        for neigh in self.neighbors:
            fitness = self.eval_fitness(neigh)
            fitness_list.append(fitness)

        best = self.neighbors[np.argmax(fitness_list)]

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
        
    def eval_node_probs(self):
        """Update probability density estimates.
        """
        if not self.mimic_speed:
            # Create mutual info matrix
            mutual_info = np.zeros([self.length, self.length])
            for i in range(self.length - 1):
                for j in range(i + 1, self.length):
                    mutual_info[i, j] = -1 * mutual_info_score(
                        self.keep_sample[:, i],
                        self.keep_sample[:, j])

        elif self.mimic_speed:
            # Set ignore error to ignore dividing by zero
            np.seterr(divide='ignore', invalid='ignore')

            # get length of the sample which survived from mimic iteration
            len_sample_kept = self.keep_sample.shape[0]
            # get the length of the bit sequence / problem size
            len_prob = self.keep_sample.shape[1]

            # Expand the matrices to so each row corresponds to a row by row
            # combination of the list of samples
            permuted_rows = np.repeat(self.keep_sample, self.length)
            permuted_rows = np.reshape(permuted_rows,
                                       (len_sample_kept, len_prob * len_prob))
            duplicated_rows = np.hstack(([self.keep_sample] * len_prob))

            # Compute the mutual information matrix in bulk
            # This is done by iterating through the list of possible feature
            # values ((length-1)^2).
            # For example, a binary string would go through 00 01 10 11, for a
            # total of 4 iterations.

            # First initialize the mutual info matrix.
            mutual_info_vectorized = np.zeros([self.length * self.length])
            # Pre-compute the clusters U and V which gets computed multiple
            # times in the inner loop.
            cluster_U = {}
            cluster_V = {}
            cluster_U_sum = {}
            cluster_V_sum = {}
            for i in range(0, self.length):
                cluster_U[i] = (duplicated_rows == i)
                cluster_V[i] = (permuted_rows == i)
                cluster_U_sum[i] = np.sum(duplicated_rows == i, axis=0)
                cluster_V_sum[i] = np.sum(permuted_rows == i, axis=0)

            # Compute the mutual information for all sample to
            # sample combination.
            # Done for each feature combination i & j ((length-1)^2)
            for i in range(0, self.length):
                for j in range(0, self.length):
                    # |U_i AND V_j|/N Length of cluster matching for feature
                    # pair i j over sample length N
                    # This is the first term in the MI computation
                    MI_first_term = np.sum(cluster_U[i] * cluster_V[j], axis=0)
                    MI_first_term = np.divide(MI_first_term, len_sample_kept)

                    # compute the second term of the MI matrix
                    # Length |U_i||V_j|, for the particular feature pair
                    UV_length = (cluster_U_sum[i] * cluster_V_sum[j])
                    MI_second_term = np.log(MI_first_term) - \
                                     np.log(UV_length) + \
                                     np.log(len_sample_kept)

                    # remove the nans and negative infinity, there shouldn't
                    # be any
                    MI_second_term[np.isnan(MI_second_term)] = 0
                    MI_second_term[np.isneginf(MI_second_term)] = 0

                    # Combine the first and second term
                    # Add the whole MI matrix for the feature to the previously
                    # computed values
                    mutual_info_vectorized = mutual_info_vectorized + \
                                             MI_first_term * MI_second_term

            # Need to multiply by negative to get the mutual information, and
            # reshape (Full Matrix)
            mutual_info_full = -1 * np.reshape(mutual_info_vectorized,
                                               (self.length, self.length))

            # Only get the upper triangle matrix above the identity row.
            mutual_info = np.triu(mutual_info_full, k=1)
            # Possible enhancements, currently we are doing double the
            # computation required.
            # Pre set the matrix so the computation is only done for rows that
            # are needed. To do for the future.

        # Find minimum spanning tree of mutual info matrix
        mst = minimum_spanning_tree(csr_matrix(mutual_info))

        # Convert minimum spanning tree to depth first tree with node 0 as root
        dft = depth_first_tree(csr_matrix(mst.toarray()), 0, directed=False)
        dft = np.round(dft.toarray(), 10)

        # Determine parent of each node
        parent = np.argmin(dft[:, 1:], axis=0)

        # Get probs
        probs = np.zeros([self.length, self.length, self.length])

        probs[0, :] = np.histogram(self.keep_sample[:, 0],
                                   np.arange(self.length + 1),
                                   density=True)[0]

        for i in range(1, self.length):
            for j in range(self.length):
                subset = self.keep_sample[np.where(
                    self.keep_sample[:, parent[i - 1]] == j)[0]]

                if not len(subset):
                    probs[i, j] = 1 / self.length
                else:
                    probs[i, j] = np.histogram(subset[:, i],
                                               np.arange(self.length + 1),
                                               density=True)[0]

        # Update probs and parent
        self.node_probs = probs
        self.parent_nodes = parent

    def find_neighbors(self):
        """Find all neighbors of the current state.
        """
        self.neighbors = []

        for node1 in range(self.length - 1):
            for node2 in range(node1 + 1, self.length):
                neighbor = np.copy(self.state)

                neighbor[node1] = self.state[node2]
                neighbor[node2] = self.state[node1]
                self.neighbors.append(neighbor)
                
    def find_sample_order(self):
        """Determine order in which to generate sample vector elements.
        """
        sample_order = []
        last = [0]
        parent = np.array(self.parent_nodes)

        while len(sample_order) < self.length:
            inds = []

            # If last nodes list is empty, select random node than has not
            # previously been selected
            if len(last) == 0:
                inds = [np.random.choice(list(set(np.arange(self.length)) -
                                              set(sample_order)))]
            else:
                for i in last:
                    inds += list(np.where(parent == i)[0] + 1)

            sample_order += last
            last = inds

        self.sample_order = sample_order
    
    def find_top_pct(self, keep_pct):
        """Select samples with fitness in the top keep_pct percentile.

        Parameters
        ----------
        keep_pct: float
            Proportion of samples to keep.
        """
        if (keep_pct < 0) or (keep_pct > 1):
            raise Exception("""keep_pct must be between 0 and 1.""")

        # Determine threshold
        theta = np.percentile(self.pop_fitness, 100 * (1 - keep_pct))

        # Determine samples for keeping
        keep_inds = np.where(self.pop_fitness >= theta)[0]

        # Determine sample for keeping
        self.keep_sample = self.population[keep_inds]

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

    def random_mimic(self):
        """Generate single MIMIC sample from probability density.

        Returns
        -------
        state: array
            State vector of MIMIC random sample.
        """
        remaining = list(np.arange(self.length))
        state = np.zeros(self.length, dtype=np.int8)
        sample_order = self.sample_order[1:]
        node_probs = np.copy(self.node_probs)

        # Get value of first element in new sample
        state[0] = np.random.choice(self.length, p=node_probs[0, 0])
        remaining.remove(state[0])
        node_probs[:, :, state[0]] = 0

        # Get sample order
        self.find_sample_order()
        sample_order = self.sample_order[1:]

        # Set values of remaining elements of state
        for i in sample_order:
            par_ind = self.parent_nodes[i - 1]
            par_value = state[par_ind]
            probs = node_probs[i, par_value]

            if np.sum(probs) == 0:
                next_node = np.random.choice(remaining)

            else:
                adj_probs = self.adjust_probs(probs)
                next_node = np.random.choice(self.length, p=adj_probs)

            state[i] = next_node
            remaining.remove(next_node)
            node_probs[:, :, next_node] = 0

        return state

    def random_neighbor(self):
        """Return random neighbor of current state vector.

        Returns
        -------
        neighbor: array
            State vector of random neighbor.
        """
        neighbor = np.copy(self.state)
        node1, node2 = np.random.choice(np.arange(self.length),
                                        size=2, replace=False)

        neighbor[node1] = self.state[node2]
        neighbor[node2] = self.state[node1]

        return neighbor
    
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

    def sample_pop(self, sample_size):
        """Generate new sample from probability density.

        Parameters
        ----------
        sample_size: int
            Size of sample to be generated.

        Returns
        -------
        new_sample: array
            Numpy array containing new sample.
        """
        if sample_size <= 0:
            raise Exception("""sample_size must be a positive integer.""")
        elif not isinstance(sample_size, int):
            if sample_size.is_integer():
                sample_size = int(sample_size)
            else:
                raise Exception("""sample_size must be a positive integer.""")

        self.find_sample_order()
        new_sample = []

        for _ in range(sample_size):
            state = self.random_mimic()
            new_sample.append(state)

        new_sample = np.array(new_sample)

        return new_sample

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