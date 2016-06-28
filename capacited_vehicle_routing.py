# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 14:30:18 2016

@author: akshaybudhkar
Solution to Question 5 of Assignment 2
"""
import math
import random
from itertools import islice

def calculate_euclidean_distance(A, B):
    x_diff = A[0] - B[0]
    y_diff = A[1] - B[1]
    return int(round(math.sqrt(x_diff*x_diff + y_diff*y_diff)))
    

def get_random_solution(lst, min_split, no_of_splits):
    random.shuffle(lst)
    size = len(lst)
    itr = iter(lst)
    
    for i in range(no_of_splits - 1, 0, -1):
        s = random.randint(min_split, size - i*min_split)
        yield list(islice(itr,0,s))
        size -= s
    yield list(itr)
    

def calculate_cost(solution, coordinates):
    cost = 0
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            current = solution[i][j]
            
            #Cost from depot
            if j == 0 or j == (len(solution[i]) - 1):
                cost += calculate_euclidean_distance(coordinates[0], coordinates[current])
            
            #Cost between cities
            if j != (len(solution[i]) - 1):
                nxt = solution[i][j+1]
                cost += calculate_euclidean_distance(coordinates[nxt], coordinates[current])

    return cost


file = open('A-n32-k5.vrp', 'r')

dimension = 0
capacity = 0
min_vehicles = 0

reading_node = False
reading_demand = False

# Every index is going to be a 2D coordinate for node# (i + 1)
coordinates = []

# Every index depicts capacity for node# (i + 1)
demands = []

for line in file: 
    data = line.split()
    type = data[0]
    
    if type == "NAME":
        name = data[2]
        min_vehicles = int(name.split('-')[-1][-1])
    elif type == "DIMENSION":
        dimension = int(data[2])
    elif type == "CAPACITY":
        capacity = int(data[2])
    elif type == "DEMAND_SECTION":
        reading_node = False
    elif type == "DEPOT_SECTION":
        reading_demand = False
        
    if reading_node:
        coordinates.append([int(data[1]),int(data[2])])
        
    if reading_demand:
        demands.append(int(data[1]))
    
    if type == "NODE_COORD_SECTION":
        reading_node = True
    elif type == "DEMAND_SECTION":
        reading_demand = True
        
depot = coordinates[0]
cities = [i + 1 for i in range(len(coordinates) - 1)] # Do not include the depot

init_soln = list(get_random_solution(cities, 1, min_vehicles))

print(init_soln)
print(calculate_cost(init_soln, coordinates))
