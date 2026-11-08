# Matchstick Master - Python Puzzle Game

A desktop-based matchstick equation puzzle game developed using Python and Tkinter. The player must move exactly one matchstick to make each displayed equation correct.

## Project details
- **Project name:** Matchstick Master
- **Language:** Python 3
- **GUI:** Tkinter
- **Storage:** JSON
- **Project type:** Puzzle game / Desktop application

## Features
- Professional dark-themed desktop interface
- 10 matchstick equation levels
- 60-second timer for each level
- Score system with a penalty for incorrect answers
- Hint option
- Top-5 scoreboard saved in `scores.json`
- Restart option
- System alert sound using Tkinter's built-in `bell()`

## Problem statement
Matchstick puzzles develop logical thinking. A player is shown an incorrect arithmetic equation made with matchsticks and must move exactly one matchstick to make the equation correct. This project provides a simple interactive desktop application for practising these puzzles.

## Objectives
1. Develop a desktop puzzle game using Python.
2. Display matchstick equation challenges.
3. Accept and validate the player's corrected equation.
4. Add a timer and score system.
5. Save the top five scores locally.
6. Provide hints and a restart option.

## Proposed system
The application displays one puzzle at a time. The player enters a corrected equation and selects **CHECK ANSWER**. The program normalizes spaces and checks the answer against the solution for the current level. A correct answer awards points and unlocks the next level. An incorrect answer deducts five points. Each level has a 60-second timer. At the end of the game, the player's score is stored in a local JSON scoreboard.

> Note: This version uses typed equation answers for interaction. It does not yet provide mouse-based matchstick dragging or animated matchstick graphics.

## Concepts and modules used
- **Tkinter:** creates the graphical user interface.
- **Functions and classes:** organize the game logic.
- **Lists and dictionaries:** store puzzle questions and answers.
- **条件 / if-else:** validate answers and control game states.
- **`after()`:** updates the countdown timer.
- **JSON:** stores the top-five scoreboard.
- **Regular expressions:** remove spaces when comparing answers.

## Algorithm
1. Start the application.
2. Load the saved scoreboard from `scores.json`, if available.
3. Display the game interface and ask for the player's name.
4. Set the current level to 1 and the score to 0.
5. Display the current matchstick equation and start the 60-second timer.
6. Read the equation entered by the player.
7. Remove spaces and normalize the input.
8. Compare the entered equation with the expected answer.
9. If the answer is correct:
   - Stop the timer.
   - Calculate and add points.
   - Enable the Next Level button.
10. Otherwise:
    - Deduct five points, without allowing a negative score.
    - Allow the player to try again while time remains.
11. Repeat for all levels or until the timer reaches zero.
12. Save the player's score and update the top-five scoreboard.
13. Display the final result and end the application.

## Flowchart
See [`assets/flowchart.png`](assets/flowchart.png).

## Sample input and output

**Sample puzzle:** `7 - 1 = 2`

**Player input:** `1 + 1 = 2`

**Expected result:** Correct answer; award points and unlock the next level.

The sample puzzle uses one matchstick move: remove the vertical match from the minus sign to make a plus sign, and move that match to the first digit to change 7 into 1.

## Complexity analysis
Let **P** be the number of puzzle levels and **L** be the maximum number of characters in an entered equation.

- Answer validation: **O(L)** per attempt, because input normalization and string comparison scan the entered text.
- Puzzle storage: **O(P)**.
- Scoreboard sorting: **O(S log S)** where S is the number of stored scores before retaining the top five. The saved scoreboard is kept small.
- Timer update: **O(1)** per tick.

## Testing
| Test | Action | Expected result |
|---|---|---|
| 1 | Enter the correct answer | Correct message and points added |
| 2 | Enter an incorrect answer | Error message and 5 points deducted |
| 3 | Select Hint | Hint message is displayed |
| 4 | Wait until timer reaches zero | Game Over message |
| 5 | Complete all levels | Final score is displayed and saved |
| 6 | Restart the game | Level and score reset |
| 7 | Close and reopen the game | Saved top-five scoreboard is loaded |

## Limitations
- Answers are typed instead of moving matchsticks with the mouse.
- The scoreboard is stored locally on the same computer.
- The timer is fixed at 60 seconds per level.
- The sound uses the operating system's standard Tkinter alert sound.
- The puzzle set is predefined.

## Future enhancements
- Add clickable and draggable matchstick graphics.
- Add background music and custom sound effects.
- Add difficulty selection (Easy, Medium and Hard).
- Add more puzzle levels.
- Add player profiles and a database-backed leaderboard.
- Add animations and a pause/resume option.

## How to run

1. Install Python 3.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run:

```bash
python main.py
```

Tkinter and JSON are included with most standard Python installations. No third-party packages are required.

## Repository structure

```text
Matchstick-Master-Python/
├── main.py
├── README.md
├── algorithm.txt
├── requirements.txt
├── scores.json
└── assets/
    └── flowchart.png
```

## Developer
Venkatesh

## License
This project is available for learning and educational use.
