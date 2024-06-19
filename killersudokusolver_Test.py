import tkinter as tk
from tkinter import messagebox
import numpy as np
import time

class KillerSudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Killer Sudoku")
        self.board = np.zeros((9, 9), dtype=int)
        self.cages = {}
        self.create_widgets()
        self.counter = 0
        self.total = 0

    def create_widgets(self):
        self.entries = [[None]*9 for _ in range(9)]
        for i in range(9):
            for j in range(9):
                self.entries[i][j] = tk.Label(self.root, width=3, height=1, font=('Arial', 18), relief=tk.RIDGE, borderwidth=2)
                self.entries[i][j].grid(row=i, column=j)

        self.generate_killer_sudoku()
        self.display_cages()
        
        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=4, columnspan=2)

    def generate_killer_sudoku(self):
        self.cages = {
            ((0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (2, 1)): 34,
            ((0, 4), (1, 4), (1, 3)): 6,
            ((0, 5), (0, 6), (0, 7)): 17,
            ((0, 8), (1, 8), (2, 8), (3, 8), (3, 7), (3, 6), (2, 6)): 33,
            ((1, 1), (1, 2), (2, 2)): 16,
            ((2, 3), (2, 4), (3, 3)): 20,
            ((1, 5), (2, 5), (1, 6)): 14,
            ((1, 7), (2, 7)): 17,
            ((3, 0), (4, 0)): 11,
            ((3, 1), (4, 1)): 9,
            ((3, 2), (4, 2)): 3,
            ((5, 0), (6, 0), (7, 0), (8, 0), (5, 1), (5, 2), (6 ,2)): 41,
            ((3, 4), (4, 4), (3, 5), (4, 5)): 17,
            ((4, 3), (5, 3)): 11,
            ((5, 4), (5, 5), (5, 6), (4, 6)): 23,
            ((4, 7), (4, 8)): 13,
            ((5, 7), (5, 8)): 4,
            ((6, 1), (7, 1), (8, 1)): 10,
            ((8, 2), (8, 3)): 15,
            ((7, 2), (7, 3), (6, 3)): 16,
            ((6, 4), (7, 4), (8, 4)): 12,
            ((6, 7), (6, 8)): 16,
            ( (7, 6), (7, 7), (7, 8)): 9,
            ((6, 5), (6, 6), (7, 5), (8, 5), (8, 6), (8, 7), (8, 8)): 38,
        }

    def display_cages(self):
        colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightpink', 'lightcoral', 'lightgray', 'lightcyan', 'lightseagreen', 'lightsalmon', 'lightsteelblue']
        i = 0
        for cells, value in self.cages.items():
            for cell in cells:
                row, col = cell
                self.entries[row][col].config(bg=colors[i])
            sum_label = tk.Label(self.root, text=value, font=('Arial', 10))
            # Offset the sum label slightly to the top left corner of the cell
            sum_label.grid(row=cells[0][0], column=cells[0][1], sticky="nw")
            i = (i + 1) % len(colors)

    def update_gui(self):
        for i in range(9):
            for j in range(9):
                cell_text = str(self.board[i][j]) if self.board[i][j] != 0 else ''
                self.entries[i][j].config(text=cell_text)
        self.root.update()

    def ai_solve_process(self):
        empty_cell = self.find_empty_cell()

        if empty_cell is None:    
            return True
        
        row, col = empty_cell

        for num in range(1, 10):
            self.total += 1
            if self.is_safe(row, col, num):
                self.board[row][col] = num
                self.counter += 1

                if self.counter == 100000:
                    self.update_gui()
                    self.counter = 0

                if self.ai_solve_process():
                    return True
                
                self.board[row][col] = 0

        return False

    def solve(self):
        start_time = time.time()
        if self.ai_solve_process():
            end_time = time.time()
            print("Sudoku opgelost!")
            print(f"Aantal iteraties: {self.total}")
            print(f"Oplossing gevonden in {end_time - start_time:.2f} seconden.")
            self.update_gui()

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
                    # If the current cell being filled is the last one in the cage,
                    # ensure the sum equals the cage sum
                    return current_sum == cage_sum
                
                elif current_sum >= cage_sum:
                    return False
        
        return True

def main():
    root = tk.Tk()
    app = KillerSudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
