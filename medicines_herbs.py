#! /usr/bin/env python3

'''
Example of linear programming using PuLP.

Reference:
https://itnext.io/introduction-to-linear-programming-with-python-1068778600ae

./medicines_herbs.py
./medicines_herbs.py > medicines_herbs.txt
'''


import webbrowser
import textwrap
import sys

from pulp import (
    LpProblem, LpMaximize, LpVariable, LpInteger, LpStatus, utilities
)
import datasense as ds


header_title = 'Linear Programming---Medicines and Herbs'
header_id = 'linear-programming-medicines-and-herbs'
output_url = 'medicines_herbs.html'
wrapper = textwrap.TextWrapper(width=70)
original_stdout = sys.stdout
sys.stdout = open(output_url, 'w')
ds.html_header(
    headertitle=header_title,
    headerid=header_id
)
# Create the linear programming model object
model = LpProblem(name='medicines_and_herbs', sense=LpMaximize)
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
model += 25*x + 20*y, 'health restored, to be maximized'
# Add the constraints
model += 3*x + 4*y <= 25, 'herb A constraint'
model += 2*x + y <= 10, 'herb B constraint'
# Write the model data to a .lp file
model.writeLP(
    filename='medicines_herbs.lp'
)
# Solve the model using PuLP's choice of solver
model.solve(solver=None)
f = open('medicines_herbs.lp')
print(f.read())
f.close()
print()
# Capture the stdout for solve
# f = open('plants_warehouses.txt')
# print(f.read())
# f.close()
# print()
# Print status of solution
print('Status', LpStatus[model.status])
# Print each variable with it' resolved optimum value
for v in model.variables():
    print(v.name, '=', v.varValue)
# Print the optimized objective function
print('Objective value =', utilities.value(model.objective))
ds.html_footer()
sys.stdout.close()
sys.stdout = original_stdout
webbrowser.open_new_tab(output_url)
