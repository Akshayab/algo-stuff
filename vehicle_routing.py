# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 11:58:24 2016

@author: akshaybudhkar
Solution to Question 4 of Assignment 2
"""
import random
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

# Note: vehicles are cities are zero indexed
vehicles = 3
cities = 9

Depot = [random.randint(5, 50) for i in range(cities)]
D = [[0 for i in range(cities)] for j in range(cities)]

# Values of the distances in the cities much be symmetric
for i in range(len(D)):
    for j in range(len(D[0])):
        if D[i][j] == 0:
            value = random.randint(5, 50)
            D[i][j] = value
            D[j][i] = value

"""
Solution Definition:
Consider a solution to be a 2D Matrix with row n representing the cities
serviced by vehicle n. Every row will have the cities processed in order
"""
init_soln = get_random_solution(range(cities), 1, vehicles)

print(list(init_soln))
