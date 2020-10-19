#! /usr/bin/env python3
'''
Example of linear programming using PuLP.

Elmhurst University SCM 510 assignment.

time -f '%e' ./plants_warehouses.py
./plants_warehouses.py
./plants_warehouses.py > plants_warehouses.txt
'''

from typing import Union, Dict, List, Tuple
import pprint

from pulp import (
    LpProblem, LpMinimize, LpVariable, LpInteger, utilities, lpSum, LpStatus
)
import datasense as ds

header_title = 'Linear Programming---Plants and Warehouses'
header_id = 'linear-programming-plants-and-warehouses'
output_url = 'plants_warehouses.html'


def main():
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    print('<pre style="white-space: pre-wrap;">')
    # Define decision variables: plants, warehouses
    plants = ['Rockford', 'Grand Rapids']
    pretty_print(plants, 'Plants')
    capacities = [500, 600]
    pretty_print(capacities, 'Capacities')
    plant_capacity = dict(zip(plants, capacities))
    pretty_print(plant_capacity, 'Plant capacity')
    warehouses = ['Chicago', 'Detroit', 'Indianapolis']
    pretty_print(warehouses, 'Warehouses')
    demand = [400, 300, 350]
    pretty_print(demand, 'Demand')
    warehouse_demand = dict(zip(warehouses, demand))
    pretty_print(warehouse_demand, 'Warehouse demand')
    # rows = plants, columns = warehouse, entries = costs plant -> warehouse
    lane_costs = [
        [10, 16, 12],
        [14, 8, 11]
    ]
    pretty_print(lane_costs, 'Lane costs')
    # Create dictionary of transportation costs by plnats, warehouses
    warehouse_lane_costs =\
        [dict(zip(warehouses, values)) for values in lane_costs]
    pretty_print(warehouse_lane_costs, 'Warehouse lane costs')
    plant_warehouse_lane_costs = dict(zip(plants, warehouse_lane_costs))
    # Create the linear programming model object
    pretty_print(plant_warehouse_lane_costs, 'Plant warehouse lane costs')
    model = LpProblem(name='plant_warehouse_model', sense=LpMinimize)
    lanes =\
        [(plant, warehouse) for plant in plants for warehouse in warehouses]
    pretty_print(lanes, 'Lanes')
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
              <= plant_capacity[plant],\
              'sum_of_products_out_of_plants_%s' % plant
    for warehouse in warehouses:
        model += lpSum([vars[plant][warehouse] for plant in plants])\
              >= warehouse_demand[warehouse],\
              'sum_of_products_into_warehouses%s'\
              % warehouse
    model.writeLP(filename='plants_warehouses.lp')
    # Solve the model using PuLP's choice of solver
    model.solve(solver=None)
    f = open('plants_warehouses.lp')
    print(f'\n{f.read()}\n')
    f.close()
    print(f'Status = {LpStatus[model.status]}\n')
    # Print resolved optimum value for each lane
    print('Lane shipments')
    for v in model.variables():
        print(v.name, '=', v.varValue)
    print(
        f'\nTotal cost of transportation = {utilities.value(model.objective)}'
    )
    print('</pre>')
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


def pretty_print(
    object: Union[str, Dict, List, Tuple],
    label: str
) -> None:
    '''
    Print data structures for clarity.

    Parameters:
        object  : Union[str, Dict, List, Tuple]
        label   : str
    '''
    pp = pprint.PrettyPrinter(depth=2, compact=True, sort_dicts=False)
    print(label + ':')
    pp.pprint(object)
    print()


if __name__ == '__main__':
    main()
