""" Classes for defining fitness functions."""

# Author: Nicolas Mahn
# Inspiration/Source: mlrose by Genevieve Hayes
# License: BSD 3 clause

import numpy as np
import statistics


class TravellingSales:
    """Fitness function for Travelling Salesman optimization problem.
    Evaluates the fitness of a tour of n nodes, represented by state vector
    :math:`x`, giving the order in which the nodes are visited, as the total
    distance travelled on the tour (including the distance travelled between
    the final node in the state vector and the first node in the state vector
    during the return leg of the tour). Each node must be visited exactly
    once for a tour to be considered valid.
    Adapted by: Nicolas Mahn

    Parameters
    ----------
    coords: list of pairs, default: None
        Ordered list of the (x, y) coordinates of all nodes (where element i
        gives the coordinates of node i). This assumes that travel between
        all pairs of nodes is possible. If this is not the case, then use
        :code:`distances` instead.

    distances: list of triples, default: None
        List giving the distances, d, between all pairs of nodes, u and v, for
        which travel is possible, with each list item in the form (u, v, d).
        Order of the nodes does not matter, so (u, v, d) and (v, u, d) are
        considered to be the same. If a pair is missing from the list, it is
        assumed that travel between the two nodes is not possible. This
        argument is ignored if coords is not :code:`None`.

    weights:... TODO
    prio_importance:
    """

    def __init__(self, coords=None, distances=None, weights=None, prio_importance=25):

        if coords is None and distances is None:
            raise Exception("""At least one of coords and distances must be"""
                            + """ specified.""")

        elif coords is not None:
            self.is_coords = True
            path_list = []
            dist_list = []

        else:
            self.is_coords = False

            # Remove any duplicates from list
            distances = list({tuple(sorted(dist[0:2]) + [dist[2]])
                              for dist in distances})

            # Split into separate lists
            node1_list, node2_list, dist_list = zip(*distances)

            if min(dist_list) <= 0:
                raise Exception("""The distance between each pair of nodes"""
                                + """ must be greater than 0.""")
            if min(node1_list + node2_list) < 0:
                raise Exception("""The minimum node value must be 0.""")

            if not max(node1_list + node2_list) == \
                   (len(set(node1_list + node2_list)) - 1):
                raise Exception("""All nodes must appear at least once in"""
                                + """ distances.""")

            path_list = list(zip(node1_list, node2_list))

        self.coords = coords
        self.weights = weights
        self.distances = distances
        self.path_list = path_list
        self.dist_list = dist_list
        self.prio_importance = prio_importance

    def evaluate(self, state):
        """Evaluate the fitness of a state vector.
            Adapted by: Nicolas Mahn
        Parameters
        ----------
        state: array
            State array for evaluation. Each integer between 0 and
            (len(state) - 1), inclusive must appear exactly once in the array.

        Returns
        -------
        fitness: float
            Value of fitness function. Returns :code:`np.inf` if travel between
            two consecutive nodes on the tour is not possible.
        """

        if self.is_coords and len(state) != len(self.coords):
            raise Exception("""state must have the same length as coords.""")

        if not len(state) == len(set(state)):
            raise Exception("""Each node must appear exactly once in state.""")

        if min(state) < 0:
            raise Exception("""All elements of state must be non-negative"""
                            + """ integers.""")

        if max(state) >= len(state):
            raise Exception("""All elements of state must be less than"""
                            + """ len(state).""")

        fitness = 0

        # Calculate length of each leg of journey
        if self.is_coords:
            for i in range(len(state) - 1):
                node1 = state[i]
                node2 = state[i + 1]

                fitness += np.linalg.norm(np.array(self.coords[node1]) - np.array(self.coords[node2])) - \
                           ((self.weights[state[i]] * \
                             (sum(self.dist_list) / (len(self.dist_list) * self.prio_importance)) * \
                             (len(state) - 1)) / (i + 1))

            # Calculate length of final leg
            node1 = state[-1]
            node2 = state[0]

            fitness += np.linalg.norm(np.array(self.coords[node1]) - np.array(self.coords[node2])) - \
                       self.weights[state[i]] * \
                       (sum(self.dist_list) / (len(self.dist_list) * self.prio_importance))


        else:
            for i in range(len(state) - 1):
                node1 = state[i]
                node2 = state[i + 1]

                path = (min(node1, node2), max(node1, node2))

                if path in self.path_list:
                    fitness += self.dist_list[self.path_list.index(path)] - \
                               ((self.weights[state[i]] * \
                                 (sum(self.dist_list) / (len(self.dist_list) * self.prio_importance)) * \
                                 (len(state) - 1)) / (i + 1))
                else:
                    fitness += np.inf

            # Calculate length of final leg
            node1 = state[-1]
            node2 = state[0]

            path = (min(node1, node2), max(node1, node2))

            if path in self.path_list:
                fitness += self.dist_list[self.path_list.index(path)] - \
                           self.weights[state[-1]] * \
                           (sum(self.dist_list) / (len(self.dist_list) * self.prio_importance))
            else:
                fitness += np.inf

        if (fitness > 0):
            return fitness
        else:
            return 0
