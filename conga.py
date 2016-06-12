# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 12:50:32 2016

@author: akshaybudhkar

ECE 457A - Assignment 2, Question 2
"""
import random

# Possible range of moves
possible_moves = [[i, j] for i in range(-1, 2) for j in range(-1, 2) if (i, j) != (0, 0)]

def pretty_print(matrix):
    for i in range(len(matrix)):
        print matrix[i]

# Check if move is in bounds        
def is_legal_move(board, new_position):
    return new_position[0] >= 0 and new_position[0] < len(board) and \
    new_position[1] >= 0 and new_position[1] < len(board[0])
    
# Move pieces from one square to another
def make_move(board, from_pos, to_pos, number, stones):
    color = board[from_pos[0]][from_pos[1]][0]
    
    board[to_pos[0]][to_pos[1]][0] = color
    board[to_pos[0]][to_pos[1]][1] += number
    stones.add(to_pos)
    
    board[from_pos[0]][from_pos[1]][1] -= number
    
    # If no stones left in the initial position
    if board[from_pos[0]][from_pos[1]][1] == 0:
        board[from_pos[0]][from_pos[1]][0] = None
        stones.remove(from_pos)
        
def random_legal_move(board, color, player_stones, opponent_stones):    
    for row, col in player_stones:
        # Randomize possible moves player can make
        random.shuffle(possible_moves)
        
        for move in possible_moves:
            new_position = (row + move[0], col + move[1])
            
            if is_legal_move(board, new_position) and new_position not in opponent_stones:
                make_move(board, (row, col), new_position, 10, player_stones)
                return True
            else:
                continue
    return False


num_of_rows = 4
num_of_cols = 4

black_stone_positions = set()
white_stone_positions = set()

"""
board is a 2D Array corresponding to the grids on the playing board
Every grid will consist of an array with the format:
["color of stone", # of stones]
"""
board = [[[None, 0] for i in range(num_of_cols)] for j in range(num_of_rows)]

# Initial setup
board[0][0] = ["black", 10]
board[3][3] = ["white", 10]

black_stone_positions.add((0, 0))
white_stone_positions.add((3, 3))

random_legal_move(board, "white", white_stone_positions, black_stone_positions)
random_legal_move(board, "black", black_stone_positions, white_stone_positions)

pretty_print(board)

print(black_stone_positions)
print(white_stone_positions)