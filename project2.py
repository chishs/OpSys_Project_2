from Simulation import *
import sys

def main(algo, fileName):
    Simulation(algo, fileName);

if __name__ == "__main__":
    main("Next-Fit", sys.argv[1])
    main("First-Fit", sys.argv[1])
    main("Best-Fit", sys.argv[1])
    main("Non-contiguous", sys.argv[1])
