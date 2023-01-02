# minesweeper-ai

I wrote an **AI to play Minesweeper**.

Starter code was provided for this project, which I completed in the context of **Harvard UniversityX**'s **[CS50 Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/2020/)** course. 

There are two main files in this project: 
- *runner.py* containing all of the code to run the graphical interface for the game.
- *minesweeper.py* containing all of the logic the game itself and for the AI to play the game. 

## Implementation
In *minesweeper.py*, I completed the implementations of the:
- *Sentence class* (*known_mines*, *known_safes*, *mark_mine*, and *mark_safe* functions).
- *MinesweeperAI class* (*add_knowledge*, *make_safe_move*, and *make_random_move* functions).

The *Minesweeper class* handles the gameplay; the *Sentence class* represents a logical sentence that contains both a set of cells and a count; the *MinesweeperAI class* handles inferring which moves to make based on knowledge.

## Specification
Minesweeper is a puzzle game that consists of a grid of cells, where some of the cells contain hidden “mines.” Clicking on a cell that contains a mine detonates the mine, and causes the user to lose the game. Clicking on a “safe” cell (i.e., a cell that does not contain a mine) reveals a number that indicates how many neighboring cells – where a neighbor is a cell that is one square to the left, right, up, down, or diagonal from the given cell – contain a mine.

### How knowledge is represented in this AI and how the AI can make inferences.



