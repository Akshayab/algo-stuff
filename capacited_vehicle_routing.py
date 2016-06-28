# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 14:30:18 2016

@author: akshaybudhkar
"""
import math

def calculate_euclidean_distance(A, B):
    x_diff = A[0] - B[0]
    y_diff = A[1] - B[1]
    return int(round(math.sqrt(x_diff*x_diff + y_diff*y_diff)))


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

print(min_vehicles)
print(dimension)
print(capacity)
print(coordinates)
print(demands)
print(depot)
print(calculate_euclidean_distance(depot, coordinates[1]))