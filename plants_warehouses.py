#! /usr/bin/env python3

'''
Example of linear programming using PuLP.

Elmhurst University SCM 510 assignment.

./plants_warehouses.py
./plants_warehouses.py > plants_warehouses.txt
'''


from typing import Union, Dict, List, Tuple
import webbrowser
import textwrap
import pprint
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


def pretty_print(object: Union[str, Dict, List, Tuple], label: str) -> None:
    pp = pprint.PrettyPrinter(depth=2, compact=True, sort_dicts=False)
    print(label + ':')
    pp.pprint(object)
    print()


# Define decision variables: plants, warehouses
# Create list of plants
plants = ['Rockford', 'Grand Rapids']
pretty_print(plants, 'Plants')
# pp.pprint(plants)
# print()
# Create list of capacities
capacities = [500, 600]
pretty_print(capacities, 'Capacities')
# Create dictionary of units sent from plants
plant_capacity = dict(zip(plants, capacities))
pretty_print(plant_capacity, 'Plant capacity')
# Create list of warehouses
warehouses = ['Chicago', 'Detroit', 'Indianapolis']
pretty_print(warehouses, 'Warehouses')
# Create list of demand
demand = [400, 300, 350]
pretty_print(demand, 'Demand')
# Create dictionary of warehouse demand
warehouse_demand = dict(zip(warehouses, demand))
pretty_print(warehouse_demand, 'Warehouse demand')
# Create list of lists of transportation costs
# rows = plants, columns = warehouse, entries = costs plant -> warehouse
lane_costs = [
    [10, 16, 12],
    [14, 8, 11]
]
pretty_print(lane_costs, 'Lane costs')
# Create dictionary of transportation costs by plnats, warehouses
warehouse_lane_costs = [dict(zip(warehouses, values)) for values in lane_costs]
pretty_print(warehouse_lane_costs, 'Warehouse lane costs')
plant_warehouse_lane_costs = dict(zip(plants, warehouse_lane_costs))
# print(f'Plant warehouse lane costs:\n{plant_warehouse_lane_costs}\n')
# transportation_costs = utilities.makeDict(
#     headers=[plants, warehouses], array=transportation_costs, default=0
# )
# Create the linear programming model object
pretty_print(plant_warehouse_lane_costs, 'Plant warehouse lane costs')
model = LpProblem(name='plant_warehouse_model', sense=LpMinimize)
# Create list of tuples containing all lanes
lanes = [(plant, warehouse) for plant in plants for warehouse in warehouses]
pretty_print(lanes, 'Lanes')
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
