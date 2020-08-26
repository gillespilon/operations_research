#! /usr/bin/env python3

'''
Example of linear programming using PuLP.

Elmhurst University SCM 510 assignment.

./plants_warehouses.py
./plants_warehouses.py > plants_warehouses.txt
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
plant_capacity = {
    'Rockford': 500,
    'Grand Rapids': 600
}
# Create list of warehouses
warehouses = ['Chicago', 'Detroit', 'Indianapolis']
# Create dictionary of warehouse demand
warehouse_demand = {
    'Chicago': 400,
    'Detroit': 300,
    'Indianapolis': 350
}
# Create list of costs, rows = plants, columns = warehouses
transportation_costs = [
    [10, 16, 12],
    [14, 8, 11]
]
# Make costs into dictionary
transportation_costs = utilities.makeDict(
    headers=[plants, warehouses], array=transportation_costs, default=0
)
# Create the linear programming model object
model = LpProblem(name='plant_warehouse_model', sense=LpMinimize)
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
model += lpSum([vars[plant][warehouse]*transportation_costs[plant][warehouse]
               for (plant, warehouse) in routes])
# Add plant capacity maximum constraints to model for each plant
for plant in plants:
    model += lpSum([vars[plant][warehouse] for warehouse in warehouses])\
          <= plant_capacity[plant], 'sum_of_products_out_of_plnats_%s' % plant
for warehouse in warehouses:
    model += lpSum([vars[plant][warehouse] for plant in plants])\
          >= warehouse_demand[warehouse], 'sum_of_products_into_warehouses%s'\
          % warehouse
model.writeLP(filename='plants_warehouses.lp')
# Solve the model using PuLP's choice of solver
model.solve(solver=None)
f = open('plants_warehouses.lp')
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
print('Total cost of transportation =', utilities.value(model.objective))
ds.html_footer()
sys.stdout.close()
sys.stdout = original_stdout
webbrowser.open_new_tab(output_url)
