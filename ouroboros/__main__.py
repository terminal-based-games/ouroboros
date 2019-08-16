#!/usr/bin/env python3

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint, choice

# Global Variables
height = 25
width = 75
begin_y = 0
begin_x = 0


class Apple:
    """Responsible for an apple's location on the game board."""

    def __init__(self):
        """Initializes the Apple class."""

    def get_apple(self, snake):
        """Returns random coordinates representing an apple's placement on the game board. These coordinates will not overlap with the snake coordinates."""
        apple = []
        while apple == []:
            apple = [randint(1, height - 2), randint(1, width - 2)]
            # If apple coordinates are in snake's coordinates, get new coordinates
            if apple in snake:
                apple = []
        return apple


class Snake:
    """Responsible for handling the snake moving on the game board."""

    def __init__(self):
        """Initializes the Snake class."""

    def get_snake(self):
        """Returns random coordinates representing a snake's placement on the game board."""
        snake = [[randint(1, height - 2), randint(1, width - 2)]]
        return snake

    def move_across_edges(self, snake):
        """Enables snake to move across the edges of the game's window."""
        # Snake will enter opposite side of screen if it moves across the edge
        # Moves through top edge
        if snake[0][0] == 0:
            snake[0][0] = height - 2
        # Moves through left edge
        if snake[0][1] == 0:
            snake[0][1] = width - 2
        # Moves through bottom edge
        if snake[0][0] == (height - 1):
            snake[0][0] = 1
        # Moves through right edge
        if snake[0][1] == (width - 1):
            snake[0][1] = 1
        return snake

    def dies_if_hits_edge(self, snake):
        """Ends the game if the snake hits the edges of the game's window."""
        if snake[0][0] == 0:
            return True
        elif snake[0][1] == 0:
            return True
        elif snake[0][0] == (height - 1):
            return True
        elif snake[0][1] == (width - 1):
            return True
        else:
            return False

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

    def check_for_180(self, key, prev_key):
        """Checks to see if the snake is trying to perform a 180 degree turn;
        Returns true if it is, else false"""
        if key == KEY_LEFT and prev_key == KEY_RIGHT:
            return True
        if key == KEY_RIGHT and prev_key == KEY_LEFT:
            return True
        if key == KEY_UP and prev_key == KEY_DOWN:
            return True
        if key == KEY_DOWN and prev_key == KEY_UP:
            return True
        return False


class Game:
    """Responsible for executing the game."""

    def __init__(self):
        window = curses.newwin(height, width, begin_y, begin_x)
        window.clear
        window.border
        window.keypad(1)  # Keypad will be interpreted by curses
        window.nodelay(1)  # getch() will be non-blocking
        window.border(0)  # Default border
        window.timeout(220)  # getch() will block delay for number of milliseconds given
        window.bkgd(" ", curses.color_pair(1) | curses.A_BOLD)  # Set window attributes
        window.addstr(window.getmaxyx()[0] - 1, 2, "Press ESC to exit")
        self.window = window
        self.score = 0

    def pause(self, key, prev_key):
        """Pauses game if the space bar is pressed; resumes game if pressed again."""
        if key == ord(" "):
            key = -1
            # loop waiting to unpause when space bar is pressed again
            while key != ord(" "):
                key = self.window.getch()
            key = prev_key
            return key

    def play(self, difficulty):
        """Primary controller to play the game of snake."""
        # Snake is represented by an "o" character
        snake = Snake().get_snake()
        self.window.addch(snake[0][0], snake[0][1], "o")

        # Apple is represented by an "*" character
        apple = Apple().get_apple(snake)
        self.window.addch(apple[0], apple[1], "*", curses.color_pair(2))

        # Initial values
        key = KEY_RIGHT
        game_over = False
        hit_edge = False

        # Key 27 = ESC
        while key != 27 and game_over == False and hit_edge == False:
            # Displays the user's current score
            self.window.addstr(
                0,
                self.window.getmaxyx()[1] - 12,
                " Score: " + str(self.score) + " ",
                curses.color_pair(1),
            )

            prev_key = key
            # getch() refreshes the screen and waits for the user to hit a key
            event = self.window.getch()
            key = key if event == -1 else event

            # Pause game if space bar is pressed;
            # Resume game if space bar is pressed again
            self.pause(key, prev_key)

            # If an invalid key is pressed, do nothing
            if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:
                key = prev_key
            if Snake().check_for_180(key, prev_key):
                key = prev_key

            # Calculate coordinates of snake
            snake = Snake().move(snake, key, self.window)
            if difficulty == False:
                # Enable snake to move across game board edges
                Snake().move_across_edges(snake)
            else:
                # Game over if snake hits game board edge
                hit_edge = Snake().dies_if_hits_edge(snake)

            # Game over if snake runs over itself
            game_over = Snake().run_over_self(snake)

            # Snake ate apple
            if snake[0] == apple:
                self.score += 1
                apple = Apple().get_apple(snake)
                # Paint a "*" character at the given (y, x) coordinates to display an apple
                self.window.addch(apple[0], apple[1], "*", curses.color_pair(2))
            else:
                last = snake.pop()
                self.window.addch(last[0], last[1], " ")
            # Snake ate apple, increase its length
            self.window.addch(snake[0][0], snake[0][1], "o")

        self.window.timeout(-1)  # Window will now block delay instead of timing out
        subwin = self.window.subwin(9, 19, 8, 28)
        subwin.clear()
        subwin.border(0)
        subwin.addstr(3, 5, "GAME OVER")
        subwin.addstr(5, 5, "Score: " + str(self.score))
        subwin.refresh()
        while self.window.getch() != 27:  # while waiting for ESC, block delay
            pass
        del self.window


class WindowManager:
    """Class for managing the curses windows."""

    def __init__(self):
        """Sets up the curses window for the main menu"""
        # Set up curses
        curses.initscr()  # Initialize curses
        curses.start_color()  # Initialize color
        curses.use_default_colors()  # Allow default color values
        curses.noecho()  # Turn off automatic echoing of keys to the screen
        curses.cbreak()  # Enable application to react to keys instantly
        curses.curs_set(0)  # Disable cursor

        # Change definition of color pair
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

        # Make main menu
        main_menu = curses.newwin(height, width, begin_y, begin_x)
        main_menu.clear()
        main_menu.border(0)
        main_menu.bkgd(
            " ", curses.color_pair(1) | curses.A_BOLD
        )  # Set window attributes
        main_menu.addstr(5, 33, "OUROBOROS", curses.A_UNDERLINE | curses.A_BLINK)
        main_menu.addstr(10, 24, "Press ENTER to Play on EASY")
        main_menu.addstr(12, 26, "Press + to Play on HARD")
        main_menu.addstr(14, 29, "Press ESC to Exit")
        main_menu.refresh()
        self.main_menu = main_menu

    def start(self):
        """Starts the main menu loop sequence."""
        while 1:
            keypress = self.main_menu.getch()
            # Easy level
            if keypress == 10:  # ENTER pressed
                Game().play(False)  # Starts a new game
                self.main_menu.touchwin()  # Brings focus back to main menu
                self.main_menu.refresh()
            # Hard level
            elif keypress == 43:
                Game().play(True)  # Starts a new game
                self.main_menu.touchwin()  # Brings focus back to main menu
                self.main_menu.refresh()
            elif keypress == 27:  # ESC pressed
                break

    def close(self):
        # close curses application
        curses.nocbreak()
        curses.echo()
        curses.endwin()


def main():
    try:
        manager = WindowManager()
        manager.start()
        manager.close()
    except:
        pass


if __name__ == "__main__":
    main()
