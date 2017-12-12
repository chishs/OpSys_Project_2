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
        self.lastRemoved = None
        self.prevProc = None
        self.runningPool = []
        self.nextIndex = None
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
            if (line[0] != "#" and len(line) > 4):
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
        self.runningPool = []
        # Pointer to location of previous process
        self.prevProc = None
        self.lastRemoved = None

        while len(self.procList) > 0 or len(self.runningPool) > 0:
            if first:
                if self.fitAlgorithm == "First-Fit":
                    print("time {0}ms: Simulator started (Contiguous -- First-Fit)".format(self.time))

                elif self.fitAlgorithm == "Next-Fit":
                    print("time {0}ms: Simulator started (Contiguous -- Next-Fit)".format(self.time))

                elif self.fitAlgorithm == "Best-Fit":
                    print("time {0}ms: Simulator started (Contiguous -- Best-Fit)".format(self.time))

                elif self.fitAlgorithm == "Non-contiguous":
                    print("time {0}ms: Simulator started (Non-contiguous)".format(self.time))

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
            for process in self.runningPool:
                endTime = process.arrivalTime + process.runTime
                if endTime <= self.time:
                    self.cleanMemory(process)
                    print("time {0}ms: Process {1} removed:".format(self.time, process.label))
                    self.printMemory()
                    if self.fitAlgorithm == "Non-contiguous":
                        self.printPageTable()
                    procToRemove.append(process)
                    if self.prevProc is not None and self.prevProc.label == process.label:
                        self.lastRemoved = process

            for process in procToRemove:
                self.runningPool.remove(process)

            procToRemove = []

            if not self.queue.isEmpty():
                for process in self.queue.Q:
                    if self.fitAlgorithm == "First-Fit":
                        temp = FitAlgorithms.firstFit(self.memory, process, self.framesLeft)
                    elif self.fitAlgorithm == "Next-Fit":
                        temp = FitAlgorithms.nextFit(self.memory, process, self.framesLeft, self.prevProc, self.nextIndex)
                    elif self.fitAlgorithm == "Best-Fit":
                        temp = FitAlgorithms.bestFit(self.memory, process, self.framesLeft)
                    elif self.fitAlgorithm == "Non-contiguous":
                        temp = FitAlgorithms.nonContiguous(self.memory, process, self.framesLeft)

                    self.memory = temp[0]

                    # Handle the case where defragmentation may occur
                    if temp[1] > 0:
                        print("time {0}ms: Process {1} arrived (requires {2} frames)".format(self.time, process.label, process.frames))
                        print("time {0}ms: Cannot place process {1} -- starting defragmentation".format(self.time, process.label))

                        procToRemove.append(process)
                        self.runningPool.append(process)

                        for proc in self.procList:
                            proc.arrivalTime += temp[1]

                        for proc in self.runningPool:
                            proc.runTime += temp[1]

                        # Recalculate the number of frames left
                        self.framesAfterDefrag()

                        self.time += temp[1]


                        # TODO: Fix defragmentation to return the frames moved as well as the number of
                        # frames moved

                        print("time {0}ms: Defragmentation complete (moved {1} frames: {2})".format(self.time, temp[1], temp[2]))
                        tempMemory = 256 * ['.']
                        for i in range(0, 256):
                            tempMemory[i] = self.memory[i]
                        for i in range(0, len(tempMemory)):
                            if tempMemory[i] == process.label:
                                tempMemory[i] = '.'

                        self.hackPrint(tempMemory)

                        print("time {0}ms: Placed process {1}:".format(self.time, process.label))
                        self.printMemory()
                        if self.fitAlgorithm == "Non-contiguous":
                            self.printPageTable()

                        self.prevProc = process
                        self.nextIndex = self.getPrevProcIndex()

                        # Make up for the 1 increase at the end
                        self.time -= 1

                    elif self.framesLeft >= process.frames:
                        print("time {0}ms: Process {1} arrived (requires {2} frames)".format(self.time, process.label, process.frames))
                        print("time {0}ms: Placed process {1}:".format(self.time, process.label))

                        self.prevProc = process
                        self.nextIndex = self.getPrevProcIndex()

                        self.printMemory()
                        if self.fitAlgorithm == "Non-contiguous":
                            self.printPageTable()

                        self.framesLeft -= process.frames
                        procToRemove.append(process)
                        self.runningPool.append(process)

                    else:
                        print("time {0}ms: Process {1} arrived (requires {2} frames)".format(self.time, process.label, process.frames))
                        print("time {0}ms: Cannot place process {1} -- skipped!".format(self.time, process.label))
                        procToRemove.append(process)
                        self.printMemory()

                        if self.fitAlgorithm == "Non-contiguous":
                            self.printPageTable()

            # TODO: Potentially write a "next-interesting event" version of th==
            # and only increase by the next event. Possibly implement a function to
            # calculate the next event and store that as self.nextEvent.

            for process in procToRemove:
                self.queue.Q.remove(process)

            procToRemove = []

            self.time += 1

        # Account for the last time increment
        if self.fitAlgorithm != "Non-contiguous":
            print("time {0}ms: Simulator ended (Contiguous -- {1})\n".format(self.time-1, self.fitAlgorithm))
        else:
            print("time {0}ms: Simulator ended (Non-contiguous)".format(self.time-1, self.fitAlgorithm))

    """
        Return a pointer to the location of the previous process
    """
    def getPrevProcIndex(self):
        for i in range(0, len(self.memory)):
            if (self.memory[i] == self.prevProc.label):
                return i + self.prevProc.frames

        return 0
    
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
        # else:
        #     print('================================')
        #     for x in range(0, 8):
        #         for y in range(0, 32):
        #             if i <= 255 - self.lastRemoved.frames:
        #                 if self.runningPool[len(self.runningPool)-1].label == memory[i]:
        #                     while i+1 < 255 and memory[i+1] != self.runningPool[len(self.runningPool)-1].label:
        #                         lastLoc = i
        #                         sys.stdout.write(self.memory[i])
        #                         i += 1
        #                 else:
        #                     sys.stdout.write(self.memory[i])
        #                     i += 1
        #
        #                 if lastLoc != -1:
        #                     for j in range(0, self.lastRemoved.frames):
        #                         sys.stdout.write('.')
        #
        #         sys.stdout.flush()
        #         sys.stdout.write('\n')
        #     print('================================')

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

    def printPageTable(self):
        # Hold each individual page table string
        procPageStrings = 26*['']
        # Hold index data for each process
        procPageLocs = []

        # Create an entry for each possible process (26 letters)
        for i in range(0, 26):
            procPageLocs.append([])

        # Add the index to the process's current indexes
        for i in range(0, 256):
            if self.memory[i] != ".":
                procPageLocs[ord(self.memory[i])%65].append(i)

        # Create the process strings for matching submitty output
        for i in range(0, 26):
            procStr = ""
            if len(procPageLocs[i]) > 0:
                procStr += "{0}: ".format(chr(i+65))
                j = 0
                # Add each individual page, frame combination to the process's string
                k = -1
                while j < len(procPageLocs[i]):
                    k += 1
                    procStr += "[{0},{1}]".format(k, procPageLocs[i][j])
                    # Add a line break every 10 entries
                    if (j + 1) % 10 == 0:
                        procStr += "\n"
                    # Add a space if not the last entry
                    elif j != len(procPageLocs[i]) - 1:
                        procStr += " "
                    j += 1

                # Add the string
                procPageStrings[i] = procStr

        # Print the table
        print("PAGE TABLE [page,frame]:")

        for i in range(0, 26):
            if len(procPageStrings[i]) > 0:
                print(procPageStrings[i])
