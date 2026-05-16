import random

def matrix_set(r, c, matrix, current_player):
    if matrix[r][c] == 0 and current_player == 'x':
        matrix[r][c] = 1
        return True
    elif matrix[r][c] == 0 and current_player == 'o':
        matrix[r][c] = 2
        return True
    else:
        return False
    
def print_matrix(matrix):
    for row in matrix:
        print(row)

def flip_pieces(matrix, gridsize):
    for r in range(gridsize):
        for c in range(gridsize):
            if matrix[r][c] == 1:
                matrix[r][c] = 2
            elif matrix[r][c] == 2:
                matrix[r][c] = 1

def drop_pieces(matrix, gridsize):
    for r in range(gridsize - 2, -1, -1):
        for c in range(gridsize):
            if matrix[r][c] == 0 or matrix[r][c] == 3:
                continue
            drop_zone = None
            for drop in range(r + 1, gridsize):
                if matrix[drop][c] == 0:
                    drop_zone = drop
                else:
                    break
            if drop_zone != None:
                matrix[drop_zone][c] = matrix[r][c]
                matrix[r][c] = 0

def lift_pieces(matrix, gridsize):
    for r in range(gridsize):
        for c in range(gridsize):
            if matrix[r][c] == 0 or matrix[r][c] == 3:
                continue
            lift_zone = None
            for lift in range(r - 1, -1, -1):
                if matrix[lift][c] == 0:
                    lift_zone = lift
                else:
                    break
            if lift_zone != None:
                matrix[lift_zone][c] = matrix[r][c]
                matrix[r][c] = 0

def push_left(matrix, gridsize):
    for r in range(gridsize):
        for c in range(gridsize):
            if matrix[r][c] == 0 or matrix[r][c] == 3:
                continue
            if c >= gridsize / 2:
                continue  
            split_zone = None
            for split in range(c - 1, -1, -1):
                if matrix[r][split] == 0:
                    split_zone = split
                else:
                    break
            if split_zone != None:
                matrix[r][split_zone] = matrix[r][c]
                matrix[r][c] = 0

def push_right(matrix, gridsize):
    for r in range(gridsize):
        for c in range(gridsize - 2, -1, -1):
            if matrix[r][c] == 0 or matrix[r][c] == 3:
                continue
            if c < gridsize / 2:
                continue
            split_zone = None
            for split in range(c + 1, gridsize):
                if matrix[r][split] == 0:
                    split_zone = split
                else:
                    break
            if split_zone != None:
                matrix[r][split_zone] = matrix[r][c]
                matrix[r][c] = 0

def split_pieces(matrix, gridsize):
    push_left(matrix, gridsize)
    push_right(matrix, gridsize)

def place_rock(matrix, gridsize):
    empty_spots = get_empty(matrix, gridsize)
    rock_spot = random.choice(empty_spots)
    matrix[rock_spot[0]][rock_spot[1]] = 3

def place_piece(matrix, gridsize):
    empty_spots = get_empty(matrix, gridsize)
    place_space = random.choice(empty_spots)
    number = random.randint(1, 2)
    matrix[place_space[0]][place_space[1]] = number

def delete_random(matrix, gridsize):
    placed_spaces = get_placed(matrix, gridsize)
    random_spot = random.choice(placed_spaces)
    matrix[random_spot[0]][random_spot[1]] = 0

def shuffle_pieces(matrix, gridsize):
    x_list = []
    o_list = []
    for r in range(gridsize):
        for c in range(gridsize):
            if matrix[r][c] == 1:
                x_list.append(1)
                matrix[r][c] = 0
            elif matrix[r][c] == 2:
                o_list.append(2)
                matrix[r][c] = 0
    empty_spaces = get_empty(matrix, gridsize)
    while x_list or o_list:
        random_space = random.choice(empty_spaces)
        random_piece = random.randint(1, 2)
        if random_piece == 1 and x_list:
            matrix[random_space[0]][random_space[1]] = x_list.pop()
            empty_spaces.remove(random_space)
        elif random_piece == 2 and o_list:
            matrix[random_space[0]][random_space[1]] = o_list.pop()
            empty_spaces.remove(random_space)

def move_piece(matrix, gridsize):
    placed = get_placed(matrix, gridsize)
    empty_spaces = get_empty(matrix, gridsize)
    piece = random.choice(placed)
    new_space = random.choice(empty_spaces)
    matrix[new_space[0]][new_space[1]] = matrix[piece[0]][piece[1]]
    matrix[piece[0]][piece[1]] = 0
    
def delete_half(matrix, gridsize):
    placed = get_placed(matrix, gridsize)
    number_pieces = len(placed)
    while len(placed) > number_pieces // 2:
        random_piece = random.choice(placed)
        matrix[random_piece[0]][random_piece[1]] = 0
        placed.remove(random_piece)

def get_empty(matrix, gridsize) -> list[tuple[int, int]]:
    empty_spots = []
    for r in range(gridsize):
        for c in range(gridsize):
            if matrix[r][c] == 0:
                empty_spots.append((r, c))
    return empty_spots

def get_placed(matrix, gridsize) -> list[tuple[int, int]]:
    placed_spots = []
    for r in range(gridsize):
        for c in range(gridsize):
            if matrix[r][c] != 0 and matrix[r][c] != 3:
                placed_spots.append((r, c))
    return placed_spots

def get_placed_o(matrix, gridsize) -> list[tuple[int, int]]:
    placed_spots = []
    for r in range(gridsize):
        for c in range(gridsize):
            if matrix[r][c] == 2:
                placed_spots.append((r, c))
    return placed_spots

def check_full(matrix, gridsize):
    full_board = True

    for r in range(gridsize):
        for c in range(gridsize):
            if matrix[r][c] == 0:
                full_board = False
            
    if full_board == True:
        return True
    return False