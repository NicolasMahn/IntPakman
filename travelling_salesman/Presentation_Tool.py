import six
import sys
sys.modules['sklearn.externals.six'] = six
import mlrose
import numpy as np


def main():
    # Create list of distances between pairs of cities
    dist_list = [(0, 1, 8.1), (0, 2, 6.0), (0, 3, 8.5), (0, 4, 13.1), (0, 5, 12.9),
                              (1, 2, 5.0), (1, 3, 7.2), (1, 4, 8.0),  (1, 5, 10.8),
                                           (2, 3, 3.7), (2, 4, 7.1),  (2, 5, 7.1),
                                                        (3, 4, 6.2),  (3, 5, 4.5),
                                                                      (4, 5, 4.7)]

    route = [4,0,5,3,2,1]
    i = 0
    sum = 0

    for r in route:
        if i == 0:
           j = 5
        else:
            j = i-1

        for d in dist_list:

            if (d[0] == route[i] and d[1] == route[j]) or (d[0] == route[j] and d[1] == route[i]):
                sum += d[2]
                continue

        #print(sum)
        i+=1

    print(sum)

if __name__ == "__main__":
    main()