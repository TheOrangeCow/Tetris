import tkinter as tk
import random

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
COLORS = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#FFA500"]


tetrominoes = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

class Tetris:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="black")
        self.canvas.pack()
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.score = 0
        self.game_over = False
        self.draw_grid()
        self.draw_piece()
        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)
        self.master.bind("<Down>", self.move_down)
        self.master.bind("<Up>", self.rotate_piece)
        self.master.bind("<r>", self.restart_game)

    def new_piece(self):
        shape = random.choice(tetrominoes)
        color = random.choice(COLORS)
        return {'shape': shape, 'color': color, 'x': GRID_WIDTH // 2 - len(shape[0]) // 2, 'y': 0}

    def check_collision(self, x_offset, y_offset):
        for y, row in enumerate(self.current_piece['shape']):
            for x, block in enumerate(row):
                if block and (self.current_piece['y'] + y + y_offset >= GRID_HEIGHT or self.current_piece['x'] + x + x_offset < 0 or self.current_piece['x'] + x + x_offset >= GRID_WIDTH or self.grid[self.current_piece['y'] + y + y_offset][self.current_piece['x'] + x + x_offset]):
                    return True
        return False

    def draw_piece(self):
        self.canvas.delete("piece")
        for y, row in enumerate(self.current_piece['shape']):
            for x, block in enumerate(row):
                if block:
                    x0 = (self.current_piece['x'] + x) * BLOCK_SIZE
                    y0 = (self.current_piece['y'] + y) * BLOCK_SIZE
                    x1 = x0 + BLOCK_SIZE
                    y1 = y0 + BLOCK_SIZE
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.current_piece['color'], outline="", tags="piece")
    
    def draw_grid(self):
        self.canvas.delete("grid")
        for y, row in enumerate(self.grid):
            for x, block in enumerate(row):
                if block:
                    x0 = x * BLOCK_SIZE
                    y0 = y * BLOCK_SIZE
                    x1 = x0 + BLOCK_SIZE
                    y1 = y0 + BLOCK_SIZE
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=block, outline="", tags="grid")

    def merge_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, block in enumerate(row):
                if block:
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']
    
    def check_line_clear(self):
        lines_to_clear = [index for index, row in enumerate(self.grid) if all(row)]
        for line in lines_to_clear:
            self.grid.pop(line)
            self.grid.insert(0, [0] * GRID_WIDTH)
            self.score += 10 * (len(lines_to_clear) ** 2)

    def draw_score(self):
        self.canvas.delete("score")
        score_text = f"Score: {self.score}"
        self.canvas.create_text(10, 10, anchor="nw", text=score_text, fill="white", font=("Arial", 16), tags="score")

    def draw_game_over(self):
        game_over_text = "Game Over"
        score_text = f"Score: {self.score}"
        restart_text = "Press R to Restart"
        self.canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, text=game_over_text, fill="white", font=("Arial", 24))
        self.canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, text=score_text, fill="white", font=("Arial", 18))
        self.canvas.create_text(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, text=restart_text, fill="white", font=("Arial", 18))

    def move_left(self, event):
        if not self.check_collision(-1, 0):
            self.current_piece['x'] -= 1
            self.draw_piece()

    def move_right(self, event):
        if not self.check_collision(1, 0):
            self.current_piece['x'] += 1
            self.draw_piece()

    def move_down(self, event):
        if not self.check_collision(0, 1):
            self.current_piece['y'] += 1
            self.draw_piece()

    def rotate_piece(self, event):
        rotated_piece = [list(reversed(row)) for row in zip(*self.current_piece['shape'])]
        if not self.check_collision(0, 0):
            if self.current_piece['x'] + len(rotated_piece[0]) > GRID_WIDTH:
                self.current_piece['x'] = GRID_WIDTH - len(rotated_piece[0])
            elif self.current_piece['x'] < 0:
                self.current_piece['x'] = 0
            self.current_piece['shape'] = rotated_piece
            self.draw_piece()

    def restart_game(self, event):
        if self.game_over:
            self.canvas.delete("all")
            self.canvas.pack_forget()
            self.__init__(self.master)
            self.run()

    def run(self):
        if not self.game_over:
            if self.check_collision(0, 1):
                self.merge_piece()
                self.check_line_clear()
                self.current_piece = self.new_piece()
                if self.check_collision(0, 0):
                    self.game_over = True
            self.draw_grid()
            self.draw_piece()
            self.draw_score()
            if self.game_over:
                self.draw_game_over()
            self.master.after(500, self.run)




root = tk.Tk()
root.title("Tetris")
game = Tetris(root)
game.run()
root.mainloop()


