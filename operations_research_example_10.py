#! /usr/bin/env python3
"""
Udemy operations research course example 10
"""

from pyscipopt import Model


def main():
    model = Model("example")
    # create the variables
    x = model.addVar(name="x")
    y = model.addVar(name="y")
    # create the objective function
    model.setObjective(coeffs=x + y, sense="maximize")
    # create the constraints
    model.addCons(cons=-x + 2 * y <= 8)
    model.addCons(cons=2 * x + y <= 14)
    model.addCons(cons=-2 * x - y <= 10)
    # invoke the solver
    model.optimize()
    solution = model.getBestSol()
    # display the results
    print(f"x:{solution[x]:6,.1f}")
    print(f"y:{solution[y]:6,.1f}")


if __name__ == "__main__":
    main()
