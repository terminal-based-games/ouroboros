import curses

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

# make main menu
main_menu = curses.newwin(25, 75, 0, 0)
main_menu.clear()
main_menu.border(0)
main_menu.bkgd(" ", curses.color_pair(1) | curses.A_BOLD)  # Set window attributes
main_menu.addstr(5, 33, "OUROBOROS", curses.A_UNDERLINE | curses.A_BLINK)
main_menu.addstr(10, 30, "Press 1 to Play")
main_menu.addstr(12, 30, "Press 2 to Quit")
main_menu.addstr(20, 26, "Check us out on Github:")
main_menu.addstr(21, 12, "https://github.com/terminal-based-games/ouroboros/")
main_menu.refresh()

while 1:
    keypress = main_menu.getch()
    if keypress == 49:
        # make new window
        window2 = curses.newwin(25, 75, 0, 0)
        window2.clear()
        window2.border(0)
        window2.bkgd(" ", curses.color_pair(1) | curses.A_BOLD)  # Set window attributes
        window2.addstr(1, 1, "THIS IS THE GAME")
        window2.addstr(2, 1, "press anything to exit to main menu")
        window2.touchwin()
        window2.refresh()
        window2.getkey()
        del window2
        main_menu.touchwin()
        main_menu.refresh()
        continue
    elif keypress == 50:
        break


# close curses application
curses.nocbreak()
curses.echo()
curses.endwin()
