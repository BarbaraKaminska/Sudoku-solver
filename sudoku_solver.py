import numpy as np
from itertools import product

class InvalidBoardException(Exception):
    pass



class SudokuSolver:

    SIZE = 9
    BOX_SIZE = 3
    DIGITS = set(i for i in range(1, SIZE+1))
    
    def __init__(self, board):
        self.board = board 
        

    def solve (self):
        try:
            if self.is_valid():
                print("solution found")
                return True

            position = self.find_empty()
            if not position:
                if not self.is_valid():
                    raise InvalidBoardException
                return True
            else:
                row, col = position
                unused_digits = self.get_candidates(row, col)
            for i in unused_digits:
                self.board[row][col] = i

                if self.solve():
                    return True
                else:
                    self.board[row][col] = 0
            return False

        except:
            print("Invalid board")
            return

    def get_candidates(self, row, col):
            box_coord = lambda x : (x//self.BOX_SIZE)*self.BOX_SIZE
            box_r = box_coord(row)
            box_c = box_coord(col)
            used_digits = set()
            used_digits.update(set(self.board[row]))
            used_digits.update(set(self.board[:, col]))
            used_digits.update(set(self.board[box_r:box_r+self.BOX_SIZE, box_c:box_c+self.BOX_SIZE].flatten()))
            used_digits.update({0})
            return list(self.DIGITS.difference(used_digits))


    def find_empty(self):
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid (self):
        for col in self.get_columns(self.board):
            if col != self.DIGITS:
                return False
        for row in self.get_rows(self.board):
            if row != self.DIGITS:
                return False
        for box in self.get_boxes(self.board):
            if box != self.DIGITS:
                return False
        return True

    def get_columns(self, board):
        return [set(board[:, i]) for i in range(self.SIZE)]

    def get_rows(self, board):
        return [set(board[i]) for i in range(self.SIZE)] 

    def get_boxes(self, board):
        res = []
        for r, c in product(range(self.BOX_SIZE), repeat=2):
            box_coord = lambda x : (x//self.BOX_SIZE)*self.BOX_SIZE
            box_r = box_coord(r)
            box_c = box_coord(c)
            res.append(set(board[box_r:(box_r+self.BOX_SIZE), box_c:(box_c+self.BOX_SIZE)].flatten()))
        return res 

    def print_board(self):
        for i in range(self.SIZE):
            if i%self.BOX_SIZE == 0:
                print("- - - - - - - - - - - - -")
            for j in range(self.SIZE):
                if j%self.BOX_SIZE == 0 and j>0:
                    print(" | ", end=" ")
                if j == self.SIZE - 1:
                    print(self.board[i][j])
                else:
                    print(self.board[i][j], end=" ")

if __name__ == '__main__':
    init = np.array([
                        [7,8,0,4,0,0,1,2,0],
                        [6,0,0,0,7,5,0,0,9],
                        [0,0,0,6,0,1,0,7,8],
                        [0,0,7,0,4,0,2,6,0],
                        [0,0,1,0,5,0,9,3,0],
                        [9,0,4,0,6,0,0,0,5],
                        [0,7,0,3,0,0,0,1,2],
                        [1,2,0,0,0,7,4,0,0],
                        [0,4,9,2,0,6,0,7,7]
    ])
    Solver = SudokuSolver(init)
    
    Solver.print_board()
    Solver.solve()
 #   print(Solver.is_valid())
    print("-------------------------")
    Solver.print_board()
