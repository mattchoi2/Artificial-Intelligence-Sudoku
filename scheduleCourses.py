import sys
from csp import Scheduler
from csp import backtracking_search
from csp import mrv
from csp import lcv
from csp import degree
from csp import no_inference

def main():
    if (len(sys.argv) != 3):
        print("Use the program as follows:")
        print("python scheduler.py <input file> <# of slots for courses>")
        exit()
    inputFile = sys.argv[1]
    slots = sys.argv[2]

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
        output.write(course + "," + str(time) + ";")
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

if __name__ == "__main__":
    main()
