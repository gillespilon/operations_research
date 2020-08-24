#! /usr/bin/env python3

'''
Example of linear programming using PuLP.

Reference:
https://itnext.io/introduction-to-linear-programming-with-python-1068778600ae
'''


from pulp import LpProblem, LpMaximize, LpVariable, LpInteger


# Create the linear programming problem object
problem = LpProblem(name='medicines_and_herbs', sense=LpMaximize)
# Create the linear programming variable objects
x = LpVariable(
    name='medicine_1_units',
    lowBound=0,
    upBound=None,
    cat=LpInteger
)
y = LpVariable(
    'medicine_2_units',
    0,
    None,
    LpInteger
)
# Add the objective function
problem += 25*x + 20*y, 'health restored, to be maximized'
# Add the constraints
problem += 3*x + 4*y <= 25, 'herb A constraint'
problem += 2*x + y <= 10, 'herb B constraint'
# Write the problem data to a .lp file
problem.writeLP(
    'medicines_herbs.lp'
)
# Solve the problem using PuLP's choice of solver
problem.solve()
