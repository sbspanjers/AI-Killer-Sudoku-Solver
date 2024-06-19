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
        self.total_counter = 0

        # Initialize remaining values for each cell with all possible values (1-9)
        self.remaining_values = {(i, j): set(range(1, 10)) for i in range(9) for j in range(9)}
        # Sets to keep track of used values in rows, columns, and boxes
        self.row_values = [set() for _ in range(9)]
        self.col_values = [set() for _ in range(9)]
        self.box_values = [set() for _ in range(9)]

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
            ((6, 5), (6, 6), (7, 5), (8, 5), (8, 6), (8, 7), (8, 8)): 38
        }

    def display_cages(self):
        colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightpink', 'lightcoral', 'lightgray', 'lightcyan', 'lightseagreen', 'lightsalmon', 'lightsteelblue']
        i = 0
        for cells, value in self.cages.items():
            for cell in cells:
                row, col = cell
                self.entries[row][col].config(bg=colors[i])
            sum_label = tk.Label(self.root, text=value, font=('Arial', 10))
            sum_label.grid(row=cells[0][0], column=cells[0][1], sticky="nw")
            i = (i + 1) % len(colors)

    def update_gui(self):
        for i in range(9):
            for j in range(9):
                cell_text = str(self.board[i][j]) if self.board[i][j] != 0 else ''
                self.entries[i][j].config(text=cell_text)
        self.root.update()

    def solve(self):
        start_time = time.time()
        sorted_cages = sorted(self.cages.items(), key=lambda x: (len(x[0]), x[1]))
        if self.solve_by_cages(sorted_cages):
            end_time = time.time()
            self.update_gui()
            print("Sudoku opgelost!")
            print("Aantal iteraties: ", self.total_counter)
            print("Tijd: {:.2f} seconden".format(end_time - start_time))
        else:
            print("Geen oplossing gevonden.")

    def solve_by_cages(self, sorted_cages):
        if not sorted_cages:
            return True
        cage_cells, cage_sum = sorted_cages[0]
        remaining_cages = sorted_cages[1:]
        
        empty_cells = [(r, c) for r, c in cage_cells if self.board[r][c] == 0]
        if not empty_cells:
            return sum(self.board[r][c] for r, c in cage_cells) == cage_sum

        return self.solve_cage(cage_cells, cage_sum, empty_cells, remaining_cages)

    def solve_cage(self, cage_cells, cage_sum, empty_cells, remaining_cages):
        if not empty_cells:
            if sum(self.board[r][c] for r, c in cage_cells) == cage_sum:
                if self.solve_by_cages(remaining_cages):
                    return True
            return False

        min_cell = self.find_least_options_cell(cage_cells)
        r, c = min_cell

        remaining_values = list(self.remaining_values[(r, c)])  # Get remaining values for the current cell
        
        for num in remaining_values:
            self.total_counter += 1
            self.counter += 1
            
            self.board[r][c] = num
            self.row_values[r].add(num)
            self.col_values[c].add(num)
            self.box_values[(r // 3) * 3 + (c // 3)].add(num)

            if self.counter == 1000:
                self.update_gui()
                self.counter = 0

            original_remaining_values = self.save_remaining_values()
            
            if self.update_remaining_values(r, c, num):
                if self.solve_cage(cage_cells, cage_sum, empty_cells[1:], remaining_cages):
                    return True
            
            #backtrack
            self.board[r][c] = 0
            self.row_values[r].remove(num)
            self.col_values[c].remove(num)
            self.box_values[(r // 3) * 3 + (c // 3)].remove(num)
            self.restore_remaining_values(original_remaining_values)
                
        return False
    
    def find_least_options_cell(self, cage_cells):
        # Find the cell with the fewest remaining values
        min_remaining_values = 10
        min_cell = None

        # loop cage_cells and find the cell with the fewest remaining values
        for cell in cage_cells:
            if self.board[cell[0]][cell[1]] == 0:
                if len(self.remaining_values[cell]) < min_remaining_values:
                    min_remaining_values = len(self.remaining_values[cell])
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
