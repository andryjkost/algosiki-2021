import csv
import pickle
import os
import codecs
import numpy as np
import pandas as pd
import numpy as np
import random, math
from urllib.request import urlopen

import matplotlib.pyplot as plt


class TravelingSalesmanProblem:

    def __init__(self, name):



        self.name = name
        self.locations = []
        self.distances = []
        self.tspSize = 0


        self.__initData()

    def __len__(self):

        return self.tspSize

    def __initData(self):

        self.__createData()
        self.tspSize = len(self.locations)

    def __createData(self):
        """Reads the desired TSP file from the Internet, extracts the city coordinates, calculates the distances
        between every two cities and uses them to populate a distance matrix (two-dimensional array).
        It then serializes the city locations and the calculated distances to disk using the pickle utility.
        """
        self.locations = []

        # open whitespace-delimited file from url and read lines from it:
        data = pd.read_csv('cities.csv')
        path_first = pd.read_csv('sample_submission.csv')
        first_path = [id for id in path_first["Path"]]
        index_cities = [city_id for city_id in data["CityId"]]
        coord_x = [x for x in data["X"]]
        coord_y = [y for y in data["Y"]]

        self.tspSize = len(index_cities)
        for i in range(len(index_cities)):
            self.locations.append([coord_x[i], coord_y[i]])

        # initialize distance matrix by filling it with 0's:
        self.distances = [[0] * self.tspSize for _ in range(self.tspSize)]

        # populate the distance matrix with calculated distances:
        for i in range(self.tspSize):
            for j in range(i + 1, self.tspSize):
                summ = 0.0
                for coord1, coord2 in zip(self.locations[i], self.locations[j]):
                    summ += pow((coord1 - coord2), 2)
                self.distances[i][j] = math.sqrt(summ)
                self.distances[j][i] = math.sqrt(summ)

    def getTotalDistance(self, indices):
        """Calculates the total distance of the path described by the given indices of the cities
        :param indices: A list of ordered city indices describing the given path.
        :return: total distance of the path described by the given indices
        """
        # distance between th elast and first city:
        distance = self.distances[indices[-1]][indices[0]]

        # add the distance between each pair of consequtive cities:
        for i in range(len(indices) - 1):
            distance += self.distances[indices[i]][indices[i + 1]]

        return distance

    def plotData(self, indices):
        """plots the path described by the given indices of the cities
        :param indices: A list of ordered city indices describing the given path.
        :return: the resulting plot
        """

        # plot the dots representing the cities:
        plt.scatter(*zip(*self.locations), marker='.', color='red')

        # create a list of the corresponding city locations:
        locs = [self.locations[i] for i in indices]
        locs.append(locs[0])

        # plot a line between each pair of consequtive cities:
        plt.plot(*zip(*locs), linestyle='-', color='blue')

        return plt


# testing the class:
def main():
    # create a problem instance:
    tsp = TravelingSalesmanProblem("santa")

    # generate a random solution and evaluate it:
    #randomSolution = random.sample(range(len(tsp)), len(tsp))

    # see http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/bayg29.opt.tour
    i=0
    solution=[i for i in range(0,197768)]
    optimalSolution = [0, 27, 5, 11, 8, 25, 2, 28, 4, 20, 1, 19, 9, 3, 14, 17, 13, 16, 21, 10, 18, 24, 6, 22, 7, 26, 15, 12, 23]

    # print("Problem name: " + tsp.name)
    # print("Optimal solution = ", optimalSolution)
    # print("Optimal distance = ", tsp.getTotalDistance(solution))
    print(tsp.distances[0][0])
    # plot the solution:
    plot = tsp.plotData(optimalSolution)
    plot.show()


if __name__ == "__main__":
    main()
