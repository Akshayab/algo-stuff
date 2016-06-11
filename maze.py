# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 15:55:09 2016

@author: Akshay Budhkar

ECE 457A - Assignment 2, Question 1
"""
import random

def pretty_print(matrix):
    for i in range(len(matrix)):
        print matrix[i]
        
def add_point(matrix, num):
    while True:
        random_row = random.randint(0, len(matrix) - 1)
        random_col = random.randint(0, len(matrix[0]) - 1)
        
        if matrix[random_row][random_col] == 0:
            matrix[random_row][random_col] = num
            break
    


num_of_rows = 25
num_of_cols = 25

"""
Use an array of arrays to represent a matrix
Let's use the following:
0 - Empty grid
1 - Wall/Obstacle
2 - S
3 - E1
4 - E2
"""
matrix = [[0 for x in range(num_of_cols)] for y in range(num_of_rows)]

# Add walls (try filling out ~30%)
for i in range(num_of_rows):
    for j in range(num_of_cols):
        if random.random() > 0.9:
            matrix[i][j] = 1


add_point(matrix, 2)
add_point(matrix, 3)
add_point(matrix, 4)

pretty_print(matrix)