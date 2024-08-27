import tkinter as tk
import numpy as np
import time
import mod_snake
import mod_apple


class Board:
    def __init__(self) -> None:
        self.screen = tk.Tk()
        self.screen.title("SNAKE")

        self.screen_size = 600
        self.square_number = 10
        self.square_size = int(self.screen_size/self.square_number)
        # self.square_size = int(self.screen_size/10)
        # self.square_number = int(self.screen_size/self.square_size)

        self.canvas = tk.Canvas(self.screen, width=self.screen_size, height=self.screen_size)
        self.canvas.pack()

        self.screen.bind("<Key>", self.key_input)
        self.keys_valid = ["Up", "Down", "Right", "Left"]
        self.key = []

        self.flag_end = False

        self.draw_board()

        self.board = np.zeros(shape=(self.square_number, self.square_number)).astype(int)
        self.snake = mod_snake.Snake(self.canvas, self.board)
        self.draw_snake()
        # self.snake_drawing = self.canvas.create_rectangle((0.,0.), (60.,60.), fill="Green")
        

    def draw_board(self):
        for i in range(self.square_number):
            self.canvas.create_line([0, i*self.square_size], [self.screen_size, i*self.square_size], fill="black", width=1)
            self.canvas.create_line([i*self.square_size, 0], [i*self.square_size, self.screen_size], fill="black", width=1)

    def draw_snake(self):
        for i in range(self.snake.len):
            xy = self.square_size*self.snake.position[i,:] + [self.square_size/2]*2
            L = self.square_size/2
            self.canvas.coords(self.snake.body[i], xy[0]-L, xy[1]-L, xy[0]+L, xy[1]+L)
        self.screen.update()


    def mainloop(self):
        while self.flag_end == False:
            self.screen.after(500, self.snake.snake_move(self.key))
            print("tail pos before board update: ", self.snake.tail_in_previous_step)
            print("snake pos: ", self.snake.position)
            self.draw_snake()
            self.screen.update()
            self.board_update()
            # print("\n", self.board)
            # self.add_apple()
            
    def key_input(self, event):
        key_pressed = event.keysym
        if key_pressed in self.keys_valid:
            self.key = key_pressed
        elif key_pressed == "Escape":
            self.flag_end = True
        elif key_pressed == "Return":
            self.snake.snake_grow(self.canvas)
            print("entered")

    def add_apple(self):
        mod_apple.generate_apple(self.board)

    def board_update(self):
        # print("snake len: ", self.snake.len)
        self.board[self.snake.tail_in_previous_step[1], self.snake.tail_in_previous_step[0]] = 0
        print("tail pos in board update: ", self.snake.tail_in_previous_step)
        print("snake pos: ", self.snake.position)
        for i in range(np.shape(self.snake.position)[0]):
            # print(i)
            # print(self.snake.position)
            # print(self.snake.position[i,0], self.snake.position[i,1])
            self.board[self.snake.position[i,1], self.snake.position[i,0]] = 1
        