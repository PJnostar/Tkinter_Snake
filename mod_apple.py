import numpy as np
import random


def generate_apple(board: np.array):
    """ 
    Generates a list of coordinates of empty squares. 
    Then pick a random coordinate to put an apple into.
    Return it
    """
    empty_squares = np.where(board==0)
    empty_squares = np.array(list(zip(empty_squares[0], empty_squares[1])))
    xy = random.randrange(0, np.shape(empty_squares)[0])
    apple_position = empty_squares[xy,:]
    return apple_position