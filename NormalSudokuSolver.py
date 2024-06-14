import random
import time
import tkinter as tk
BOARD_SIZE = 9  # Size of the board (9x9 for standard Sudoku)
SUBGRID_SIZE = 3  # Size of the subgrids (3x3 for standard Sudoku)
EMPTY_CELLS = 45 # Number of empty cells in template
INITIAL_DELAY = 0.25  # Initial delay in seconds
REDUCED_DELAY = 0.05  # Reduced delay in seconds
CHANGE_DELAY_TIME = 15  # Time after which the delay changes (in seconds)

def is_valid(board, row, col, num):
    """Check if num can be placed at board[row][col]."""
    for i in range(BOARD_SIZE):
        if board[row][i] == num or board[i][col] == num:
            return False
    
    start_row, start_col = SUBGRID_SIZE * (row // SUBGRID_SIZE), SUBGRID_SIZE * (col // SUBGRID_SIZE)
    for i in range(start_row, start_row + SUBGRID_SIZE):
        for j in range(start_col, start_col + SUBGRID_SIZE):
            if board[i][j] == num:
                return False
    
    return True

def fill_board(board):
    """Fill the board with a valid Sudoku solution using backtracking."""
    numbers = list(range(1, BOARD_SIZE + 1))
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 0:
                random.shuffle(numbers)  # Shuffle numbers to introduce randomness
                for num in numbers:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if fill_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_sudoku_template():
    """Generate a Sudoku template with a certain number of cells left empty."""
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    fill_board(board)
    
    # Remove some numbers to create a Sudoku template
    removed = 0
    while removed < EMPTY_CELLS:
        row, col = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
        if board[row][col] != 0:
            board[row][col] = 0
            removed += 1
    
    return board

def create_gui(board):
    """Create a tkinter GUI for displaying the Sudoku board."""
    root = tk.Tk()
    root.title("Sudoku Solver")
    canvas = tk.Canvas(root, width=450, height=450)
    canvas.pack()

    cell_width = 450 // BOARD_SIZE
    cell_height = 450 // BOARD_SIZE

    for i in range(BOARD_SIZE + 1):
        line_width = 3 if i % SUBGRID_SIZE == 0 else 1
        canvas.create_line(0, i * cell_height, 450, i * cell_height, width=line_width)
        canvas.create_line(i * cell_width, 0, i * cell_width, 450, width=line_width)

    cells = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            x1 = j * cell_width
            y1 = i * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height
            cell_text = str(board[i][j]) if board[i][j] != 0 else ''
            font = ("Arial", 18, "bold") if board[i][j] != 0 else ("Arial", 16)
            cells[i][j] = canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=cell_text, font=font)

    return root, canvas, cells

def update_gui(canvas, cells, board, colors):
    """Update the GUI to reflect the current state of the board."""
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            cell_text = str(board[i][j]) if board[i][j] != 0 else ''
            canvas.itemconfig(cells[i][j], text=cell_text, fill=colors[i][j])
    canvas.update()

def ai_solve_process(board, canvas, cells, start_time, delay=INITIAL_DELAY):
    """Solve the Sudoku board with real-time visualization."""
    current_time = time.time()
    elapsed_time = current_time - start_time

    # Change delay after 20 seconds
    if elapsed_time > CHANGE_DELAY_TIME:
        delay = REDUCED_DELAY

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 0:
                for num in range(1, BOARD_SIZE + 1):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        colors[row][col] = "black"
                        update_gui(canvas, cells, board, colors)  # Update the GUI to show progress
                        time.sleep(delay)  # Wait for the specified delay
                        if ai_solve_process(board, canvas, cells, start_time, delay):
                            return True
                        colors[row][col] = "red"
                        update_gui(canvas, cells, board, colors)  # Update the GUI to show backtracking
                        time.sleep(delay)  # Wait for the specified delay
                        board[row][col] = 0
                        colors[row][col] = "black"
                        update_gui(canvas, cells, board, colors)
                return False
            
    # After solving, set all added numbers to green
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if cells[i][j] and canvas.itemcget(cells[i][j], 'fill') == 'black':
                colors[i][j] = "green"
    update_gui(canvas, cells, board, colors)
    return True

# Generate a Sudoku template with 45 empty cells
sudoku_template = generate_sudoku_template()

# Create and start the GUI
root, canvas, cells = create_gui(sudoku_template)
colors = [["black" if sudoku_template[i][j] != 0 else "black" for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]

def start_solving():
    start_time = time.time()
    if ai_solve_process(sudoku_template, canvas, cells, start_time):
        print("Sudoku solved!")
    else:
        print("No solution exists for the given Sudoku.")

root.after(1000, start_solving)  # Start solving after a 1-second delay to allow the GUI to load
root.mainloop()