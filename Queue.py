"""
    Support the following operations:
    - Add a Process to Queue
        - Break ties based on alphabetical order
    - Remove a Process from queue
        - Break ties based on alphabetical order
    - Check if empty
    - Check size
"""
class Queue:
    def __init__(self):
        self.Q = []

    def size(self):
        return len(self.Q)

    def enqueue(self, process):
        self.Q.append(process)

    def dequeue(self, process):
        self.data.pop(0)

    def isEmpty(self):
        return not len(self.Q) != 0

    def __repr__(self):
        return str(vars(self))
