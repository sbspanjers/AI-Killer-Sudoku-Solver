import tkinter as tk
import numpy as np
import time
from collections import defaultdict

class KillerSudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Killer Sudoku")
        self.board = np.zeros((9, 9), dtype=int)  # Sudoku board initialized with zeros
        self.cages = {}  # Dictionary to store cage configurations
        self.create_widgets()
        self.counter = 0
        self.total_counter = 0
        # Initialize remaining values for each cell with all possible values (1-9)
        self.remaining_values = {(i, j): set(range(1, 10)) for i in range(9) for j in range(9)}
        # Sets to keep track of used values in rows, columns, and boxes
        self.row_values = [set() for _ in range(9)]
        self.col_values = [set() for _ in range(9)]
        self.box_values = [set() for _ in range(9)]

    def create_widgets(self):
        self.entries = [[None]*9 for _ in range(9)]  # Create a 9x9 grid of entry widgets
        for i in range(9):
            for j in range(9):
                self.entries[i][j] = tk.Label(self.root, width=3, height=1, font=('Arial', 18), relief=tk.RIDGE, borderwidth=2)
                self.entries[i][j].grid(row=i, column=j)  # Place each label in the grid

        self.generate_killer_sudoku()
        self.display_cages()

        # Button to trigger the solving process
        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=4, columnspan=2)

    def generate_killer_sudoku(self):
        # Define the cages for the Killer Sudoku puzzle
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
            ((6, 5), (6, 6), (7, 5), (8, 5), (8, 6), (8, 7), (8, 8)): 38
        }

    def display_cages(self):
        # Define colors for the cages
        colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightpink', 'lightcoral', 'lightgray', 'lightcyan', 'lightseagreen', 'lightsalmon', 'lightsteelblue']
        i = 0
        for cells, value in self.cages.items():
            for cell in cells:
                row, col = cell
                self.entries[row][col].config(bg=colors[i])  # Color each cell in the cage
            sum_label = tk.Label(self.root, text=value, font=('Arial', 10))
            sum_label.grid(row=cells[0][0], column=cells[0][1], sticky="nw")  # Place the sum label in the top-left cell of the cage
            i = (i + 1) % len(colors)

    def update_gui(self):
        # Update the GUI with the current board state
        for i in range(9):
            for j in range(9):
                cell_text = str(self.board[i][j]) if self.board[i][j] != 0 else ''
                self.entries[i][j].config(text=cell_text)
        self.root.update()

    def ai_solve_process(self):
        least_options_cell = self.find_least_options_cell()
        self.counter += 1

        if least_options_cell is None:
            return True  # If no empty cell is found, the board is solved
        
        row, col = least_options_cell
        remaining_values = list(self.remaining_values[(row, col)])  # Get remaining values for the current cell

        for num in remaining_values:
            self.total_counter += 1
            self.board[row][col] = num
            # Update tracking sets
            self.row_values[row].add(num)
            self.col_values[col].add(num)
            self.box_values[(row // 3) * 3 + (col // 3)].add(num)

            if self.counter == 1000:  # Update the GUI every 100 iterations
                self.update_gui()
                self.counter = 0

            original_remaining_values = self.save_remaining_values()  # Save current state

            if self.update_remaining_values(row, col, num):  # Update remaining values for related cells
                if self.ai_solve_process():
                    return True  # Recursively solve the next cell
            
            # Backtrack
            self.board[row][col] = 0
            self.row_values[row].remove(num)
            self.col_values[col].remove(num)
            self.box_values[(row // 3) * 3 + (col // 3)].remove(num)
            self.restore_remaining_values(original_remaining_values)  # Restore saved state

        return False

    def solve(self):
        start_time = time.time()
        if self.ai_solve_process():
            end_time = time.time()
            self.update_gui()
            print("Solved", f"Solved in {self.total_counter} iterations")
            print("Time taken:", end_time - start_time)
        else:
            print("No solution found")

    def find_least_options_cell(self):
        # Find the cell with the fewest remaining values
        min_remaining_values = 10
        min_cell = None
        for cell, values in self.remaining_values.items():
            # check if cell is 0
            if len(values) < min_remaining_values and self.board[cell[0]][cell[1]] == 0:
                min_remaining_values = len(values)
                min_cell = cell
        return min_cell

    def update_remaining_values(self, row, col, num):
        # Update remaining values for related cells (row, col, box, cage)
        if (row, col) in self.remaining_values:
            del self.remaining_values[(row, col)]

        for r in range(9):
            if num in self.remaining_values.get((r, col), []):
                self.remaining_values[(r, col)].remove(num)
                if not self.remaining_values[(r, col)]:
                    return False

        for c in range(9):
            if num in self.remaining_values.get((row, c), []):
                self.remaining_values[(row, c)].remove(num)
                if not self.remaining_values[(row, c)]:
                    return False

        for i in range(3):
            for j in range(3):
                if num in self.remaining_values.get((i + (row // 3) * 3, j + (col // 3) * 3), []):
                    self.remaining_values[(i + (row // 3) * 3, j + (col // 3) * 3)].remove(num)
                    if not self.remaining_values[(i + (row // 3) * 3, j + (col // 3) * 3)]:
                        return False

        for cage_cells, cage_sum in self.cages.items():
            if (row, col) not in cage_cells:
                continue
            
            current_sum = 0
            empty_cells = []
            
            for r, c in cage_cells:
                if self.board[r][c] == 0:
                    empty_cells.append((r, c))
                else:
                    current_sum += self.board[r][c]
            
            remaining_sum = cage_sum - current_sum

            if len(empty_cells) == 1:
                r, c = empty_cells[0]
                if remaining_sum in self.remaining_values[(r, c)]:
                    self.remaining_values[(r, c)] = {remaining_sum}
                else:
                    return False
            else:
                for r, c in empty_cells:
                    self.remaining_values[(r, c)] = {val for val in self.remaining_values[(r, c)] if val <= remaining_sum}

        return True

    def save_remaining_values(self):
        # Save a deep copy of the current remaining values
        return {key: set(value) for key, value in self.remaining_values.items()}

    def restore_remaining_values(self, original_remaining_values):
        # Restore remaining values from the saved state
        self.remaining_values = original_remaining_values

def main():
    root = tk.Tk()
    app = KillerSudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
