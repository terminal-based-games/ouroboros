#!/usr/bin/env python3

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint, choice


class Apple:
    """Responsible for an apple's location on the game board."""

    def __init__(self):
        """Initializes the Apple class."""

    def init_apple(self, snake):
        apple = []
        while apple == []:
            apple = [[randint(1, 28), randint(1, 68)]]
            # If apple coordinates are in snake's coordinates, start over
            if apple in snake:
                apple = []
        return apple


class Snake:
    """
    Responsible for handling the snake moving on the game board. 
    """

    def __init__(self):
        """Initializes the Snake class."""

    def init_snake(self):
        snake = [[randint(1, 28), randint(1, 68)]]
        return snake

    def move_across_edges(self, snake):
        """Enables snake to move across the edges of the game's window."""
        # Snake will enter opposite side of screen if it moves across the edge
        # Moves through top edge
        if snake[0][0] == 0:
            snake[0][0] = 28
        # Moves through right edge
        if snake[0][1] == 69:
            snake[0][1] = 1
        # Moves through bottom edge
        if snake[0][0] == 29:
            snake[0][0] = 1
        # Moves through left edge
        if snake[0][1] == 0:
            snake[0][1] = 68
        return snake

    def move(self, snake, key, window):
        """Calculates the new coordinates of the snake on the game board."""
        snake.insert(
            0,
            [
                snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1),
                snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1),
            ],
        )
        self.move_across_edges(snake)
        return snake

    def run_over_self(self, snake):
        """If snake runs over itself, the game is over."""
        if snake[0] in snake[1:]:
            return True
        else:
            return False

    def eat_apple(self, snake, apple, score, window):
        """Handles operations that occur when the snake eats an apple. (Not currently used.)"""
        if snake[0] == apple[0]:
            apple = []
            score += 1
            while apple == []:
                # Generate random coordinates for the apple
                apple = [[randint(1, 28), randint(1, 68)]]
                # If apple coordinates are in snake's coordinates, start over
                if apple in snake:
                    apple = []
            # Paint a "*" character at the given (y, x) coordinates to display an apple
            window.addch(apple[0][0], apple[0][1], "*")
        else:
            last = snake.pop()  # Decrease snake length
            window.addch(last[0], last[1], " ")
        window.addch(snake[0][0], snake[0][1], "o")
        return score


class Board:
    """Responsible for game board (terminal window) setup."""

    def __init__(self, height, width, begin_y, begin_x):
        """Initializes the game."""
        # Initialize a new window
        self.height = height
        self.width = width
        self.begin_y = begin_y
        self.begin_x = begin_x

    def initial_setup(self):
        """Initializes curses and window (game board) settings."""
        # Set up curses
        curses.initscr()  # Initialize curses
        curses.noecho()  # Turn off automatic echoing of keys to the screen
        curses.cbreak()  # Enable application to react to keys instantly
        curses.curs_set(0)  # Disable cursor

        # Initialize a new window
        window = curses.newwin(self.height, self.width, self.begin_y, self.begin_x)
        window.keypad(1)
        window.nodelay(1)
        window.border(0)
        window.timeout(520)

        return window

    def render(self, snake, apple):
        """Render the game board in a window generated by the curses library."""
        window = self.initial_setup()
        # Snake is represented by an "o" character
        window.addch(snake[0][0], snake[0][1], "o")
        # Apple is represented by an "*" character
        window.addch(apple[0][0], apple[0][1], "*")

        return window


class Game:
    """
    Responsible for executing the game.
    """

    def __init__(self):
        """Initializes the game."""

    def pause(self, key, prev_key, window):
        """Pauses game if the space bar is pressed; resumes game if pressed again."""
        if key == ord(" "):
            key = -1
            while key != ord(" "):
                key = window.getch()
            key = prev_key
            return key

    def game_over(self):
        """Sets terminal functionality back to original state."""
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def play(self, snake, apple, score, window):
        """Primary controller to play the game of snake."""
        try:
            # Initial values
            key = KEY_RIGHT
            game_over = False

            # Key 27 = ESC
            while key != 27 and game_over == False:
                window.addstr(0, 2, " Score: " + str(score) + " ")

                prev_key = key
                # getch() refreshes the screen and waits for the user to hit a key
                event = window.getch()
                key = key if event == -1 else event

                # Pause game if space bar is pressed;
                # Resume game if space bar is pressed again
                self.pause(key, prev_key, window)

                # If an invalid key is pressed, do nothing
                if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:
                    key = prev_key

                # Calculate coordinates of snake
                s = Snake()
                snake = s.move(snake, key, window)

                # Game over if snake runs over itself
                game_over = s.run_over_self(snake)

                # Snake ate apple
                if snake[0] == apple[0]:
                    apple = []
                    score += 1
                    while apple == []:
                        # Generate random coordinates for the apple
                        apple = [[randint(1, 28), randint(1, 68)]]
                        # If apple coordinates are in snake's coordinates, start over
                        if apple in snake:
                            apple = []
                    # Paint a "*" character at the given (y, x) coordinates to display an apple
                    window.addch(apple[0][0], apple[0][1], "*")
                else:
                    last = snake.pop()
                    window.addch(last[0], last[1], " ")
                # Snake ate apple, increase its length
                window.addch(snake[0][0], snake[0][1], "o")

        finally:
            self.game_over()


def main():
    # Variables for new game
    height = 30
    width = 70
    begin_y = 0
    begin_x = 0

    # Set initial coordinates for snake and apple
    s = Snake()
    a = Apple()
    snake = s.init_snake()
    apple = a.init_apple(snake)
    # Set game score to zero
    score = 0

    # Set up new game
    board = Board(height, width, begin_y, begin_x)
    window = board.render(snake, apple)
    game = Game()
    game.play(snake, apple, score, window)


if __name__ == "__main__":
    main()
