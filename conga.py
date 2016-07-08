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

"""
Calculate the goodness of a move
Evaluation function: number of moves for player - number of moves for opponent
"""
def evaluation_function(board, player_stones, opponent_stones):
    score = 0
    for row, col in player_stones:
        for move in possible_moves:
            new_pos = (row + move[0], col + move[1])
            if is_legal_move(board, new_pos) and new_pos not in opponent_stones:
                score += 2
                
    for row, col in opponent_stones:
        for move in possible_moves:
            new_pos = (row + move[0], col + move[1])
            if is_legal_move(board, new_pos) and new_pos not in player_stones:
                score -=1
                
    return score
    
def evaluation_function_two(board, player_stones, opponent_stones):
    return len(player_stones) - len(opponent_stones)
        
# Move pieces from one square to another
def make_move(board, from_pos, to_pos, number, stones, color):
    print("Trying to move " + str(number) + " piece(s) from " + str(from_pos) + \
        " to " + str(to_pos))
    
    original_num = board[from_pos[0]][from_pos[1]][1]
    
    if number > 0:
        # Only move the stones there in the grid, not more
        if original_num < number:
            number = original_num
         
        # Update grid where the stones will be moved to
        if board[to_pos[0]][to_pos[1]][0] == color:
            board[to_pos[0]][to_pos[1]][1] += number
        else:
            board[to_pos[0]][to_pos[1]][0] = color
            board[to_pos[0]][to_pos[1]][1] = number

        stones.add(to_pos)
        
        # Update grid where the stones will be moved from
        board[from_pos[0]][from_pos[1]][1] -= number
        
        # If no stones left in the initial position
        if board[from_pos[0]][from_pos[1]][1] <= 0:
            board[from_pos[0]][from_pos[1]][0] = None
            board[from_pos[0]][from_pos[1]][1] = 0
            if from_pos in stones:
                stones.remove(from_pos)
            
        print(color + " moves " + str(number) + " piece(s) from " + str(from_pos) + \
        " to " + str(to_pos))
        
        # Did any stones move?
        return number > 0
    return False
        
def random_legal_move(board, color, player_stones, opponent_stones):
    print(color + "'s turn")
    
    random_stones = random.sample(player_stones, len(player_stones))
    
    for row, col in random_stones:
        # Randomize possible moves player can make
        random.shuffle(possible_moves)
        
        for move in possible_moves:
            new_pos = (row + move[0], col + move[1])
            num = board[row][col][1]
            
            if is_legal_move(board, new_pos):
                if new_pos not in opponent_stones:
                    second_pos = (new_pos[0] + move[0], new_pos[1] + move[1])
                    
                    if second_pos in opponent_stones or not(is_legal_move(board, second_pos)):                        
                        if make_move(board, (row, col), new_pos, num, player_stones, color):
                            return True
                    else:
                        third_pos = (second_pos[0] + move[0], second_pos[1] + move[1])
                        
                        if third_pos in opponent_stones or not(is_legal_move(board, third_pos)):
                            if make_move(board, (row, col), new_pos, 1, player_stones, color) or \
                            make_move(board, (row, col), second_pos, num - 1, player_stones, color):
                                return True
                        else:
                            if make_move(board, (row, col), new_pos, 1, player_stones, color) or \
                            make_move(board, (row, col), second_pos, 2, player_stones, color) or \
                            make_move(board, (row, col), third_pos, num - 3, player_stones, color):
                                return True


    print("No move possible, " + color + " lost")
    return False


"""
Evaluates function for the board with the potential moves of the player.
Returns the move with the least value (cause it is a Min)
"""
def get_child_with_best_evaluation(board, player_stones, opponent_stones, current_best):
    best_evaluation = float("inf")
    
    for row, col in opponent_stones:
        for move in possible_moves:
            new_pos = (row + move[0], col + move[1])

            if is_legal_move(board, new_pos) and new_pos not in player_stones:
                potential_stones = set(opponent_stones)
                potential_stones.add(new_pos)
                
                second_pos = (new_pos[0] + move[0], new_pos[1] + move[1])
                if second_pos not in player_stones and is_legal_move(board, second_pos):
                    potential_stones.add(second_pos)
                             
                    third_pos = (second_pos[0] + move[0], second_pos[1] + move[1])
                    
                    if third_pos not in player_stones and is_legal_move(board, third_pos):
                        potential_stones.add(third_pos)                        
                        
                evaluation = evaluation_function_two(board, player_stones, potential_stones)
                
                # Alpha prunning
                if evaluation < current_best:
                    return evaluation
                
                if evaluation < best_evaluation:
                    best_evaluation = evaluation
                    
    return best_evaluation
    
    
"""
Use MinMax strategy to calculate the best possible move
Use a depth limit of 2
"""
def smart_legal_move(board, color, opponent, player_stones, opponent_stones):
    print(color +"'s turn")
    best_move = []
    best_evaluation = -1*float("inf")
    for row, col in player_stones:
        for move in possible_moves:
            new_pos = (row + move[0], col + move[1])
            complete_move = []
            
            if is_legal_move(board, new_pos) and new_pos not in opponent_stones:
                potential_stones = set(player_stones)
                potential_stones.add(new_pos)
                
                complete_move.append((row, col))
                complete_move.append(new_pos)
                
                second_pos = (new_pos[0] + move[0], new_pos[1] + move[1])
                if second_pos not in opponent_stones and is_legal_move(board, second_pos):
                    potential_stones.add(second_pos)
                    
                    complete_move.append(second_pos)                    
                    third_pos = (second_pos[0] + move[0], second_pos[1] + move[1])
                    
                    if third_pos not in opponent_stones and is_legal_move(board, third_pos):
                        potential_stones.add(third_pos)                        
                        complete_move.append(third_pos)
                        
                evaluation = get_child_with_best_evaluation(board, potential_stones, opponent_stones, best_evaluation)
                
                if evaluation >= best_evaluation:
                    best_move = complete_move
                    best_evaluation = evaluation
                    
    if len(best_move) == 0:
        print("No move possible, " + color + " lost")
        return False
    else:
        num = board[best_move[0][0]][best_move[0][1]][1]
        if len(best_move) == 2:
            if make_move(board, best_move[0], best_move[1], num, player_stones, color):
                return True
        elif len(best_move) == 3:
            if make_move(board, best_move[0], best_move[1], 1, player_stones, color) or \
            make_move(board, best_move[0], best_move[2], num - 1, player_stones, color):
                return True
        elif len(best_move) == 4:
            if make_move(board, best_move[0], best_move[1], 1, player_stones, color) or \
            make_move(board, best_move[0], best_move[2], 2, player_stones, color) or \
            make_move(board, best_move[0], best_move[3], num - 3, player_stones, color):
                return True
                
    print("No move possible, " + color + " lost")
    return False
    
    
num_of_rows = 4
num_of_cols = 4

black_stone_positions = set()
white_stone_positions = set()

"""
board is a 2D Array corresponding to the grid locations on the playing board
Every grid location will consist of an array with the format:
["color of stone", # of stones]
"""
board = [[[None, 0] for i in range(num_of_cols)] for j in range(num_of_rows)]

# Initial setup
board[0][0] = ["black", 10]
board[3][3] = ["white", 10]

black_stone_positions.add((0, 0))
white_stone_positions.add((3, 3))

# Game playing
iterations = 0

while (random_legal_move(board, "white", white_stone_positions, black_stone_positions)):
    
    if smart_legal_move(board, "black", "white", black_stone_positions, white_stone_positions):
        print("")
    else:
        break
    
    iterations += 1
    
    print("")

    
print("White stone positions: " + str(white_stone_positions))
print("Black stone positions: " + str(black_stone_positions))

print("")
pretty_print(board)
print("It took " + str(iterations) + " iterations")