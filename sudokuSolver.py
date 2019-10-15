
from csp import Sudoku
from csp import backtracking_search
from search import breadth_first_tree_search
from search import depth_first_tree_search
from search import Problem
from csp import forward_checking
from csp import mrv
from csp import lcv
from csp import mac
from csp import least_constraining_variable
from csp import most_constraining_value
import sys
import math
import time
# For package errors, run "pip install <package name>" on cmd

def printNode(node):
    output = "\nOutput String:\n"
    for box in node.state:
        output += str(box[1])
    return output

def sudokuSolver():
    if (len(sys.argv) != 3):
        print("Please use as follows:")
        print("python sudokuSolver.py <file name> [bfs, dfs, backtracking, backtracking-noOrdering, backtracking-reverse]")
        exit()
    fileName = sys.argv[1]
    searchAlgo = sys.argv[2]

    # Read thru the file
    lineList = list()
    with open(fileName, "r") as f:
        for line in f:
            lineList.append(line)

    output = open("output.txt", "w+")
    for x in range(0, len(lineList)): # Change to len(list)
        # Create the board
        line = lineList[x].rstrip() # Removes the '\n' from the string
        print("Parsing '" + line + "'")

        # Instantiate a Sudoku
        solver = Sudoku(line)
        # Print out the inference?
        solver.display(solver.infer_assignment())

        if ("backtracking" in searchAlgo):
            start = time.time()
            # mrv is miniumum remaining values is the strategy when picking the first unassigned variables
            # lcv is Least-constraining-values for ordering the values of the domain
            # forward_checking is the inference
            if searchAlgo == "backtracking":
                backtracking_search(solver, select_unassigned_variable=mrv, order_domain_values=lcv, inference=forward_checking)
            elif searchAlgo == "backtracking-noOrdering":
                backtracking_search(solver, inference=forward_checking)
            elif searchAlgo == "backtracking-reverse":
                backtracking_search(solver, select_unassigned_variable=least_constraining_variable, order_domain_values=most_constraining_value, inference=forward_checking)
            end = time.time()
            print("\nBacktracking search solution:")
            solver.display(solver.infer_assignment())
            output.write(backtrack_solution_to_string(solver))
            printStats(end - start, solver.nassigns, "IGNORE", output)
        elif (searchAlgo == "dfs"):
            print("\nDFS tree search solution:")
            start = time.time()
            solutionNode = depth_first_tree_search(solver)
            end = time.time()
            output.write(printNode(solutionNode))
            printStats(end - start, solver.nodesGenerated, solver.maxNodeMemory, output)
        elif (searchAlgo == "bfs"):
            print("\nBFS tree search solution:")
            start = time.time()
            solutionNode = breadth_first_tree_search(solver)
            end = time.time()
            # print out the results of the tree BFS
            printNode(solutionNode)
            printStats(end - start, solver.nodesGenerated, solver.maxNodeMemory, output)

def printStats(runtime, nodesGenerated, maxNodeMemory, output):
    print("=== Statistics ===")
    output.write("\nRuntime:\t\t{0:.2f}".format(runtime))
    output.write("\nNodes created:\t\t" + str(nodesGenerated))
    output.write("\nMax nodes in memory:\t" + str(maxNodeMemory))
    output.write("\n==================")

def backtrack_solution_to_string(solver):
    assignment = solver.infer_assignment()
    output = "\nOutput string:\n"
    for key, val in assignment.items():
        output += str(val)
    return output

sudokuSolver()
