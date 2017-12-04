"""
    Handles all of the fit algorithms
    --- Next Fit
    --- First Fit
    --- Best Fit
    --- Non-Contiguous
"""

class FitAlgorithms:

    def nextFit(memory, process):
        # TODO: Fill this in

        return memory

    def firstFit(memory, process):
        # TODO: Fill this in

        return memory

    def bestFit(memory, process):
        # TODO: Fill this in

        return memory

    def nonContiguous(memory, process):
        #TODO: Fill this in

        return memory

    def defragmentation(memory):
        nonEmptyFrames = []
        for frame in memory:
            if frame is not '.':
                nonEmptyFrames.append(frame)

        emptyFrames = (256-len(nonEmptyFrames))*['.']

        return nonEmptyFrames + emptyFrames
