import tkinter as tk
from tkinter import messagebox
import numpy as np
import time

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.value = 0
        self.possibleValues = [1, 2, 3, 4, 5, 6, 7, 8, 9]


    def remove_possible_value(self, value: int):
        if value in self.possibleValues:
            self.possibleValues.remove(value)

    def add_possible_value(self, value: int):
        if value not in self.possibleValues:
            self.possibleValues.append(value)
       

class KillerSudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Killer Sudoku")
        self.board = np.zeros((9, 9), dtype=object)
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
                self.board[i][j] = Cell(i, j)

        self.generate_killer_sudoku()
        self.display_cages()
        
        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=4, columnspan=2)

    def generate_killer_sudoku(self):
        self.cages = {
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
                cell_text = str(self.board[i][j].value) if self.board[i][j].value != 0 else ''
                self.entries[i][j].config(text=cell_text)
        self.root.update()

    def arc_consistency(self, cell: Cell):
        # remove the value from the possible values of all cells in the same row
        for c in self.board[cell.row]:
            c.remove_possible_value(cell.value)

        # remove the value from the possible values of all cells in the same column
        for r in range(9):
            self.board[r][cell.col].remove_possible_value(cell.value)

        # remove the value from the possible values of all cells in the same box
        start_row, start_col = cell.row - cell.row % 3, cell.col - cell.col % 3
        for i in range(3):
            for j in range(3):
                self.board[i + start_row][j + start_col].remove_possible_value(cell.value)


    def reset_possible_values(self, cell: Cell, num: int):
        # add the value back to the possible values of all cells in the same row
        for c in self.board[cell.row]:
            c.add_possible_value(num)

        # add the value back to the possible values of all cells in the same column
        for r in range(9):
            self.board[r][cell.col].add_possible_value(num)

        # add the value back to the possible values of all cells in the same box
        start_row, start_col = cell.row - cell.row % 3, cell.col - cell.col % 3
        for i in range(3):
            for j in range(3):
                self.board[i + start_row][j + start_col].add_possible_value(num)
        

    def ai_solve_process(self):
        empty_cell = self.find_empty_cell()
        if empty_cell is None:
            print(f"Total: {self.total}")
            self.update_gui()
            return True
        
        cell = empty_cell
        row, col = cell.row, cell.col

        for num in cell.possibleValues:
            if self.is_safe(row, col, num):
                self.board[row][col].value = num
                self.arc_consistency(self.board[row][col])

                self.counter += 1
                self.total += 1

                if self.counter == 100000:
                    self.update_gui()
                    self.counter = 0

                if self.ai_solve_process():
                    return True
                
                self.board[row][col].value = 0
                self.reset_possible_values(cell, num)

        return False

    def solve(self):
        self.ai_solve_process()

    def find_empty_cell(self) -> Cell:
        for i in range(9):
            for j in range(9):
                if self.board[i][j].value == 0:
                    return self.board[i][j]
        return None
    
    def is_safe(self, row, col, num):
        return (
            self.is_row_safe(row, num) and
            self.is_col_safe(col, num) and
            self.is_box_safe(row - row % 3, col - col % 3, num) and
            self.check_cage_constraint(row, col, num)
        )

    def is_row_safe(self, row: int, num: int):
        # Check if the number is not present in the row
        return num not in [cell.value for cell in self.board[row]]

    def is_col_safe(self, col, num):
        # Check if the number is not present in the column
        return num not in [self.board[i][col].value for i in range(9)]

    def is_box_safe(self, start_row, start_col, num):
        for i in range(3):
            for j in range(3):
                if self.board[i + start_row][j + start_col] == num:
                    return False
        return True
    
    def check_cage_constraint(self, row, col, num):
        for cage_cells, cage_sum in self.cages.items():
            if (row, col) in cage_cells:
                current_sum = sum(self.board[r][c].value for r, c in cage_cells if self.board[r][c].value != 0) + num
                
                if len([1 for r, c in cage_cells if self.board[r][c].value == 0]) == 1:
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
