import sys
from search import Graph
from search import GraphProblem
from search import astar_search
from decimal import *
from search import idastar_search

# python findPath.py Forbes,Bouquet O'Hara,University
# python findPath.py Forbes,Bouquet Forbes,Bellefield

MPH_WALK_SPEED = float(3.0)

def main():
    getcontext().prec = 2 # We only care about two decimal places
    if (len(sys.argv) != 3):
        print("Wrong usage, try this:")
        print("python findPath.py <intersection init> <intersection dest>")
        exit()

    initial = sys.argv[1]
    goal = sys.argv[2]
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

if __name__ == "__main__":
    main()
