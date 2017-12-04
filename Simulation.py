from Process import *
from Queue import *
from FitAlgorithms import *
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

        # Add the processes to the procL==t
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
            2) Removes any processes from memory if they're fin==hed (Clean up memory)
            3) Adds processes to memory (Relies on FitAlgorithms class)
    """
    # TODO:
    # Implement FitAlgorithms class
    def startSim(self):
        first = True
        procToRemove = []
        runningPool = []
        prevProc = None

        while len(self.procList) > 0 or len(runningPool) > 0:
            if first:
                if self.fitAlgorithm == "First-Fit":
                    print("time {0}ms: Simulator started (Contiguous -- First-Fit)".format(self.time))

                elif self.fitAlgorithm == "Next-Fit":
                    print("time {0}ms: Simulator started (Contiguous -- Next-Fit)".format(self.time))

                elif self.fitAlgorithm == "Best-Fit":
                    print("time {0}ms: Simulator started (Contiguous -- Best-Fit)".format(self.time))
                first = False

            # Add any new processes
            for process in self.procList:
                if process.arrivalTime <= self.time:
                    self.queue.enqueue(process)
                    procToRemove.append(process)

            for process in procToRemove:
                self.procList.remove(process)

            procToRemove = []

            # Remove any processes / clean up memory if they're done
            for process in runningPool:
                endTime = process.arrivalTime + process.runTime
                if endTime <= self.time:
                    self.cleanMemory(process)
                    print("time {0}ms: Process {1} removed".format(self.time, process.label))
                    self.printMemory()
                    procToRemove.append(process)

            for process in procToRemove:
                runningPool.remove(process)
                if len(runningPool) > 0:
                    prevProc = runningPool[len(runningPool)-1]

            procToRemove = []

            if not self.queue.isEmpty():
                for process in self.queue.Q:
                    if self.fitAlgorithm == "First-Fit":
                        temp = FitAlgorithms.firstFit(self.memory, process, self.framesLeft)
                    elif self.fitAlgorithm == "Next-Fit":
                        temp = FitAlgorithms.nextFit(self.memory, process, self.framesLeft, prevProc)
                    elif self.fitAlgorithm == "Best-Fit":
                        temp = FitAlgorithms.bestFit(self.memory, process, self.framesLeft)
                    elif self.fitAlgorithm == "Non-contiguous":
                        temp = FitAlgorithms.nonContiguous(self.memory, process, self.framesLeft)
                    self.memory = temp[0]

                    # Handle the case where defragmentation may occur
                    if temp[1] > 0:
                        print("time {0}ms: Process {1} arrived (requiring {2} frames)".format(self.time, process.label, process.frames))
                        print("time {0}ms: Cannot place process {1} -- starting defragmentation".format(self.time, process.label))

                        procToRemove.append(process)
                        runningPool.append(process)

                        for proc in self.procList:
                            proc.arrivalTime += temp[1]

                        # Recalculate the number of frames left
                        self.framesAfterDefrag()

                        self.time += temp[1]


                        # TODO: Fix defragmentation to return the frames moved as well as the number of
                        # frames moved

                        print("time {0}ms: Defragmentation complete -- (moved {1} frames: {2})".format(self.time, temp[1], temp[2]))
                        tempMemory = 256 * ['.']
                        for i in range(0, 256):
                            tempMemory[i] = self.memory[i]
                        for i in range(0, len(tempMemory)):
                            if tempMemory[i] == process.label:
                                tempMemory[i] = '.'

                        self.hackPrint(tempMemory)

                        print("time {0}ms: Placed process {1}".format(self.time, process.label))
                        self.printMemory()

                        prevProc = process

                        # Make up for the 1 increase at the end
                        self.time -= 1

                    elif self.framesLeft > process.frames:
                        print("time {0}ms: Process {1} arrived (requiring {2} frames)".format(self.time, process.label, process.frames))
                        print("time {0}ms: Placed process {1}:".format(self.time, process.label))

                        prevProc = process

                        self.printMemory()
                        self.framesLeft -= process.frames
                        procToRemove.append(process)
                        runningPool.append(process)

                    else:
                        print("time {0}ms: Process {1} arrived (requiring {2} frames)".format(self.time, process.label, process.frames))
                        print("time {0}ms: Cannot place process {1} -- skipped!".format(self.time, process.label))
                        procToRemove.append(process)

            # TODO: Potentially write a "next-interesting event" version of th==
            # and only increase by the next event. Possibly implement a function to
            # calculate the next event and store that as self.nextEvent.

            for process in procToRemove:
                self.queue.Q.remove(process)

            procToRemove = []

            self.time += 1

    """
        Clean memory and add frames back to the frame counter (framesLeft)
    """
    def cleanMemory(self, process):
        for i in range(0, len(self.memory)):
            if self.memory[i] == process.label:
                self.memory[i] = '.'
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

    # Hack to print the memory after a defragmentation
    def hackPrint(self, memory):
        i = 0
        print('================================')
        for x in range(0, 8):
            for y in range(0, 32):
                sys.stdout.write(memory[i])
                i += 1
            sys.stdout.flush()
            sys.stdout.write('\n')
        print('================================')

    def framesAfterDefrag(self):
        frames = 0
        for i in range(len(self.memory)-1, 0):
            if self.memory[i] == '.':
                frames += 1
            else:
                break

        self.framesLeft = frames
