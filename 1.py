import tkinter as tk
import random

# Game settings
GAME_WIDTH = 500
GAME_HEIGHT = 500
SPACE_SIZE = 20
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
SPEED = 150

class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Snake Game")
        self.window.resizable(False, False)
        
        self.canvas = tk.Canvas(self.window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()
        
        self.snake = [(0, 0)]
        self.food = self.create_food()
        self.direction = "Right"
        self.running = True
        
        self.window.bind("<Left>", lambda event: self.change_direction("Left"))
        self.window.bind("<Right>", lambda event: self.change_direction("Right"))
        self.window.bind("<Up>", lambda event: self.change_direction("Up"))
        self.window.bind("<Down>", lambda event: self.change_direction("Down"))
        
        self.next_turn()
        self.window.mainloop()
    
    def create_food(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        return x, y
    
    def change_direction(self, new_direction):
        opposite = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}
        if new_direction != opposite.get(self.direction):
            self.direction = new_direction
    
    def next_turn(self):
        if not self.running:
            return
        
        head_x, head_y = self.snake[-1]
        
        if self.direction == "Left":
            head_x -= SPACE_SIZE
        elif self.direction == "Right":
            head_x += SPACE_SIZE
        elif self.direction == "Up":
            head_y -= SPACE_SIZE
        elif self.direction == "Down":
            head_y += SPACE_SIZE
        
        new_head = (head_x, head_y)
        
        if (
            head_x < 0 or head_x >= GAME_WIDTH or
            head_y < 0 or head_y >= GAME_HEIGHT or
            new_head in self.snake
        ):
            self.running = False
            self.canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, text="GAME OVER", fill="red", font=("Arial", 24))
            return
        
        self.snake.append(new_head)
        
        if new_head == self.food:
            self.food = self.create_food()
        else:
            self.snake.pop(0)
        
        self.canvas.delete("all")
        for segment in self.snake:
            self.canvas.create_rectangle(
                segment[0], segment[1],
                segment[0] + SPACE_SIZE, segment[1] + SPACE_SIZE,
                fill=SNAKE_COLOR, outline=""
            )
        self.canvas.create_oval(
            self.food[0], self.food[1],
            self.food[0] + SPACE_SIZE, self.food[1] + SPACE_SIZE,
            fill=FOOD_COLOR, outline=""
        )
        
        self.window.after(SPEED, self.next_turn)

if __name__ == "__main__":
    SnakeGame()
