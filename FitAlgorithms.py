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

    def nextFit(memory, process, framesLeft, prevProc):
        framesReq = process.frames
        frameCount = 0
        timeIncrease = 0
        startIndex = 0
        added = False
        procStr = ""

        if framesReq > framesLeft:
            return (memory, 0, procStr)

        elif prevProc is not None:
            # Find location of the previous process
            for i in range(0, len(memory)):
                if memory[i] == prevProc.label:
                    while i < 256 and memory[i] != '.':
                        i += 1
                    startIndex = i

                    # Get the length of the frame after the last place proc
                    while i < 256 and memory[i] == '.':
                        i+= 1
                        frameCount += 1

                    if frameCount >= framesReq:
                        added = True
                        for j in range(startIndex, startIndex+framesReq):
                            memory[j] = process.label
                        frameCount = 0
                        startIndex = 0
                        break

                    elif i == 256:
                        # Find the first spot from the top (Same as First-Fit)
                        frameCount = 0
                        startIndex = 0
                        if i == 256:
                            i = 0
                        added = True
                        temp = FitAlgorithms.firstFit(memory, process, framesLeft)
                        return (temp[0], temp[1], temp[2])
        else:
            temp = FitAlgorithms.firstFit(memory, process, framesLeft)
            return (temp[0], temp[1], temp[2])
        if not added:
            # Defragment
            temp = FitAlgorithms.defragmentation(memory)
            memory = temp[0]
            timeIncrease = temp[1]
            procStr = temp[2]

            # Add the process
            for i in range(0, len(memory)):
                if memory[i] == '.':
                    for j in range(0, process.frames):
                        memory[i+j] = process.label
                    break

        return (memory, timeIncrease, procStr)

    def bestFit(memory, process, framesLeft):
        framesReq = process.frames
        frameCount = 0
        timeIncrease = 0
        startIndex = 0
        added = False
        procStr = ""
        freePartitions = []

        if framesReq > framesLeft:
            return (memory, 0, procStr)

        else:
            # Create a way to find the smallest free partition process will fit in
            j = 0
            while j < 256:
                if memory[j] == '.':
                    startIndex = j
                    while j < 256 and memory[j] == '.':
                        j += 1
                        frameCount += 1
                    freePartitions.append((startIndex, frameCount))
                    startIndex = 0
                    frameCount = 0
                else:
                    j += 1
            j = 0

            minPartition = (0, -1)
            for i in range(0, len(freePartitions)):
                frameDif = freePartitions[i][1] - process.frames
                if (frameDif >= 0 and frameDif < minPartition[1]) or minPartition[1] == -1:
                    minPartition = freePartitions[i]
                    added = True

            if minPartition[1] < process.frames:
                # Defragment
                temp = FitAlgorithms.defragmentation(memory)
                memory = temp[0]
                timeIncrease = temp[1]
                procStr = temp[2]

                # Add the process
                for i in range(0, len(memory)):
                    if memory[i] == '.':
                        for k in range(0, process.frames):
                            memory[i+k] = process.label
                        break

            else:
                startIndex = minPartition[0]
                for i in range(startIndex, startIndex + process.frames):
                    memory[i] = process.label

        return (memory, timeIncrease, procStr)

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

        return (memory, timeIncrease, procStr)
