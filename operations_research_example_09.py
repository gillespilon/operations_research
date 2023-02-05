#! /usr/bin/env python3
"""
Udemy operations research course example 09

https://developers.google.com/optimization/reference/python/index_python
"""

from ortools.linear_solver import pywraplp


def main():
    # declare the solver
    # create the linear solver with the GLOP backend
    # pywraplp is a Python wrapper for the underlying C++ solver
    # the arguement "GLOP" GLOP, the OR-Tools linear solver
    solver = pywraplp.Solver.CreateSolver("GLOP")
    # create the variables
    x = solver.NumVar(0, 10, "x")
    y = solver.NumVar(0, 10, "y")
    # create the constraints
    solver.Add(-x + 2 * y <= 8)
    solver.Add(2 * x + y <= 14)
    solver.Add(2 * x - y <= 10)
    # create the objective function
    solver.Maximize(x + y)
    # invoke the solver
    results = solver.Solve()
    # display the results
    if results == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found")
        print(f"x:{x.solution_value():6,.1f}")
        print(f"y:{y.solution_value():6,.1f}")
    else:
        print("Optimal solution not found")


if __name__ == "__main__":
    main()
