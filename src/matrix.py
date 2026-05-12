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

def check_win(matrix, gridsize, target_num):
    full_board = True

    for r in range(gridsize):
        for c in range(gridsize):
            if matrix[r][c] == 0:
                full_board = False
                continue
            
            target = target_num
            
            if matrix[r][c] == 2:
                target = target_num * 2
            
            if target_num == 3:
                try:
                    if (matrix[r][c] + matrix[r][c+1] + matrix[r][c+2] == target and 
                        matrix[r][c+1] != 0 and matrix[r][c+2] != 0):
                        return 1
                except IndexError:
                    pass
                try:
                    if (matrix[r][c] + matrix[r+1][c] + matrix[r+2][c] == target and 
                        matrix[r+1][c] != 0 and matrix[r+2][c] != 0):
                        return 1
                except IndexError:
                    pass
                try:
                    if (matrix[r][c] + matrix[r+1][c+1] + matrix[r+2][c+2] == target 
                        and matrix[r+1][c+1] != 0 and matrix[r+2][c+2] != 0):
                        return 1
                except IndexError:
                    pass
                try:
                    if (matrix[r][c] + matrix[r+1][c-1] + matrix[r+2][c-2] == target and 
                        c - 2 >= 0 and matrix[r+1][c-1] != 0 and matrix[r+2][c-2] != 0):
                        return 1
                except IndexError:
                    pass

            elif target_num == 4:
                try:
                    if (matrix[r][c] + matrix[r][c+1] + matrix[r][c+2] + matrix[r][c+3] == target and 
                        matrix[r][c+1] != 0 and matrix[r][c+2] != 0 and matrix[r][c+3] != 0):
                        return 1
                except IndexError:
                    pass
                try:
                    if (matrix[r][c] + matrix[r+1][c] + matrix[r+2][c] + matrix[r+3][c] == target and 
                        matrix[r+1][c] != 0 and matrix[r+2][c] != 0 and matrix[r+3][c] != 0):
                        return 1
                except IndexError:
                    pass
                try:
                    if (matrix[r][c] + matrix[r+1][c+1] + matrix[r+2][c+2] + matrix[r+3][c+3] == target and 
                        matrix[r+1][c+1] != 0 and matrix[r+2][c+2] != 0 and matrix[r+3][c+3] != 0):
                        return 1
                except IndexError:
                    pass
                try:
                    if (matrix[r][c] + matrix[r+1][c-1] + matrix[r+2][c-2] + matrix[r+3][c-3] == target and 
                        c - 3 >= 0 and matrix[r+1][c-1] != 0 and matrix[r+2][c-2] != 0 and matrix[r+3][c-3] != 0):
                        return 1
                except IndexError:
                    pass                
            else:
                raise ValueError("target_num not 3 or 4")
    if full_board == True:
        return 2
    return 0