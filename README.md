# Ouroboros
> A terminal-based game inspired by Snake.

[![Build Status](https://travis-ci.com/terminal-based-games/ouroboros.svg?branch=master)](https://travis-ci.com/terminal-based-games/ouroboros)

"Snake" is a game that was preloaded on Nokia phones in 1997. A single player controls a square, which continually grows as it moves, resembling a snake. The objective of the game is to get the snake to eat items (by running into food objects) without running into the border of the screen, any obstacles, or itself. 

## Prerequisites
* Ensure you can run Python 3 from the command line. You can check this by running:

```
python --version
```

If you do not have Python 3 installed, go here: [Download the latest version of Python](https://www.python.org/downloads/)

* Ensure you can run pip from the command line. You can check this by running:

```
pip --version
```

If you do not have pip installed, go here: [Installing pip with get-pip.py](https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py)

* Ensure pip, setuptools, and wheel are up to date by running:

```
python -m pip install --upgrade pip setuptools wheel
```

**Windows:**

In addition to the above requirements, please install the following curses package for Windows:

```
python -m pip install windows-curses
```

For more information, you can read the documentation for [windows-curses 2.0](https://pypi.org/project/windows-curses/).

## Install & Run

```sh
$ pip3 install open-ouroboros
$ ouroboros                     # Run the game
```

**Upgrade:**
```sh
$ pip3 install --upgrade open-ouroboros
```

## Play

**Objective:** Eat as many apples as you can without running into yourself.

**Move:** Use the arrow keys on your keyboard to move the snake (that's you!) into any apples that appear. The goal is to eat as many as you can without running into yourself. With each apple, the snake grows a bit in length.

**Pause:** Hit the space bar to pause the game, and hit the space bar again to resume.

**Exit:** Press the Escape key at any time to exit the game. 

## Demo

![Snake Demo](https://media.giphy.com/media/MdGrSYHxXItqPhXukM/giphy.gif)

## Technology

* Python 3.7
* curses 

## Roadmap 

| Deadline | Event | Description |
| --- | --- | --- |
| 07/02/19 | Research | Finalize open source project goal and discuss scope. |
| 07/06/19 | Design | High-level design, flow charts, and structure for prototype. |
| 07/09/19 | Demo | Deliver a prototype. |
| 07/23/19 | Sprint | Develop minimum viable product ("MVP"). |
| 07/30/19 | Test | Conduct QA and testing. |
| 08/01/19 | Deploy | Deploy MVP to production. |
| 08/13/19 | Sprint | Fix bugs, improve UX, polish final product. |

### MVP
Our minimum viable product is a functional terminal-based game of Snake. This will be a single player game that can run on Mac OS X.

## Future Work
* 2-player mode
* AI players
* High-score leaderboard

## Contribute

Interested in contributing to this project? We'd love to have you! Please take a moment to review our [guide to contributing](/CONTRIBUTING.md) before getting started. 

We welcome developers of any background and skill level. :seedling:

## Testing

Enter the following command to run unit tests:

```
pytest
```

## Credits
* [Implementing Snake using OOP](https://robertheaton.com/2018/12/02/programming-project-5-snake/)

## Built By

* **Mack Cooper** - [@mackkcooper](https://github.com/mackkcooper)

* **Carissa Allen** - [@carissaallen](https://github.com/carissaallen)

All contributors who participate in this project will be recognized here.

## License
Distributed under the MIT License. See [LICENSE](/LICENSE) for more information.
