#! /usr/bin/env python3

'''
Example of linear programming using PuLP.

Elmhurst University SCM 510 assignment.
'''


import webbrowser
import textwrap
import sys

from pulp import (
    LpProblem, LpMinimize, LpVariable, LpInteger, utilities, lpSum, LpStatus
)
import datasense as ds


header_title = 'Linear Programming---Plants and Warehouses'
header_id = 'linear-programming-plants-and-warehouses'
output_url = 'plants_warehouses.html'
wrapper = textwrap.TextWrapper(width=70)
original_stdout = sys.stdout
sys.stdout = open(output_url, 'w')
ds.html_header(
    headertitle=header_title,
    headerid=header_id
)
# Create list of plants
plants = ['Rockford', 'Grand Rapids']
# Create dictionary of units sent from plants
supply = {
    'Rockford': 500,
    'Grand Rapids': 600
}
# Create list of warehouses
warehouses = ['Chicago', 'Detroit', 'Indianapolis']
# Create dictionary of warehouse demand
demand = {
    'Chicago': 400,
    'Detroit': 300,
    'Indianapolis': 350
}
# Create list of costs, rows = plants, columns = warehouses
costs = [
    [10, 16, 12],
    [14, 8, 11]
]
# Make costs into dictionary
costs = utilities.makeDict(
    headers=[plants, warehouses], array=costs, default=0
)
# Create the linear programming problem object
problem = LpProblem(name='plant_warehouse_problem', sense=LpMinimize)
# Create list of tuples containing all lanes
routes = [(plant, warehouse) for plant in plants for warehouse in warehouses]
# Create dictionary containing all lanes
vars = LpVariable.dicts(
    name='route',
    indexs=(plants, warehouses),
    lowBound=0,
    upBound=None,
    cat=LpInteger
)
# Add the objective function
problem += lpSum([vars[plant][warehouse]*costs[plant][warehouse]
                 for (plant, warehouse) in routes])
# Add supply maximum constraints to problem for each supply note (plant)
for plant in plants:
    problem += lpSum([vars[plant][warehouse] for warehouse in warehouses])\
            <= supply[plant], 'sum_of_products_out_of_plnats_%s' % plant
for warehouse in warehouses:
    problem += lpSum([vars[plant][warehouse] for plant in plants])\
            >= demand[warehouse], 'sum_of_products_into_warehouses%s'\
            % warehouse
problem.writeLP(filename='plants_warehouses.lp')
# Solve the problem using PuLP's choice of solver
problem.solve(solver=None)
f = open('plants_warehouses.lp')
print(f.read())
f.close()
print()
# Print status of solution
print('Status', LpStatus[problem.status])
# Print each variable with it' resolved optimum value
for v in problem.variables():
    print(v.name, '=', v.varValue)
# Print the optimized objective function
print('Total cost of transportation =', utilities.value(problem.objective))
ds.html_footer()
sys.stdout.close()
sys.stdout = original_stdout
webbrowser.open_new_tab(output_url)
