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
def make_move(board, from_pos, to_pos, number, stones, color):
    if number > 0:
        board[to_pos[0]][to_pos[1]][0] = color
        board[to_pos[0]][to_pos[1]][1] += number
        stones.add(to_pos)
        
        board[from_pos[0]][from_pos[1]][1] -= number
        
        # If no stones left in the initial position
        if board[from_pos[0]][from_pos[1]][1] == 0:
            board[from_pos[0]][from_pos[1]][0] = None
            stones.remove(from_pos)
            
        print(color + " moves " + str(number) + " pieces from " + str(from_pos) + \
        " to " + str(to_pos))
        
def random_legal_move(board, color, player_stones, opponent_stones):    
    print(color + "'s turn")
    
    for row, col in player_stones:
        # Randomize possible moves player can make
        random.shuffle(possible_moves)
        
        for move in possible_moves:
            new_pos = (row + move[0], col + move[1])
            num = board[row][col][1]
            
            if is_legal_move(board, new_pos):
                if new_pos not in opponent_stones:
                    second_pos = (new_pos[0] + move[0], new_pos[1] + move[1])
                    
                    if second_pos in opponent_stones or not(is_legal_move(board, second_pos)):                        
                        make_move(board, (row, col), new_pos, num, player_stones, color)
                        return True
                    else:
                        third_pos = (second_pos[0] + move[0], second_pos[1] + move[1])
                        
                        if third_pos in opponent_stones or not(is_legal_move(board, third_pos)):
                            make_move(board, (row, col), new_pos, 1, player_stones, color)
                            make_move(board, (row, col), second_pos, num - 1, player_stones, color)
                            return True
                        else:
                            make_move(board, (row, col), new_pos, 1, player_stones, color)
                            make_move(board, (row, col), second_pos, 2, player_stones, color)
                            make_move(board, (row, col), third_pos, num - 3, player_stones, color)
                            return True


    print("No move possible, " + color + " lost")
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

# Random playing

colors = ["white", "black"]
positions = [white_stone_positions, black_stone_positions]

index = 0
other_index = 2 - index - 1

while (random_legal_move(board, colors[index], positions[index], positions[other_index])):
    index += 1
    index = index % 2
    other_index = 2 - index - 1
    print("")

    
print(white_stone_positions)
print(black_stone_positions)

print("")
pretty_print(board)