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
            if matrix[r][c] != 0:
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
            if matrix[r][c] != 0:
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
            if matrix[r][c] != 0:
                if c < gridsize / 2:
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
            if matrix[r][c] != 0:
                if c >= gridsize / 2:
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

def check_full(matrix, gridsize):
    full_board = True

    for r in range(gridsize):
        for c in range(gridsize):
            if matrix[r][c] == 0:
                full_board = False
            
    if full_board == True:
        return True
    return False