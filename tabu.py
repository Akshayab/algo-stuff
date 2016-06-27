# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 10:59:15 2016

@author: akshaybudhkar
"""
import csv

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

print(tabu_matrix)