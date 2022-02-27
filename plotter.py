import matplotlib.pyplot as plot
import argparse
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List Car posts.')
    parser.add_argument('--file',  help="Specify the input csv")
    args = parser.parse_args()

    x = [5,7,8,7,2,17,2,9,4,11,12,9,6]
    y = [99,86,87,88,111,86,103,87,94,78,77,85,86]

    plot.scatter(x, y)
    plot.show()

