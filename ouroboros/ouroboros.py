#!/usr/bin/env python3

import curses


"""
Responsible for where the snake is located on the game board, 
and which direction it is moving.
"""


class Snake:
    def __init__(self, body, direction):
        """Initializes the snake."""
        self.body = body
        self.direction = direction

    def move(position):
        """
        Accepts a 'position' argument, adding this to the front of the snake's body,
        and popping off the back position. This will cause the snake to slither around the
        game board while maintaining its length.
        """
        self.body = self.body[1:] + [position]

    def set_direction(direction):
        """Sets the snake's direction to the input value."""
        self.direction = direction

    def head(self):
        """Returns the position of the snake's head (front of body)."""
        return self.body[-1]


"""
Responsible for storing an apple's location on the game board.
"""


class Apple:
    pass


"""
Responsible for executing the game.
(Can split this as it grows larger; e.g., create a RenderGame class to
display the game state, or a Board class.)
"""


class Game:
    def __init__(self, height, width):
        """Initializes the game."""
        self.height = height
        self.width = width

    def render(self):
        print("Height: {}".format(self.height))
        print("Width: {}".format(self.width))


def main():
    game = Game(10, 20)
    game.render()


if __name__ == "__main__":
    main()
