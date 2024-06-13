import numpy as np
import time

class KillerSudokuSolver:
    def __init__(self):
        self.board = np.zeros((9, 9), dtype=int)
        self.cages = self.generate_killer_sudoku()

    def generate_killer_sudoku(self):
        return {
            ((0, 0), (0, 1)): 3,
            ((0, 2), (0, 3), (0, 4)): 15,
            ((0, 5), (1, 5), (1, 4), (2, 4)): 22,
            ((0, 6), (1, 6)): 4,
            ((0, 7), (1, 7)): 16,
            ((0, 8), (1, 8), (2, 8), (3, 8)): 15,
            ((1, 0), (1, 1), (2, 0), (2, 1)): 25,
            ((1, 2), (1, 3)): 17,
            ((2, 2), (2, 3), (3, 3)): 9,
            ((2, 5), (3, 5), (4, 5)): 8,
            ((2, 6), (2, 7), (3, 6)): 20,
            ((3, 0), (4, 0)): 6,
            ((3, 1), (3, 2)): 14,
            ((3, 4), (4, 4), (5, 4)): 17,
            ((3, 7), (4, 7), (4, 6)): 17,
            ((4, 1), (4, 2), (5, 1)): 13,
            ((4, 3), (5, 3), (6, 3)): 20,
            ((4, 8), (5, 8)): 12,
            ((5, 0), (6, 0), (7, 0), (8, 0)): 27,
            ((5, 2), (6, 2), (6, 1)): 6,
            ((5, 5), (6, 5), (6, 6)): 20,
            ((5, 6), (5, 7)): 6,
            ((6, 4), (7, 4), (7, 3), (8, 3)): 10,
            ((6, 7), (6, 8), (7, 7), (7, 8)): 14,
            ((7, 1), (8, 1)): 8,
            ((7, 2), (8, 2)): 16,
            ((7, 5), (7, 6)): 15,
            ((8, 4), (8, 5), (8, 6)): 13,
            ((8, 7), (8, 8)): 17
        }

    def solve(self):
        if self.ai_solve_process():
            self.log_solution()
        else:
            print("No solution exists.")

    def ai_solve_process(self):
        empty_cell = self.find_empty_cell()
        if empty_cell is None:
            return True
        
        row, col = empty_cell

        for num in range(1, 10):
            if self.is_safe(row, col, num):
                self.board[row][col] = num
                if self.ai_solve_process():
                    return True
                
                self.board[row][col] = 0

        return False

    def find_empty_cell(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None
    
    def is_safe(self, row, col, num):
        return (
            self.is_row_safe(row, num) and
            self.is_col_safe(col, num) and
            self.is_box_safe(row - row % 3, col - col % 3, num) and
            self.check_cage_constraint(row, col, num)
        )

    def is_row_safe(self, row, num):
        return num not in self.board[row]

    def is_col_safe(self, col, num):
        return num not in [self.board[i][col] for i in range(9)]

    def is_box_safe(self, start_row, start_col, num):
        for i in range(3):
            for j in range(3):
                if self.board[i + start_row][j + start_col] == num:
                    return False
        return True
    
    def check_cage_constraint(self, row, col, num):
        for cage_cells, cage_sum in self.cages.items():
            if (row, col) in cage_cells:
                current_sum = sum(self.board[r][c] for r, c in cage_cells if self.board[r][c] != 0) + num
                
                if len([1 for r, c in cage_cells if self.board[r][c] == 0]) == 1:
                    return current_sum == cage_sum
                
                elif current_sum >= cage_sum:
                    return False
        
        return True

    def log_solution(self):
        print("Killer Sudoku Solved:")
        for row in self.board:
            print(" ".join(map(str, row)))

def main():
    solver = KillerSudokuSolver()
    solver.solve()

if __name__ == "__main__":
    main()
