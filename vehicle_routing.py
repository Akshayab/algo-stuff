# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 11:58:24 2016

@author: akshaybudhkar
Solution to Question 4 of Assignment 2
Best result so far for 9 cities, 3 vehicles:
([[1, 8, 3], [7], [5, 4, 2, 0, 6]], [[1, 8, 3], [7], [5, 4, 2, 0, 6]], 163)
"""
import random
import math
from itertools import islice

def get_random_solution(lst, min_split, no_of_splits):
    random.shuffle(lst)
    size = len(lst)
    itr = iter(lst)
    
    for i in range(no_of_splits - 1, 0, -1):
        s = random.randint(min_split, size - i*min_split)
        yield list(islice(itr,0,s))
        size -= s
    yield list(itr)


def calculate_cost(solution, depot, distance, service):
    cost = 0
    # Service times in each city are added
    for time in service:
        cost += time
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            current = solution[i][j]
            # Cost from/to the depot
            if j == 0 or j == (len(solution[i]) - 1):
                cost += depot[current]
            
            # Cost between cities
            if j != (len(solution[i]) - 1):
                nxt = solution[i][j+1]
                cost += distance[current][nxt]
                
    return cost
    
"""
Neighborhood Definition Rules:
- You can move a city from one route to another
- When a city is added to a new route, it is always added at the end
- Do not move the city if it is the only one serviced by the vehicle
- You cannot switch cities in the same route
- It doesn't provide as much diversification
"""

def get_random_neighbor(solution): 
    move_from = random.randint(0, len(solution) - 1)
    
    # Ensure we only move from a route with more than one city
    while len(solution[move_from]) <= 1:
        move_from = random.randint(0, len(solution) - 1)
        
    move_to = random.randint(0, len(solution) - 1)
    
    # Ensure we move to a different route
    while move_to == move_from:
        move_to = random.randint(0, len(solution) - 1)
        
    city_to_move = solution[move_from][random.randint(0, len(solution[move_from]) - 1)]
    solution[move_from].remove(city_to_move)
    
    solution[move_to].append(city_to_move)
    
    return solution
    
def simulated_annealing(solution, depot, distance, service):
    current = solution
    current_cost = calculate_cost(current, depot, distance, service)
    best = solution
    best_cost = current_cost
    
    current_temp = 500
    final_temp = 1
    alpha = 0.85
    max_iterations = 100
    
    flop_iterations = 0
    
    while current_temp > final_temp and flop_iterations < 5000:
        iterations = 0
        
        while iterations < max_iterations:
            nbr = get_random_neighbor(current)
            nbr_cost = calculate_cost(nbr, depot, distance, service)
            change = nbr_cost - current_cost
            
            # If we improve, make that change
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
            flop_iterations = 0
            best_cost = current_cost
            best = current
        else:
            flop_iterations += 1
            
        print(best_cost)
    
    return (best, best_cost)
        
# Note: vehicles and cities are zero indexed
vehicles = 3
cities = 9

Depot = [random.randint(5, 50) for i in range(cities)]
D = [[0 for i in range(cities)] for j in range(cities)]
service_times = [random.randint(5, 50) for i in range(cities)]

# Values of the distances in the cities must be symmetric
for i in range(len(D)):
    for j in range(len(D[0])):
        if D[i][j] == 0:
            value = random.randint(5, 50)
            D[i][j] = value
            D[j][i] = value
        if i == j:
            D[i][j] = 0

"""
Solution Definition:
The solution is defined as a list of lists. The number of sub-lists is equal to the number of vehicles.
The elements in each sub-list represent the cities being serviced by that vehicle. The order of elements in the list
defines the order in which the cities are serviced by that vehicle. Since this is a permutation problem, an element
will only occur once i.e. in only one of the sub-lists.
"""
init_soln = list(get_random_solution(range(cities), 1, vehicles))

print("Initial solution: " + str(init_soln))
print("Cost of initial solution: " + str(calculate_cost(init_soln, Depot, D, service_times)))

nbr = get_random_neighbor(init_soln)

print(simulated_annealing(init_soln, Depot, D, service_times))