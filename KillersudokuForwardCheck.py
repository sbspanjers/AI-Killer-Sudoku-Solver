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
        empty_cell = self.find_empty_cell()  # Find an empty cell
        self.counter += 1
        self.total_counter += 1

        if empty_cell is None:
            return True  # If no empty cell is found, the board is solved
        
        row, col = empty_cell
        remaining_values = list(self.remaining_values[(row, col)])  # Get remaining values for the current cell

        for num in remaining_values:
            if self.is_safe(row, col, num):
                self.board[row][col] = num
                # Update tracking sets
                self.row_values[row].add(num)
                self.col_values[col].add(num)
                self.box_values[(row // 3) * 3 + (col // 3)].add(num)

                if self.counter == 100:  # Update the GUI every 100 iterations
                    self.counter = 0
                    self.update_gui()

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

    def find_empty_cell(self):
        # Find the first empty cell in the board
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return i, j
        return None
    
    def is_safe(self, row, col, num):
        # Check if num can be placed in board[row][col] without violating Sudoku rules
        box_index = (row // 3) * 3 + (col // 3)
        return (
            num not in self.row_values[row] and
            num not in self.col_values[col] and
            num not in self.box_values[box_index] and
            self.is_value_consistent_with_cages(row, col, num)
        )

    def is_value_consistent_with_cages(self, row, col, num):
        # Check if placing num in board[row][col] violates any cage constraints
        for cage_cells, cage_sum in self.cages.items():
            if (row, col) in cage_cells:
                current_sum = sum(self.board[r][c] for r, c in cage_cells if self.board[r][c] != 0) + num
                
                if len([1 for r, c in cage_cells if self.board[r][c] == 0]) == 1:
                    return current_sum == cage_sum  # If last cell in cage, ensure the sum matches
                
                elif current_sum >= cage_sum:
                    return False  # If sum exceeds cage sum, return False
        
        return True

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

        for cage_cells, _ in self.cages.items():
            if (row, col) in cage_cells:
                for r, c in cage_cells:
                    if num in self.remaining_values.get((r, c), []):
                        self.remaining_values[(r, c)].remove(num)
                        if not self.remaining_values[(r, c)]:
                            return False

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
