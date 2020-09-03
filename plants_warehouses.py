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
# Define decision variables: plants, warehouses
# Create list of plants
plants = ['Rockford', 'Grand Rapids']
print(f'Plants:\n{plants}\n')
# Create list of capacities
capacities = [500, 600]
print(f'Capacities:\n{capacities}\n')
# Create dictionary of units sent from plants
plant_capacity = dict(zip(plants, capacities))
print(f'Plant capacity:\n{plant_capacity}\n')
# Create list of warehouses
warehouses = ['Chicago', 'Detroit', 'Indianapolis']
print(f'Warehouses:\n{warehouses}\n')
# Create list of demand
demand = [400, 300, 350]
print(f'Demand:\n{demand}\n')
# Create dictionary of warehouse demand
warehouse_demand = dict(zip(warehouses, demand))
print(f'Warehouse demand:\n{warehouse_demand}\n')
# Create list of lists of transportation costs
# rows = plants, columns = warehouse, entries = costs plant -> warehouse
lane_costs = [
    [10, 16, 12],
    [14, 8, 11]
]
print(f'Lane costs:\n{lane_costs}\n')
# Create dictionary of transportation costs by plnats, warehouses
warehouse_lane_costs = [dict(zip(warehouses, values)) for values in lane_costs]
print(f'Warehouse lane costs:\n{warehouse_lane_costs}\n')
plant_warehouse_lane_costs = dict(zip(plants, warehouse_lane_costs))
print(f'Plant warehouse lane costs:\n{plant_warehouse_lane_costs}\n')
# transportation_costs = utilities.makeDict(
#     headers=[plants, warehouses], array=transportation_costs, default=0
# )
# Create the linear programming model object
model = LpProblem(name='plant_warehouse_model', sense=LpMinimize)
# Create list of tuples containing all lanes
lanes = [(plant, warehouse) for plant in plants for warehouse in warehouses]
print(f'Lanes:\n{lanes}\n')
# Create dictionary containing all lanes
vars = LpVariable.dicts(
    name='Lane',
    indexs=(plants, warehouses),
    lowBound=0,
    upBound=None,
    cat=LpInteger
)
# Add the objective function
model += lpSum(
    [vars[plant][warehouse]*plant_warehouse_lane_costs[plant][warehouse]
     for (plant, warehouse) in lanes]
)
# Add plant capacity maximum constraints to model for each plant
for plant in plants:
    model += lpSum([vars[plant][warehouse] for warehouse in warehouses])\
          <= plant_capacity[plant], 'sum_of_products_out_of_plants_%s' % plant
for warehouse in warehouses:
    model += lpSum([vars[plant][warehouse] for plant in plants])\
          >= warehouse_demand[warehouse], 'sum_of_products_into_warehouses%s'\
          % warehouse
model.writeLP(filename='plants_warehouses.lp')
# Solve the model using PuLP's choice of solver
model.solve(solver=None)
f = open('plants_warehouses.lp')
print(f'\n{f.read()}\n')
f.close()
# Capture the stdout for solve
# f = open('plants_warehouses.txt')
# print(f.read())
# f.close()
# print()
# Print status of solution
print(f'Status = {LpStatus[model.status]}\n')
# Print resolved optimum value for each lane
print('Lane shipments')
for v in model.variables():
    print(v.name, '=', v.varValue)
# Print the optimized objective function
print(f'\nTotal cost of transportation = {utilities.value(model.objective)}')
ds.html_footer()
sys.stdout.close()
sys.stdout = original_stdout
webbrowser.open_new_tab(output_url)
