#!/usr/bin/env python3

import curses


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

    def head():
        """Returns the position of the snake's head (front of body)."""
        return self.body[-1]
