# Pac-Man Multi-Agent AI Project
In this project, you'll be implementing the Expectimax algorithm and a better evaluation function for the Pac-Man game.

## Required Python Version
This project requires Python version 3.6 or higher.

### Required Libraries
The following libraries are required to run the project:

*os
*time
*random
*numpy
*tkinter

##### Running the Code
To run the code, use the following command:

"python3 pacman.py -l mediumClassic -p ExpectimaxAgent -a evalFn=better -a depth=3 -q -n 20"

This command will run the Pac-Man game using the ExpectimaxAgent class with the better evaluation function and a search depth of 3. The game will be played in quiet mode (i.e., without displaying graphics) and 20 games will be played.

The available command line arguments are:

-l: Specifies the layout to use for the game. The available options are smallClassic and mediumClassic. If not specified, the mediumClassic layout is used by default.
-p: Specifies the agent to use for the game.
-a: Specifies additional arguments for the agent. You can specify the evaluation function using evalFn=better or the search depth using depth=3.
-n: Specifies the number of games to play.
-q: Makes the game run in quiet mode, without displaying graphics.