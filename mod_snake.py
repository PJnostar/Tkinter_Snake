import tkinter as tk
import numpy as np

class Snake:
    def __init__(self, canvas: tk.Canvas, board:np.array):
        self.position = np.zeros(shape=(3,2)).astype(int)
        self.len = self.position.shape[0]
        self.body = []
        for i in range(self.len):
            self.position[i,0] = 2-i
            self.body.append(canvas.create_rectangle(0,0,0,0, fill="Green"))

        self.key_last = []
        self.tail_in_previous_step = np.zeros(shape=2).astype(int)

        #                 [     right,     left, up,    down       ]
        self.boundaries = [board.shape[0]-1, 0, 0, board.shape[1]-1]
        # print(self.boundaries)

    def snake_move(self, key):
        self.tail_in_previous_step = self.position[-1,:]
        print("tail position: ", self.tail_in_previous_step)
        # there are 2 conditions to move:
        # 1 - If snake wants to move to the right, then it could not already be moving to the left
        # 2 - If the snake is already moving to the right, then pressing Left cannot change direction - it keeps going right
        if self.check_boundaries(key):
            if key == "Right" and self.key_last != "Left" or (key=="Left" and self.key_last=="Right"):
                self.key_last = "Right"
                self.position[1:, :] = self.position[0:self.len-1,:]
                self.position[0,0] += 1
            elif key == "Left" and self.key_last != "Right" or (key=="Right" and self.key_last=="Left"):
                self.key_last = "Left"
                self.position[1:, :] = self.position[0:self.len-1,:]
                self.position[0,0] -= 1
            elif key == "Up" and self.key_last != "Down":
                self.key_last = "Up"
                self.position[1:, :] = self.position[0:self.len-1,:]
                self.position[0,1] -= 1
            elif key == "Down"and self.key_last != "Up":
                self.key_last = "Down"
                self.position[1:, :] = self.position[0:self.len-1,:]
                self.position[0,1] += 1
        print("snake position: in snake move \n", self.position)

    def check_boundaries(self, key):
        if self.position[0,0]>=self.boundaries[0] and key=="Right":
            return False #"crashed"
        elif self.position[0,0]<=self.boundaries[1] and key=="Left":
            return False #"crashed"
        elif self.position[0,1]<=self.boundaries[2] and key=="Up":
            return False #"crashed"
        elif self.position[0,1]>=self.boundaries[3] and key=="Down":
            return False #"crashed"
        else:
            return True
        
    def snake_grow(self, canvas: tk.Canvas):
        #first determine where to add the new element of the body (always behind the tail)
        if self.key_last == "Right":
            new_body_cell = np.array( self.position[-1,:]-[1,0] )
        elif self.key_last == "Left":
            new_body_cell = np.array( self.position[-1,:]+[1,0] )
        elif self.key_last == "Up":
            new_body_cell = np.array( self.position[-1,:]+[0,1] )
        elif self.key_last == "Down":
            new_body_cell = np.array( self.position[-1,:]-[0,1] )

        #then add new element to the position array and update the snake length
        self.position = np.vstack((self.position, new_body_cell))

        self.len = self.position.shape[0]
        self.body.append(canvas.create_rectangle(0,0,0,0, fill="Green"))