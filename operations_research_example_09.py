#! /usr/bin/env python3
"""
Udemy operations research course example 09

https://developers.google.com/optimization/reference/python/index_python
"""

from ortools.linear_solver import pywraplp


def main():
    solver = pywraplp.Solver.CreateSolver("GLOP")
    x = solver.NumVar(0, 10, "x")
    y = solver.NumVar(0, 10, "y")
    solver.Add(-x + 2 * y <= 8)
    solver.Add(2 * x + y <= 14)
    solver.Add(2 * x - y <= 10)
    solver.Maximize(x + y)
    results = solver.Solve()
    if results == pywraplp.Solver.OPTIMAL:
        print("Optimal solution found")
        print(f"x:{x.solution_value():6,.1f}")
        print(f"y:{y.solution_value():6,.1f}")
    else:
        print("Optimal solution not found")


if __name__ == "__main__":
    main()
