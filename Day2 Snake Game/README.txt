Pygame Snake Game Tutorial
"""
This tutorial will guide you on how to use the provided Pygame Snake Game script. This script allows you to play the classic Snake Game, where you control a growing snake that must avoid colliding with itself and the window borders, while eating fruits that appear randomly on the screen.
"""

Prerequisites
"""
Ensure you have the following:

Python 3.6 or newer
Pygame library installed
"""
Setup
"""

Clone or download the script to your local machine.
Run the script using Python.
"""
Script Explanation
The script defines a snake game with the following elements:

A game window of 720x480 pixels.
A snake that starts with a size of 4 blocks and is controlled by the arrow keys.
A fruit that appears at random positions on the screen.
A scoring system that increases the score by one each time the snake eats a fruit.
The game ends when the snake collides with the window's borders or with itself. The final score is then displayed.

Important Variables and Functions
snake_speed: Determines the speed of the snake.

snake_position: Stores the current position of the snake's head.

snake_body: Stores the positions of all the blocks that make up the snake's body.

fruit_position: Stores the current position of the fruit.

direction and change_to: Control the current and next direction of the snake's movement.

score: Stores the current score.

show_score(color, font, size): Displays the current score on the screen.

game_over(): Ends the game, displays the final score and closes the program.

game(): Contains the main game loop that handles events, updates the game state, draws the game elements and checks for the game over condition.

Running the Game
To start the game, run the script with a Python interpreter. Use the arrow keys to control the direction of the snake. The game ends when the snake collides with the window borders or with itself, and the final score is displayed. To play again, run the script again.