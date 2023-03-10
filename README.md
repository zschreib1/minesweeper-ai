# minesweeper-ai

I wrote an **AI to play Minesweeper**.

Starter code was provided for this project, which I completed in the context of **Harvard UniversityX**'s **[CS50 Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/2020/)** course. Please **do not** directly use the source code as it is **only** for reference. Plagiarism is strictly prohibited by both Harvard University and the edX platform. See [academic honesty](https://cs50.harvard.edu/ai/2020/honesty/) for details.

There are two main files in this project: 
- *runner.py* containing all of the code to run the graphical interface for the game.
- *minesweeper.py* containing all of the logic the game itself and for the AI to play the game. 


## Specification
Minesweeper is a puzzle game that consists of a grid of cells, where some of the cells contain hidden “mines.” Clicking on a cell that contains a mine detonates the mine, and causes the user to lose the game. Clicking on a “safe” cell (i.e., a cell that does not contain a mine) reveals a number that indicates how many neighboring cells – where a neighbor is a cell that is one square to the left, right, up, down, or diagonal from the given cell – contain a mine.

The goal of the game is to flag (i.e., identify) each of the mines. In many implementations of the game, including the one in this project, the player can flag a mine by right-clicking on a cell (or two-finger clicking, depending on the computer).


## Implementation
In **minesweeper.py**, I completed the implementations of the:
- *Sentence class* (**known_mines**, **known_safes**, **mark_mine**, and **mark_safe** functions).
- **MinesweeperAI class** (**add_knowledge**, **make_safe_move**, and **make_random_move** functions).

The *Minesweeper class* handles the gameplay; the *Sentence class* represents a logical sentence that contains both a set of cells and a count; the *MinesweeperAI class* handles inferring which moves to make based on knowledge.

### How knowledge is represented in this AI and how the AI can make inferences.
Knowledge-based agents make decisions by considering their knowledge base, and making inferences based on that knowledge. In this program, we represent an AI’s knowledge about a Minesweeper game by making each cell a propositional variable that is true if the cell contains a mine, and false otherwise.

We’ll represent each sentence of our AI’s knowledge like the below.
{A, B, C, D, E, F, G, H} = 1

Every logical sentence in this representation has two parts: a set of cells on the board that are involved in the sentence, and a number count, representing the count of how many of those cells are mines. The above logical sentence says that out of cells A, B, C, D, E, F, G, and H, exactly 1 of them is a mine.

Visit the [Harvard CS50AI](https://cs50.harvard.edu/ai/2020/projects/1/minesweeper/) for more information about the specifications for the project. 

## Getting started
Once in the directory for the project, run **pip3 install -r requirements.txt** to install the required Python package (pygame) for this project if you don’t already have it installed.
