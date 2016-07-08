# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 14:30:18 2016

@author: akshaybudhkar
Solution to Question 5 of Assignment 2 - optimal is 661
Best so far, for :A-n33-k5.vrp is 1255, [[12, 22, 11, 19, 3, 29, 31], [13, 10, 7, 28, 25, 32], [18, 27, 20, 2, 24], [30, 17, 9, 1, 23], [21, 5], [15, 16, 6, 4, 8, 26], [14]]
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

def get_valid_random_solution(lst, min_split, no_of_splits, demands):
    valid = False
    
    while not valid:
        valid = True
        soln = list(get_random_solution(lst, min_split, no_of_splits))
        
        for i in range(len(soln)):
            total_demands = 0
            for j in range(len(soln[i])):
                total_demands += demands[soln[i][j]]
            
            if total_demands > 100:
                valid = False
                break

    return soln
    
def check_validity(soln, demands):
    for i in range(len(soln)):
        total_demands = 0
        for j in range(len(soln[i])):
            total_demands += demands[soln[i][j]]
        
        if total_demands > 100:
            return False

    return True
    
    
def get_valid_neighbor(init, min_vehicles, demands):
    valid = False
    final = []
    
    while not valid:
        current = init
        move_from = random.randint(0, len(current) - 1)
        
        # Ensure that we have at least one city left
        if current[move_from] == 1 and len(current) == min_vehicles:
            while len(current[move_from]) <= 1:
                move_from = random.randint(0, len(current) - 1)
            
        move_to = random.randint(0, len(current) - 1)
        
        # Ensure we move to a new route
        while move_from == move_to:
            move_to = random.randint(0, len(current))
            
        city_to_move = current[move_from][random.randint(0, len(current[move_from]) - 1)]
        current[move_from].remove(city_to_move)
                    
        if move_to == len(current):
            current.append([city_to_move])
        else:
            current[move_to].append(city_to_move)

        if len(current[move_from]) == 0:
            current.remove([])

        if check_validity(current, demands):
            valid = True
            final = current
    
    return final
    

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
    
    
def simulated_annealing(init, coordinates, demands, cities, min_vehicles):
    current = init
    current_cost = calculate_cost(init, coordinates)
    best = init
    best_cost = current_cost
    
    current_temp = 1000
    final_temp = 1
    alpha = 0.85
    max_iterations = 100
    
    while current_temp > final_temp:
        iterations = 0
        
        while iterations < max_iterations:
            nbr = get_valid_neighbor(current, min_vehicles, demands)
            nbr_cost = calculate_cost(nbr, coordinates)
            change = nbr_cost - current_cost
            
            # If it is better, we make that change my default
            if change < 0:
                current = nbr
                current_cost = nbr_cost
            else:
                x = random.random()
                if x < math.exp(-1*change/current_temp):
                    current = nbr
                    current_cost = nbr_cost
                    
            iterations += 1

        current_temp = current_temp*alpha
        
        if current_cost < best_cost:
            best = current
            best_cost = current_cost
            
        print(best_cost)
    
    return (best, best_cost)


file = open('A-n33-k5.vrp', 'r')

dimension = 0       # number of nodes, including depot
capacity = 0        # capacity of each vehicle
min_vehicles = 0    # min no of vehicles/routes

reading_node = False
reading_demand = False

# Every index is going to be a 2D coordinate for (i + 1)th node
# Eg: The first (0th) element contains coords for node 1
coordinates = []

# Every index depicts the demand for (i + 1)th node
# Eg: The first (0th) element contains coords for node 1
demands = []

for line in file: 
    data = line.split()
    type = data[0]

    if type == "NAME":                  # name of file for identification
        name = data[2]
        min_vehicles = int(name.split('-')[-1][-1])
    elif type == "DIMENSION":           # number of nodes, including depot
        dimension = int(data[2])
    elif type == "CAPACITY":            # capacity of each vehicle
        capacity = int(data[2])
    elif type == "DEMAND_SECTION":      # demand of all nodes
        reading_node = False
    elif type == "DEPOT_SECTION":       # list of all depot nodes
        reading_demand = False
        
    if reading_node:
        coordinates.append([int(data[1]),int(data[2])])
        
    if reading_demand:
        demands.append(int(data[1]))
    
    if type == "NODE_COORD_SECTION":    # coordinates of each node
        reading_node = True
    elif type == "DEMAND_SECTION":      # demand of all nodes
        reading_demand = True
        
depot = coordinates[0]
cities = [i + 1 for i in range(len(coordinates) - 1)] # Do not include the depot

init_soln = list(get_valid_random_solution(cities, 1, min_vehicles, demands))

print("Initial solution: " + str(init_soln))
print("Cost of initial solution: " + str(calculate_cost(init_soln, coordinates)))
print(simulated_annealing(init_soln, coordinates, demands, cities, min_vehicles))
