#!/usr/bin/env python3
import plotille
import numpy as np

def main():
    X = np.linspace(0, 5, 100)
    print(plotille.scatter(X, np.sin(X), height=30, width=60))


if __name__ == "__main__":
    main()
