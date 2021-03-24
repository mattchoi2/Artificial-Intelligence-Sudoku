# Artificial-Intelligence-Sudoku

This was an assignment implemented in Python to complete the below description.  The code can be found in [choi-cs1571-a1.py](https://github.com/mattchoi2/Artificial-Intelligence-Sudoku/blob/master/choi-cs1571-a1.py)

## Description

This assignment is intended to give you practice in implementing some of the concepts we have been
discussing in class. You will be given code that implements the pseudocode in the textbook, and be
asked to adapt it in a variety of ways.
Logistics
▪ This is an individual assignment. You may talk about it in general terms with your classmates,
but your work should represent your individual work.
▪ Written portions of the assignment should be filled in as part of this document, and should be
submitted on Gradescope. Your code should be submitted on CourseWeb
▪ The program you submit should be named: *last-name*-cs1571-a1.py
▪ Assume for all parts that the input is well-formed

Part A. Sudoku & Complexity (50 points)
1. Create a function named “sudokuSolver”. This function should take as inputs:
▪ A string representing a sudoku grid of two possible sizes: 2x2 (containing the digits 1
through 4) and 3x3 (containing the digits 1 through 9). Each grid is represented by a string
where a digit denotes a filled cell and a ‘.’ denotes an empty cell. The string is intended to fill
in the Sudoku grid from left to right and top to bottom. For example, “...1.13..32.2...” is
displayed as:

. . | . 1
. 1| 3 .
----+-----
. 3| 2 .
2 .| . .

▪ A string representing one of the three algorithms that you are planning to run as input:
“bfs”, “dfs”, or “backtracking”.
Run BFS (tree search), DFS (tree search), and backtracking on the three grids found in
exampleSudokus-q1.txt. You should implement naïve versions of BFS and DFS, in that they can
choose the variables to fill one by one, but should not use any heuristics to determine which
numbers are legal to fill in. For backtracking, use minimum-remaining-values, least-constrainingvalue, and forward checking.
With each Sudoku board, your program should output a number of different factors to a file:
a. The solution to the puzzle as a String in the same format as the input string.
b. Total number of nodes created (or in the case of backtracking, the number of assignments
tried)
c. The maximum number of nodes kept in memory at a time (ignore in the case of
backtracking)
d. The running time of the search, using the Python time library (time.time())
To help you, we’ve provided you with the code that comes along with the textbook, which
includes a representation of Sudoku in csp.py. You’ll notice that Sudoku subclasses both CSP and
Problem, and so it is fairly easy to call the different search methods on it right out of the box.
Here are the key elements of this task:
▪ Figure out how to call the methods provided by the textbook.
▪ Make the modifications needed to output the correct counts.
▪ Make the modifications needed to run naïve BFS and DFS on the Sudoku puzzle.
▪ Modify the Sudoku representation to reflect the 2x2 board size. This will also make it easier to
test your code.
