from matrix import *
import random

def cpu_easy_move(matrix, gridsize):
    empty_spaces = get_empty(matrix, gridsize)
    random_space = random.choice(empty_spaces)
    return random_space

def cpu_normal_move(matrix, gridsize):
    target_num = 0
    
    if gridsize == 4:
        target_num = 4
    else:
        target_num = 5
    
    empty_spaces = get_empty(matrix, gridsize)
    placed_o = get_placed_o(matrix, gridsize)
    
    if not placed_o:
        return cpu_easy_move(matrix, gridsize)
    
    possible_moves = {}
    directions = [(0, -1), (0, 1), (1, 0), (-1, 0), (1, 1), (-1, 1), (-1, -1), (1, -1)]
    
    for empty in empty_spaces:
        for dr, dc in directions:     
            move_score = 0
            if (empty[0] + dr, empty[1] + dc) in placed_o:
                move_score += 1
                if (empty[0] + (dr * 2), empty[1] + (dc * 2)) in placed_o:
                    move_score += 1
                    if (empty[0] + (dr * 3), empty[1] + (dc * 3)) in placed_o:
                        move_score += 1
                        if target_num == 5 and (empty[0] + (dr * 4), empty[1] + (dc * 4)) in placed_o:
                            move_score += 1
            if empty in possible_moves and possible_moves[empty] < move_score:
                possible_moves[empty] = move_score
            elif empty not in possible_moves:
                possible_moves[empty] = move_score

    if not possible_moves:
        return cpu_easy_move(matrix, gridsize)
    
    max_score = 0
    for empty in empty_spaces:
        try:
            if possible_moves[empty] > max_score:
                max_score = possible_moves[empty]
        except KeyError:
            pass
    best_moves = [k for k, v in possible_moves.items() if v == max_score]
    the_move = random.choice(best_moves)

    return the_move