# coding=utf-8

"""
Class representation of a process.
Basically a data container with following attributes:
--- Label
--- Frames Required in Memory
--- Arrival time
--- Run time
"""


class Process():
    def __init__(self, label, frames, arrival, runTime):
        assert (runTime != 0)
        # Only care about the state, burst time and arrival time of a process
        self.label = label
        self.frames = frames
        self.arrivalTime = arrival
        self.runTime = runTime

    # For debugging
    def __repr__(self):
        return(str('Label: {0}'.format(self.label),
        'Frames Required: {0}'.format(self.frames),
        'Arrival time: {0}'.format(self.arrivalTime),
        'Run time: {0}'.format(self.runTime)))
