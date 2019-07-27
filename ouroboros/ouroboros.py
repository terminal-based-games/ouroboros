#!/usr/bin/env python3

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint, choice

# Initial values
height = 30
width = 70
begin_y = 0
begin_x = 0
key = KEY_RIGHT
score = 0
game_over = False
possible_keys = [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN]
# Position the snake + food
snake = [[4, 10]]
apple = [[11, 29]]


class Snake:
    """
    Responsible for handling the snake moving on the game board, 
    """

    def __init__(self):
        """Initializes the snake."""

    def get_direction(self, snake, apple):
        """Gets the direction of the snake."""
        y_difference = snake[0] - apple[0]
        x_difference = snake[1] - apple[1]
        if abs(x_difference) >= abs(y_difference):
            if x_difference < 0:
                return KEY_RIGHT
            else:
                return KEY_LEFT
        else:
            if x_difference < 0:
                return KEY_DOWN
            else:
                return KEY_UP

    def move(self, snake, key, symbol, window):
        """Moves snake on the game board."""
        # Calculates the new coordinates of the head of the snake
        snake.insert(
            0,
            [
                snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1),
                snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1),
            ],
        )
        # Snake will enter opposite side of screen if it moves across the edge
        # Moves through top border
        if snake[0][0] == 0:
            snake[0][0] = 28
        # Moves through right border
        if snake[0][1] == 68:
            snake[0][1] = 1
        # Moves through bottom border
        if snake[0][0] == 28:
            snake[0][0] = 1
        # Moves through left border
        if snake[0][1] == 0:
            snake[0][1] = 68

        return snake


class Apple:
    """Responsible for an apple's location on the game board."""

    def __init__(self):
        """Initializes the apple."""

    def move(self, obj, key, symbol, window):
        """Moves an apple on the game board."""
        obj.insert(
            0,
            [
                obj[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1),
                obj[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1),
            ],
        )
        return obj


class Game:
    """
    Responsible for executing the game. (Can split this as it grows larger; 
    e.g., create a RenderGame class to display the game state, or a Board class.)
    """

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
        stdscr = curses.initscr()  # Initialize curses
        curses.noecho()  # Turn off automatic echoing of keys to the screen
        curses.cbreak()  # Enable application to react to keys instantly
        curses.curs_set(False)  # Disable cursor

        # Initialize a new window
        window = curses.newwin(self.height, self.width, self.begin_y, self.begin_x)
        window.keypad(True)
        window.nodelay(True)
        window.border(0)

        return window

    def render(self):
        """Render the game board in a window generated by the curses library."""
        global snake
        global apple

        window = self.initial_setup()
        try:
            # Snake is represented by an "o" character
            window.addch(snake[0][0], snake[0][1], "o")

            # Apple is represented by an "*" character
            window.addch(apple[0][0], apple[0][1], "*")
        except (curses.error):
            pass

        return window

    def next_move(self, snake, apple):
        """Gets the next move."""
        global possible_keys
        s = Snake()
        if randint(0, 3) == 0:
            return (choice(possible_keys), choice(possible_keys))
        else:
            return s.get_direction(snake, apple)

    def play(self, window):
        """Primary controller to play the game of snake."""
        try:
            a = Apple()
            s = Snake()
            global key
            global score
            global snake
            global apple
            global game_over
            global possible_keys
            while key != 27 and game_over == False:
                window.border(0)
                window.addstr(0, 2, " Score: " + str(score) + " ")
                window.timeout(520)

                prev_key = key
                event = window.getch()
                key = key if event == -1 else event

                # Pause the game if space bar is pressed;
                # Resume game if space bar is pressed again
                if key == ord(" "):
                    key = -1
                    while key != ord(" "):
                        key = window.getch()
                    key = prev_key
                    continue

                # If an invalid key is pressed, do nothing
                if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:
                    key = prev_key

                snake = s.move(snake, key, "o", window)
                # Game over if snake runs over itself
                if snake[0] in snake[1:]:
                    game_over = True

                # Snake eats an apple
                if snake[0] == apple[0]:
                    apple = []
                    score += 1
                    while apple == []:
                        apple = [[randint(1, 28), randint(1, 68)]]
                        if apple in snake:
                            apple = []
                    try:
                        window.addch(apple[0][0], apple[0][1], "*")
                    except (curses.error):
                        pass
                else:
                    try:
                        last = snake.pop()  # decrease snake length
                        window.addch(last[0], last[1], " ")
                    except (curses.error):
                        pass
                try:
                    window.addch(snake[0][0], snake[0][1], "o")
                except (curses.error):
                    pass

                move_apple = self.next_move(snake[0], apple[0])

                apple = a.move(apple, move_apple, "*", window)

                # Snake eats apple
                if snake[0] == apple[0]:
                    apple = []
                    score += 1
                    while apple == []:
                        apple = [[randint(1, 28), randint(1, 68)]]
                        if apple in snake:
                            apple = []
                    window.addch(apple[0][0], apple[0][1], "*")

        finally:
            # Terminate a curses application
            curses.nocbreak()
            curses.echo()
            curses.endwin()


def main():

    # Set up new game
    game = Game(height, width, begin_y, begin_x)
    window = game.render()
    game.play(window)


if __name__ == "__main__":
    main()
