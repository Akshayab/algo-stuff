# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 14:30:18 2016

@author: gaurang
Solution to Question 2 of Assignment 3
Optimal is 2020 @ http://debian.cse.msu.edu/CSE/pub/GA/programs/Genocop-doc/TSP/TSPLIB_VALUES
Optimal Cost = 9074.14804787284
Optimal Tour =  [0, 27, 5, 11, 8, 25, 2, 28, 4, 20, 1, 19, 9, 3, 14, 17, 13, 16, 21, 10, 18, 24, 6, 22, 7, 26, 15, 12, 23]
http://file.scirp.org/pdf/ICA_2013052411354682.pdf
Best solution: [2, 28, 25, 4, 8, 11, 5, 27, 0, 12, 15, 23, 7, 26, 22, 6, 24, 18, 10, 16, 21, 13, 17, 14, 3, 9, 19, 1, 20]
Best cost: 9371.46982682
"""
import math
import random


def euclidean(a, b):
    return math.sqrt(pow(a[1] - b[1], 2) + pow(a[0] - b[0], 2))

'''
Online update is done each time an ant constructs a solution
Then local search happens
After local search, offline update is applied
'''

def generate_solution():
    start = []
    start.append(random.randint(0, 28))
    # start = list(random.randint(0, 28))
    while len(start) != 29:
        start = get_next(start)
    return start

def get_next(visited):
    best_prob = 0
    next_city = -1
    for i in range(0, 29):
        if i in visited:
            continue
        else:
            current_prob = calculate_probability(visited, visited[-1], i)
            if current_prob > best_prob:
                best_prob = current_prob
                next_city = i
    if best_prob > random.uniform(0, 1):
        visited.append(next_city)
    else:
        city = random.randint(0, 28)
        while city in visited:
            city = random.randint(0, 28)
        visited.append(city)
    return visited

def calculate_probability(visited, from_city, to_city):
    total_pheromone = 0
    total_distance = 0
    edge_pheromone = pheromone[from_city][to_city]
    edge_dist = euclidean(coordinates[from_city], coordinates[to_city])
    numerator = edge_pheromone/edge_dist
    for i in range(0, 29):
        if i in visited:
            continue
        else:
            total_pheromone += pheromone[from_city][i]
            total_distance += euclidean(coordinates[from_city], coordinates[i])
    denominator = total_pheromone/total_distance
    return numerator/denominator

def calculate_cost(soln):
    cost = 0
    for i in range(0, 29):
        city_coords = coordinates[soln[i]]
        if i == 28:
            next_coords = coordinates[soln[0]]
        else:
            next_coords = coordinates[soln[i + 1]]
        cost += euclidean(city_coords, next_coords)
    return cost

def online_update(soln, cost):
    for i in range(0, 29):
        x = soln[i]
        if i == 28:
            y = soln[0]
        else:
            y = soln[i + 1]
        pheromone[x][y] += (q/cost)
        pheromone[y][x] += (q/cost)

def pheromone_evaporate():
    for i in range(len(pheromone)):
        for j in range(len(pheromone)):
            if pheromone[i][j] != 0.5:
                pheromone[i][j] *= (1 - rho)

def offline_update(soln, cost):
    for i in range(0, 29):
        x = soln[i]
        if i == 28:
            y = soln[0]
        else:
            y = soln[i + 1]
        pheromone[x][y] += (q / cost)
        pheromone[y][x] += (q / cost)

'''
ACO algo:
set all params and initialize pheromone
loop
    sub loop
        Construct solutions based on the state transition rule
        Apply the online pheromone update rule
        Continue until all ants have been generated
    Apply Local Search
    Evaluate all solutions and record the best solution so far
    Apply the offline pheromone update rule
continue until stopping criteria
'''

def ant_col():
    iterations = 0
    iter_best_cost = float("inf")
    iter_best_soln = []
    while iterations < max_iter:
        ant_best_cost = float("inf")
        ant_best_solution = []
        for ant in range(0, num_ants):
            current_solution = generate_solution()
            current_cost = calculate_cost(current_solution)
            if current_cost < ant_best_cost:
                ant_best_cost = current_cost
                ant_best_solution = current_solution
            online_update(current_solution, current_cost)
            pheromone_evaporate()
            offline_update(ant_best_solution, ant_best_cost)
        if ant_best_cost < iter_best_cost:
            iter_best_cost = ant_best_cost
            iter_best_soln = ant_best_solution
        offline_update(iter_best_soln, iter_best_cost)
        iterations += 1
    print "Best solution: " + str(iter_best_soln)
    print "Best cost: " + str(iter_best_cost)

file = open('bays_29.tsp', 'r')
num_ants = 25
num_cities = 0
rho = 0.25
max_iter = 20
q = 2000
reading_city = False
reading_weight = False

# Every index is going to be a 2D coordinate for (i + 1)th city
# Eg: The first (0th) element contains coords for city 1
coordinates = []

# Every index is going to contain the (i+1)th city's edge weight's to the other cities
# 2D matrix
weights = []

for line in file:
    data = line.split()
    type = data[0]

    if type == "DIMENSION:":  # number of cities
        num_cities = int(data[1])
    elif type == "DISPLAY_DATA_SECTION":
        reading_weight = False
    elif type == "EOF":
        break

    if reading_city:
        coordinates.append([float(data[1]), float(data[2])])
    if reading_weight:
        weights.append(data)

    if type == "DISPLAY_DATA_SECTION":  # coordinates of each node
        reading_city = True

    if type == "EDGE_WEIGHT_SECTION":
        reading_weight = True

# initialize pheromone on every edge between the cities
pheromone = [[1000 for i in range(len(coordinates))] for j in range(len(coordinates))]

for i in range(len(coordinates)):
    for j in range(len(coordinates)):
        if i == j:
            pheromone[i][j] = 0

ant_col()
