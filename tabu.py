# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 10:59:15 2016

@author: akshaybudhkar
"""
import csv
import random

def get_column(index, matrix):
    return [row[index] for row in matrix]

def calculate_cost(instance, flow_arr, distance_arr):
    permutation_flow = [[0 for i in range(20)] for j in range(20)]
    cost = 0
        
    for i in range(len(instance)):
        permutation_flow[i] = flow_arr[instance[i]]
    
    permut_flow_permut = [[0 for i in range(20)] for j in range(20)]
    
    for i in range(len(instance)):
        flow_col = get_column(instance[i], permutation_flow)
        
        for j in range(len(permut_flow_permut)):
            permut_flow_permut[j][i] = flow_col[j]
    
    for i in range(len(distance_arr)):
        row_cost = 0
        for j in range(len(distance_arr[0])):
            row_cost += permut_flow_permut[i][j] * distance_arr[i][j]
        
        cost += row_cost
            
    return cost
    
    
def get_most_optimal_neighbor(instance, flow_arr, distance_arr, tabu_matrix, tabu_size):
    best_cost = float("inf")
    best_instance = None
    
    for i in range(len(instance)):
        for j in range(len(instance)):
            if i != j:
                new_instance = instance[:]
                new_instance[i], new_instance[j] = new_instance[j], new_instance[i]
                new_cost = calculate_cost(new_instance, flow_arr, distance_arr)
                
                # Check if better than best so far and if not tabued
                if new_cost < best_cost and tabu_matrix[new_instance[i]][i] == 0 \
                and tabu_matrix[new_instance[j]][j] == 0:
                    best_cost = new_cost
                    best_instance = new_instance
                    tabu_matrix[new_instance[j]][j] = tabu_size
                    tabu_matrix[new_instance[i]][i] = tabu_size
    
    print best_cost
    return best_instance
    
def decrement_tabu(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] > 0:
                matrix[i][j] -= 1
    return matrix

def tabu_search(instance, flow_arr, distance_arr, tabu_matrix):
    current = instance
    best_cost = calculate_cost(current, flow_arr, distance_arr)
    iterations = 0
    tabu_size = random.randint(4, 14)
    
    while calculate_cost(current, flow_arr, distance_arr) > 2570 and iterations < 500:
        current = get_most_optimal_neighbor(current, flow_arr, distance_arr, tabu_matrix, tabu_size)
        tabu_matrix = decrement_tabu(tabu_matrix)
        iterations += 1
        if iterations % 50 == 0:
            tabu_size = random.randint(4, 14)
        
        if calculate_cost(current, flow_arr, distance_arr) < best_cost:
            best_cost = calculate_cost(current, flow_arr, distance_arr)
        
    return {'cost': calculate_cost(current, flow_arr, distance_arr),
            'iterations': iterations,
            'instance': current,
            'best': best_cost}
    
# Initial flow and distance arrays setup
flow_file = open('flow.csv', 'r')
distance_file = open('distance.csv', 'r')

flow_arr = []
distance_arr = []

flow_reader = csv.reader(flow_file)
distance_reader = csv.reader(distance_file)

for row in flow_reader:
    flow_arr.append([int(x) for x in row])

for row in distance_reader:
    distance_arr.append([int(x) for x in row])    

""" 
Initial tabu structure
Defined as departments as rows and locations as columns (a 2D Dimensional Array)
"""
tabu_matrix = [[0 for i in range(20)] for j in range(20)]

init_soln = [i for i in range(20)]

# Shuffle for random initial solution
random.shuffle(init_soln)

print(init_soln)
print(tabu_search(init_soln, flow_arr, distance_arr, tabu_matrix))