# For Sudoku
from csp import Sudoku
from csp import backtracking_search
from search import breadth_first_tree_search
from search import depth_first_tree_search
from search import Problem
from csp import forward_checking
from csp import mrv
from csp import lcv
from csp import least_constraining_variable
from csp import most_constraining_value
import math
import time
# For scheduler
from csp import Scheduler
from csp import degree
from csp import no_inference
# For find path
from search import Graph
from search import GraphProblem
from search import astar_search
from decimal import *
from search import idastar_search

# ========================= SUDOKU =========================

def printNode(node):
    output = "\nOutput String:\n"
    for box in node.state:
        output += str(box[1])
    return output

def sudokuSolver(fileName, searchAlgo):

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
            solver.display(solver.infer_assignment())
            output.write(backtrack_solution_to_string(solver))
            printStats(end - start, solver.nassigns, "IGNORE", output)
        elif (searchAlgo == "dfs"):
            start = time.time()
            solutionNode = depth_first_tree_search(solver)
            end = time.time()
            output.write(printNode(solutionNode))
            printStats(end - start, solver.nodesGenerated, solver.maxNodeMemory, output)
        elif (searchAlgo == "bfs"):
            start = time.time()
            solutionNode = breadth_first_tree_search(solver)
            end = time.time()
            output.write(printNode(solutionNode))
            # print out the results of the tree BFS
            printStats(end - start, solver.nodesGenerated, solver.maxNodeMemory, output)

def printStats(runtime, nodesGenerated, maxNodeMemory, output):
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

# ========================== SCHEDULER =======================

def scheduleCourse(inputFile, slots):

    # Open the file and load line by line
    classInfos = list()
    with open(inputFile, "r") as f:
        for line in f:
            classInfos.append(line)

    classDicts = [] # This array will hold multiple dictionaries of class info
    for classInfo in classInfos:
        classInfo = classInfo.split(";")
        classDict = {} # This dictionary will contain key->vals for class info
        classDict["name"] = classInfo[0]
        classDict["number"] = classInfo[1]
        classDict["sections"] = classInfo[2]
        classDict["professors"] = parseProfessors(classInfo[5], classInfo[6])
        if len(classInfo[7].rstrip()) == 0:
            classDict["areas"] = None
        else:
            classDict["areas"] = classInfo[7].rstrip().split(",")
        classDicts.append(classDict)
        # printClassDictionaries(classDict)

    mySchedule = Scheduler(classDicts, slots)
    # Uses MRV, LCV, and a custom inference function called "degree"
    backtracking_search(mySchedule, select_unassigned_variable=degree, order_domain_values=lcv, inference=no_inference)
    assignments = mySchedule.infer_assignment()

    output = open("output.txt", "w+")
    for course, time in assignments.items():
        output.write(course + "," + str(time) + ";\n")
        print(course + ": time slot " + str(time))

def printClassDictionaries(classDict):
    print(classDict["name"] + " " + classDict["number"])
    print("\tSections: " + classDict["sections"])
    print("\tProfessors:")
    for prof, sections in classDict["professors"].items():
        if "area" in sections.keys():
            print("\t\t" + prof + " has " + sections["num"] + " sections in the area " + str(sections["area"]))
        else:
            print("\t\t" + prof + " has " + sections["num"] + " sections")

def parseProfessors(profInput, sectionInput):
    completeProfs = {}
    profs = []
    if not " " in profInput or not ", " in profInput:
        profs = profInput.split(",")
    else:
        profs = profInput.split(", ")

    sections = sectionInput.split(",")
    i = 0
    for prof in profs:
        completeProfs[prof] = {"num": sections[i]}
        i += 1

    return completeProfs

# =============================== FIND PATH ===============================

MPH_WALK_SPEED = float(3.0)

def findPath(initial, goal):
    getcontext().prec = 2 # We only care about two decimal places

    graphData = {}
    distances = {}
    distances["heuristics"] = {}
    # This information will be used in the heuristic h in the GraphProblem class

    # File with the coords and elevations (heuristic)
    with open("partC-intersections.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            tokens = line.split(",")
            node = tokens[0] + "," + tokens[1]
            longitude = float(tokens[2])
            latitude = float(tokens[3])
            altitude = int(tokens[4])
            heuristicVal = [longitude, latitude, altitude]
            distances[node] = heuristicVal

    # File with the connections in the graph and their distances (path cost)
    with open("partC-distances.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            tokens = line.split(",")
            start = tokens[0] + "," + tokens[1]
            finish = tokens[2] + "," + tokens[3]
            distance = tokens[4]

            connections = {}
            if start in graphData.keys(): # if the connections for this start already exists...
                connections = graphData[start] # Just add onto the existing connections
            connections[finish] = float(distance) # Add the connection and distance
            graphData[start] = connections # Update / Add if new start connection

    map = Graph(graphData, directed=False, locations=distances) # Because a connection can go BOTH WAYS
    solver = GraphProblem(initial, goal, map) # Turn the graph into a graph problem
    solutionNode = astar_search(solver, h=solver.h)
    # solutionNode = idastar_search(solver, h=solver.h)
    # Print the solution path
    # debugPrintPath(solutionNode, distances, solver)
    realPrintPath(solutionNode)
    # print("nodes generated is " + str(solver.nodesGenerated))

def realPrintPath(solutionNode):
    for node in solutionNode.path():
        print(node.state + ",", end="")
    print(milesToMinutes(solutionNode.path_cost))

def debugPrintPath(solutionNode, distances, solver):
    print("=========SOLUTION==========")
    lastNode = solutionNode.path().pop()
    totalDistance = lastNode.path_cost
    print("Total distance " + str(totalDistance))


    for node in solutionNode.path():
        print(str(node.state) + " (height=" + str(distances[node.state][2]) + ")")
        # print("\theuristic(distance to goal)=" + str(round(node.f, 2)))
        print("\theuristic(distance to goal)=" + str(solver.graph.locations["heuristics"][node.state]))
        print("\tcost(distance from origin)=" + str(round(node.path_cost, 2)) + " miles")
        print("\tcost(distance to goal)=" + str(round(totalDistance - node.path_cost, 2)) + " miles")
        if not node.path_cost == 0:
            print("\tcost(time)=" + milesToMinutes(node.path_cost))
        # The best_first_graph_search() from search.py assigns a .h attribute on each node
        # This is what I think calls the h() function in GraphProblem
    print("Total cost: " + milesToMinutes(solutionNode.path_cost))

def milesToMinutes(miles):
    return str(round((miles / MPH_WALK_SPEED) * 100, 2))

# ======================================================================

# Place the name of the program you want to run off of command line here!
if __name__ == "__main__":
    print("Swap a function call on line 238 to any of the following from command line:")
    print("\tsudokuSolver(<file name>, [bfs, dfs, backtracking, backtracking-noOrdering, backtracking-reverse])")
    print("\tscheduleCourse(<input file>, <# of slots for courses>)")
    print("\tfindPath(<intersection init>, <intersection dest>)\n")

    sudokuSolver("exampleSudokus-q1.txt", "dfs")
    # sudokuSolver(<file name>, [bfs, dfs, backtracking, backtracking-noOrdering, backtracking-reverse])
    # scheduleCourse(<input file>, <# of slots for courses>)
    # scheduleCourse("partB-courseList-shortened.txt", 10)
    # findPath(<intersection init>, <intersection dest>)
    # findPath("Forbes,Bouquet", "Forbes,Bellefield")
