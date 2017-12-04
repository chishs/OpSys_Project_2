"""
    Handles all of the fit algorithms
    --- Next Fit
    --- First Fit
    --- Best Fit
    --- Non-Contiguous
"""

class FitAlgorithms:

    def firstFit(memory, process, framesLeft):
        framesReq = process.frames
        frameCount = 0
        startIndex = 0
        added = False
        procStr = ""

        # Tell simulation how much time to add if defragmenting
        timeIncrease = 0

        # Make sure there is enough space
        if framesLeft < framesReq:
            return (memory, 0, "")

        # Try to add the process without defragmentation
        for i in range(0, len(memory)):
            if memory[i] == '.':
                startIndex = i
                # Count the number of free spots
                while i < 256:
                    if memory[i] == '.':
                        frameCount += 1
                        i += 1
                    else:
                        break

                # Add the process if enough space
                if frameCount >= framesReq:
                    # Place the process in this memory block
                    for j in range(startIndex, startIndex+framesReq):
                        memory[j] = process.label
                    added = True
                    break
                else:
                    frameCount = 0

        # If it was not added and there is room for the
        # process to be added
        if not added:
            # Defragment
            temp = FitAlgorithms.defragmentation(memory)
            memory = temp[0]
            timeIncrease = temp[1]
            procStr = temp[2]

            for i in range(0, len(memory)):
                if memory[i] == '.':
                    for j in range(0, process.frames):
                        memory[i+j] = process.label
                    break

        return (memory, timeIncrease, procStr)

    def nextFit(memory, process, framesLeft):
        # TODO: Fill this in

        return memory

    def bestFit(memory, process, framesLeft):
        # TODO: Fill this in

        return memory

    def nonContiguous(memory, process, framesLeft):
        #TODO: Fill th== in

        return memory

    def defragmentation(memory):
        timeIncrease = 0
        freeSpotsAtEnd = 0
        procMoved = []
        # Calculate time increase
        for i in range(0, len(memory)):
            if memory[i] != '.':
                if i > 0 and memory[i-1] == '.':
                    while memory[i] != '.':
                        if not memory[i] in procMoved:
                            procMoved.append(memory[i])
                        timeIncrease += 1
                        i += 1

        # Calculate the number of free spots at end of memory
        for i in range(len(memory)-1, 0):
            if memory[i] == '.':
                freeSpotsAtEnd += 1
            else:
                break

        nonEmptyFrames = []
        for frame in memory:
            if frame != '.':
                nonEmptyFrames.append(frame)

        emptyFrames = (256-len(nonEmptyFrames))*['.']

        memory = nonEmptyFrames + emptyFrames

        procStr = ""
        # Generate the moved processes string
        for i in range(0, len(procMoved)):
            procStr += procMoved[i]
            if i != len(procMoved) - 1:
                procStr += " "

        print(procStr)

        return (memory, timeIncrease, procStr)
