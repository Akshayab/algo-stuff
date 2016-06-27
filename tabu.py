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
            permut_flow_permut[j][instance[i]] = flow_col[j]
    
    for i in range(len(distance_arr)):
        for j in range(len(distance_arr[0])):
            cost += permut_flow_permut[i][j] + distance_arr[i][j]
            
    return cost
    
    

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

solution_instance = [i for i in range(20)]

# Shuffle for random initial solution
random.shuffle(solution_instance)

print(calculate_cost(solution_instance, flow_arr, distance_arr))
print(solution_instance)