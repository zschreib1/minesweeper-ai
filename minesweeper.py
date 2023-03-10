import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        # Stores known mines
        mines = set()

        # Any time the number of cells is equal to the count (and count of mines is != 0), we know that all of that sentence's cells must be mines.
        if len(self.cells) == self.count and self.count != 0:
            mines = self.cells 
            return mines 
        else:
            return mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # Stores known safes
        safes = set()

        # Each time we have a sentence whose count is 0, we know that all the surrounding cells are safe
        if self.count == 0:
            safes = self.cells 
            return safes 
        else:
            return safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # If a cell known to be a mine is in the sentence, remove it and decrement the sentence mine count by one as there is now one less mine in the sentence
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            return None
        
        # If cell is not in the sentence, then no action is necessary.

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # If a cell known to be safe is in the sentence, remove it without decrementing the mine count
        if cell in self.cells:
            self.cells.remove(cell)
            return None

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def knowledge_chunker(self, seq, size):
        """
        Extracts an array of 2 sentences from the knowledge base.
        
        Called when new knowledge is being inferred by add_knowledge (based on the subset method described in the Background).
        """
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        print(cell)
        print(count)
        # 1) Mark the cell as move that has been made
        self.moves_made.add(cell)

        # 2) Mark the cell as safe
        self.mark_safe(cell)

        # Stores neighboring cells
        neighboring_cells = set()

        # Identify neighboring cells whose state is still undetermined
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                
                # Ignore neighboring cell known to be a mine and reduce count by 1
                if (i, j) in self.mines:
                    count -= 1 
                    continue 

                # Ignore neighboring cell known to be safe
                if (i, j) in self.safes:
                    continue

                # Ignoring neighboring cell if the move was already made
                if (i, j) in self.moves_made:
                    continue
                
                # Take neighboring cell into account as long as it is within the bounds of the board and add the cell (i, j) to the neighboring_cells set
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighboring_cells.add((i, j))

        # Creates a new sentence based on the cell's neighboring cells and the count 
        new_sentence = Sentence(neighboring_cells, count)

        # Check if new_sentence should be added to the knowledge base based on based on it's value of `cell` and `count`. Make a copy of the new_sentence_safe_cells to avoid modifying it while checking if it should be added to the knowledge base
        new_sentence_safe_cells = new_sentence.cells 
        new_sentence_safe_cells_copy = new_sentence_safe_cells.copy()

        # No need to add new_sentence with count = 0 to knowledge base as all cells are safe, mark them as such
        if new_sentence.count == 0:
            for cell in new_sentence_safe_cells_copy:
                self.mark_safe(cell)

        # No need to add new_sentence with count = 1 to knowledge base if there is only one cell in it as the cell is a mine, mark it as such
        elif new_sentence.count == 1 and len(new_sentence.cells) == 1:
            self.mark_mine(list(new_sentence.cells)[0])

        # 3) Add the new_sentence to the knowledge base
        else:
            self.knowledge.append(new_sentence)

        # 4) If, based on any of the sentences in self.knowledge, new cells can be marked as safe or as mines, then the function should do so.
        for sentence in self.knowledge:
            # As the number of safes in the safe_cells variable changes with each iteration (as I am marking safes), create a copy of the initial set against which to mark safes 
            safe_cells = sentence.known_safes()
            safe_cells_copy = safe_cells.copy()

            if safe_cells != set():
                pass

            if safe_cells:
                for cell in safe_cells_copy:
                    self.mark_safe(cell)
            
            # As the number of mines in the mine_cells variable changes with each iteration (as I am marking mines), create a copy of the initial set against which to mark mines 
            mine_cells = sentence.known_mines()
            mine_cells_copy = mine_cells.copy()

            if mine_cells != set():
                pass

            if mine_cells:
                for cell in mine_cells_copy:
                    self.mark_mine(cell)
        
        # 5) Add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge. Any time we have two sentences set1 = count1 and set2 = count2 where set1 is a subset of set2, then we can construct the new sentence set2 - set1 = count2 - count1.

        # Stores the inferred_sentences that will be added to the knowledge base
        inferred_knowledge = []

        # Compare cells and count for 2 sentences (s1 and s2) extracted from the knowledge base
        if self.knowledge is not []:
            for sentences in self.knowledge_chunker(self.knowledge, 2):
                # If there are 2 sentences in the knowledge_chunker
                if len(sentences) > 1:
                    # Create set1
                    set1 = sentences[0]
                    set1_cells = set1.cells 
                    set1_count = set1.count

                    # Create set2
                    set2 = sentences[1]
                    set2_cells = set2.cells 
                    set2_count = set2.count 

                    # Remove any duplicates 
                    if set1 == set2:
                        self.knowledge.remove(set2)

                    elif set1_cells != set2_cells:
                        # Check if set1 is a subset of set2
                        if set1_cells.issubset(set2_cells):
                            inferred_cells = set2_cells - set1_cells
                            inferred_count = set2_count - set1_count 
                            inferred_sentence = Sentence(inferred_cells, inferred_count)
                            # Add new sentence to inferred knowledge base
                            inferred_knowledge.append(inferred_sentence)

                        # Check if set2 is a subset of set1
                        elif set2_cells.issubset(set1_cells):
                            inferred_cells = set1_cells - set2_cells
                            inferred_count = set1_count - set2_count
                            inferred_sentence = Sentence(inferred_cells, inferred_count)
                            # Add inferred sentence to inferred knowledge base
                            inferred_knowledge.append(inferred_sentence)
        
        # If no inferred knowledge, don't modify the knowledge base
        if not inferred_knowledge:
            pass
        else:
            # Add inferred sentence to the knowledge base if it isn't present yet
            for inferred in inferred_knowledge:
                if inferred not in self.knowledge:
                    self.knowledge.append(inferred)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # Stores a duplicate of safe moves in order not to modify the value
        possible_safe_moves = self.safes.copy()

        # Removes moves made from possible_safe_moves
        possible_safe_moves -= self.moves_made

        if len(possible_safe_moves) == 0:
            return None

        # Removes an arbitrary safe move from the possible_safe_moves set
        safe_move = possible_safe_moves.pop() 
        return safe_move


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        # Stores random moves
        random_moves = set()

        # Generates a random move within the bounds of the board
        i = random.randrange(self.height)
        j = random.randrange(self.width)
        random_move = (i, j)

        # If the random move wasn't already made and it is not known to be a mine, add it to the random moves set.
        if random_move not in self.moves_made and random_move not in self.mines:
            random_moves.add(random_move)
        
        # If there are no random moves possible
        if len(random_moves) == 0:
            return None 

        # Removes an arbitrary random_move from the random_moves set
        random_move = random_moves.pop() 
        return random_move 