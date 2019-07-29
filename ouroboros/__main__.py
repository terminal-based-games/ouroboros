#!/usr/bin/env python3

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint, choice


class Apple:
    """Responsible for an apple's location on the game board."""

    def __init__(self):
        """Initializes the Apple class."""

    def get_apple(self, snake):
        """Returns random coordinates representing an apple's placement on the game board. These coordinates will not overlap with the snake coordinates."""
        apple = []
        width = Board.width - 2
        height = Board.height - 2
        while apple == []:
            apple = [randint(1, height), randint(1, width)]
            # If apple coordinates are in snake's coordinates, start over
            if apple in snake:
                apple = []
        return apple


class Snake:
    """Responsible for handling the snake moving on the game board."""

    def __init__(self):
        """Initializes the Snake class."""

    def get_snake(self):
        """Returns random coordinates representing a snake's placement on the game board."""
        width = Board.width - 2
        height = Board.height - 2
        snake = [[randint(1, height), randint(1, width)]]
        return snake

    def move_across_edges(self, snake):
        """Enables snake to move across the edges of the game's window."""
        # Snake will enter opposite side of screen if it moves across the edge
        # Moves through top edge
        if snake[0][0] == 0:
            snake[0][0] = Board.height - 2
        # Moves through left edge
        if snake[0][1] == 0:
            snake[0][1] = Board.width - 2
        # Moves through bottom edge
        if snake[0][0] == (Board.height - 1):
            snake[0][0] = 1
        # Moves through right edge
        if snake[0][1] == (Board.width - 1):
            snake[0][1] = 1
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
        return snake

    def run_over_self(self, snake):
        """If snake runs over itself, the game is over."""
        if snake[0] in snake[1:]:
            return True
        else:
            return False


class Board:
    """Responsible for game board (terminal window) setup."""

    def __init__(self, height, width, begin_y, begin_x):
        """Initializes the Board class."""
        Board.height = height
        Board.width = width
        self.begin_y = begin_y
        self.begin_x = begin_x

    def initial_setup(self):
        """Initializes curses and window (game board) settings."""
        # Set up curses
        curses.initscr()  # Initialize curses
        curses.start_color()  # Initialize color
        curses.use_default_colors()  # Allow default color values
        # Change definition of color pair
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.noecho()  # Turn off automatic echoing of keys to the screen
        curses.cbreak()  # Enable application to react to keys instantly
        curses.curs_set(0)  # Disable cursor

        # Initialize a new window
        window = curses.newwin(
            self.height, self.width, self.begin_y, self.begin_x
        )  # Return a new window
        window.keypad(1)  # Keypad will be interpreted by curses
        window.nodelay(1)  # getch() will be non-blocking
        window.border(0)  # Default border
        window.timeout(220)  # getch() will block delay for number of milliseconds given
        window.bkgd(" ", curses.color_pair(1) | curses.A_BOLD)  # Set window attributes
        window.addstr(window.getmaxyx()[0] - 1, 2, "Press ESC to exit")

        return window

    def render(self, snake, apple):
        """Render the game board in a window generated by the curses library."""
        window = self.initial_setup()
        # Snake is represented by an "o" character
        window.addch(snake[0][0], snake[0][1], "o")
        # Apple is represented by an "*" character
        window.addch(apple[0], apple[1], "*", curses.color_pair(2))

        return window


class Game:
    """Responsible for executing the game."""

    def __init__(self):
        """Initializes the Game class."""

    def pause(self, key, prev_key, window):
        """Pauses game if the space bar is pressed; resumes game if pressed again."""
        if key == ord(" "):
            key = -1
            # loop waiting to unpause when space bar is pressed again
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
                # Displays the user's current score
                window.addstr(
                    0,
                    window.getmaxyx()[1] - 12,
                    " Score: " + str(score) + " ",
                    curses.color_pair(1),
                )

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
                snake = Snake().move(snake, key, window)
                # Enable snake to move across game board edges
                Snake().move_across_edges(snake)

                # Game over if snake runs over itself
                game_over = Snake().run_over_self(snake)

                # Snake ate apple
                if snake[0] == apple:
                    score += 1
                    apple = Apple().get_apple(snake)
                    # Paint a "*" character at the given (y, x) coordinates to display an apple
                    window.addch(apple[0], apple[1], "*", curses.color_pair(2))
                else:
                    last = snake.pop()
                    window.addch(last[0], last[1], " ")
                # Snake ate apple, increase its length
                window.addch(snake[0][0], snake[0][1], "o")

        finally:
            self.game_over()


def main():
    # Initial game values
    height = 25
    width = 75
    begin_y = 0
    begin_x = 0
    score = 0

    # Initialize game board
    board = Board(height, width, begin_y, begin_x)
    # Set initial coordinates for snake and apple
    snake = Snake().get_snake()
    apple = Apple().get_apple(snake)
    # Initialize window (terminal screen)
    window = board.render(snake, apple)
    # Play game!
    Game().play(snake, apple, score, window)


if __name__ == "__main__":
    main()
