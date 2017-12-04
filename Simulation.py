from Process import *
from Queue import *
import sys

class Simulation:
    def __init__(self, algorithm, inputFile):
        self.fitAlgorithm = algorithm
        self.inputFile = inputFile
        self.queue = Queue()
        # Create the memory as a 1 dimensional 256 element array
        # Rely on printMemory() to put the array into required format
        self.memory = 256 * ['.']
        self.time = 0
        self.framesLeft = 256
        self.procList = []

        # Prepare and start the simulation
        self.getProcesses()
        self.startSim()


    """
        Process the .txt file for the process information
    """
    def getProcesses(self):
        procList = []
        test = open(self.inputFile, "r+")

        # Add the processes to the procList
        for line in test:
            if (line[0] != "#" and len(line) > 1):
                line = line.replace("\n", "")
                line = line.split(" ")
                label = line[0]
                framesReq = int(line[1])
                for i in range(2, len(line)):
                    temp = line[i].split('/')
                    arrivalTime = int(temp[0])
                    runTime = int(temp[1])
                    self.procList.append(
                        Process(label=label, frames=framesReq, arrival=arrivalTime, runTime=runTime))

    """
        Simuation implemented as a state machine:
            1) Adds new processes if current time = arrival time of any getProcesses
            2) Removes any processes from memory if they're finished (Clean up memory)
            3) Adds processes to memory (Relies on FitAlgorithms class)
    """
    # TODO:
    # Implement FitAlgorithms class
    def startSim(self):
        while len(self.procList) > 0:
            # Add any new processes
            for process in self.procList:
                if process.arrivalTime is self.time:
                    self.queue.enqueue(process)
                    self.procList.remove(process)

            # Remove any processes / clean up memory if they're done
            for process in self.queue.Q:
                endTime = process.arrivalTime + process.runTime
                if endTime is self.time:
                    self.cleanMemory(self.memory, process)

            if not self.queue.isEmpty():
                for process in self.queue.Q:
                    # TODO: Write the algorithm handler class
                    if self.fitAlgorithm is "Next-Fit":
                        self.memory = FitAlgorithms.nextFit(memory, process)

                    elif self.fitAlgorithm is "First-Fit":
                        self.memory = FitAlgorithms.firstFit(memory, process)

                    elif self.fitAlgorithm is "Best-Fit":
                        self.memory = FitAlgorithm.bestFit(memory, process)

                    elif self.fitAlgorithm is "Non-contiguous":
                        self.memory = FitAlgorithms.nonContiguous(memory, process)

            # Increase by one time-step
            self.time += 1

    """
        Clean memory and add frames back to the frame counter (framesLeft)
    """
    def cleanMemory(self, process):
        for process in self.memory:
            if self.memory is process.label:
                self.memory = '.'
        self.framesLeft += process.frames

    """
        Helper function to print the memory in required format
    """
    def printMemory(self):
        i = 0
        print('================================')
        for x in range(0, 8):
            for y in range(0, 32):
                sys.stdout.write(self.memory[i])
                i += 1
            sys.stdout.flush()
            sys.stdout.write('\n')
        print('================================')
