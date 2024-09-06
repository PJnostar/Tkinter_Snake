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
        self.square_number = 15
        self.square_size = int(self.screen_size/self.square_number)
        # self.square_size = int(self.screen_size/10)
        # self.square_number = int(self.screen_size/self.square_size)
        self.snake_delay = 250      #delay in miliseconds

        self.canvas = tk.Canvas(self.screen, width=self.screen_size, height=self.screen_size)
        self.canvas.pack()

        self.screen.bind("<Key>", self.key_input)
        self.keys_valid = ["Up", "Down", "Right", "Left"]
        self.key = []
        self.screen.bind("<Button-1>", self.new_game)

        self.flag_end = False

        self.draw_board()

        self.board = np.zeros(shape=(self.square_number, self.square_number)).astype(int)
        self.snake = mod_snake.Snake(self.canvas, self.board)
        self.draw_snake()
        
        self.apple_on_game_start()

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                               Drawing functions
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

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

    def draw_apple(self):
        xy = self.square_size*self.apple_position + [self.square_size/2]*2
        L = self.square_size/2
        self.canvas.coords(self.apple_image, xy[1]-L, xy[0]-L, xy[1]+L, xy[0]+L)

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                               Game Logic functions
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

    def new_game(self, event):
        if self.flag_end == True:
            self.canvas.delete("all")
            self.key = []
            self.board = np.zeros(shape=(self.square_number, self.square_number)).astype(int)
            self.draw_board()
            self.snake = mod_snake.Snake(self.canvas, self.board)
            self.draw_snake()
            self.apple_on_game_start()
            self.board_update()
            self.flag_end = False
            self.mainloop()

    def key_input(self, event):
        key_pressed = event.keysym
        if key_pressed in self.keys_valid:
            self.key = key_pressed
        # elif key_pressed == "Escape":
        #     self.flag_end = True
    
    def board_update(self):
        self.board[self.snake.tail_in_previous_step[1], self.snake.tail_in_previous_step[0]] = 0
        for i in range(np.shape(self.snake.position)[0]):
            self.board[self.snake.position[i,1], self.snake.position[i,0]] = 1

    def apple_on_game_start(self):
        self.apple_position = []
        self.apple_image = self.canvas.create_rectangle(0,0,0,0, fill="Red")
        self.apple_position = mod_apple.generate_apple(self.board)
        self.board[self.apple_position[0], self.apple_position[1]] = 2
        self.draw_apple()

    def apple_eaten(self):
        if np.array_equal(self.snake.position[0,:], [self.apple_position[1], self.apple_position[0]]):
            self.snake.snake_grow(self.canvas)
            
            if 0 in self.board:
                self.apple_position = mod_apple.generate_apple(self.board)
                self.board[self.apple_position[0], self.apple_position[1]] = 2
                self.draw_apple()
            else:
                print("wszedl do else'a")
                self.flag_end =  True

    def game_over(self):
        #game ends when snake eats itself aka snake's head hits its body
        snake_head = self.snake.position[0,:]
        head_hit_body = np.any(np.all(self.snake.position[1:]==snake_head, axis=1))
        if head_hit_body:
            final_message = "Game over" + "\n" + "Your score is: " + str(self.snake.len - 3)
            self.canvas.create_text([self.screen_size/2]*2, text=final_message, font="cmr 15 bold", fill="black")
            self.flag_end = True

        #game ends when snake hits the walls
        if self.snake.check_boundaries(self.key) == False:
            final_message = "Game over" + "\n" + "Your score is: " + str(self.snake.len - 3)
            self.canvas.create_text([self.screen_size/2]*2, text=final_message, font="cmr 15 bold", fill="black")
            self.flag_end = True
    
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#                               Mainloop function
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

    def mainloop(self):
        self.screen.update()
        while self.flag_end == False:
            # print("------------------------------------------")
            self.draw_snake()
            self.board_update()
            self.apple_eaten()
            self.screen.after(self.snake_delay, self.snake.snake_move(self.key))
            self.game_over()
            # print("board\n", self.board)
        self.screen.mainloop()
            