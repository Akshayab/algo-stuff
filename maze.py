# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 15:55:09 2016

@author: Akshay Budhkar

ECE 457A - Assignment 2, Question 1
"""
import random
from collections import deque

def pretty_print(matrix):
    for i in range(len(matrix)):
        print matrix[i]
        
def add_point(matrix, num):
    while True:
        random_row = random.randint(0, len(matrix) - 1)
        random_col = random.randint(0, len(matrix[0]) - 1)
        
        if matrix[random_row][random_col] == 0:
            matrix[random_row][random_col] = num
            return (random_row, random_col)

# Convert matrix to a graph for traversal purposes
def maze_to_graph(matrix):
    # Create a graph (going outwards) with no neighbors
    row_max = len(matrix)
    col_max = len(matrix[0])
    graph = {(i, j): [] for i in range(row_max) for j in range(col_max) if matrix[i][j] != 1}
    
    # Add the neighbors
    for row, col in graph.keys():
        if row < row_max - 1 and matrix[row + 1][col] != 1:
            graph[(row, col)].append(("N", (row + 1, col)))
            graph[(row + 1, col)].append(("S", (row, col)))
            
        if col < col_max - 1 and matrix[row][col + 1] != 1:
            graph[(row, col)].append(("E", (row, col + 1)))
            graph[(row, col + 1)].append(("W", (row, col)))
            
    return graph
    
    
def find_bfs_path(graph, start, end_one, end_two):
    # Make a queue which stores the node and the path to the node
    queue = deque([(start, "")])
    visited = set() # All visited nodes
    
    while queue:
        current, path = queue.popleft()
        
        if current == end_one or current == end_two:
            return path[1:]
        
        if current in visited:
            continue
        visited.add(current)

        for direction, node in graph[current]:
            queue.append((node, path + "-" + direction))
            
    return "There is no way from start to end"
    
def find_dfs_path(graph, start, end_one, end_two):
    # Make a stack which stores the node and the path to the node
    stack = deque([(start, "")])
    visited = set() # All visited nodes
    
    while stack:
        current, path = stack.pop()
        
        if current == end_one or current == end_two:
            return path[1:]
        
        if current in visited:
            continue
        visited.add(current)

        for direction, node in graph[current]:
            stack.append((node, path + "-" + direction))
            
    return "There is no way from start to end"
        
        
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


start = add_point(matrix, 2)
end_one = add_point(matrix, 3)
end_two = add_point(matrix, 4)

graph = maze_to_graph(matrix)

print((start, end_one, end_two))
print(find_bfs_path(graph, start, end_one, end_two))

print((start, end_one, end_two))
print(find_dfs_path(graph, start, end_one, end_two))