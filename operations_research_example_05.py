#! /usr/bin/env python3
"""
Udemy operations research course example 05
"""

import pyomo.environ as pyo
from pyomo.opt import SolverFactory


def main():
    m = pyo.ConcreteModel()
    # sets
    m.setO = pyo.Set(initialize=["A", "B", "C", "D", "E"])
    m.R = {"A": 500, "B": 4000, "C": 3000, "D": 2000, "E": 2000}
    m.NT = {"A": 1, "B": 3, "C": 2, "D": 1, "E": 5}
    m.Nteams = 5
    # variables
    m.x = pyo.Var(m.setO, within=pyo.Binary)
    # objective function
    m.obj = pyo.Objective(
        expr=sum([m.x[o]*m.R[o] for o in m.setO]), sense=pyo.maximize
    )
    # constraints
    m.C1 = pyo.Constraint(
        expr=sum([m.x[o]*m.NT[o] for o in m.setO]) <= m.Nteams
    )
    # solve
    opt = SolverFactory("gurobi")
    m.results = opt.solve(m)
    # print
    m.pprint()
    print("\n\nOF:", pyo.value(m.obj))


if __name__ == "__main__":
    main()
