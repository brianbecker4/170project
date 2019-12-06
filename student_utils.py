import networkx as nx
import numpy as np


def basic_greedy():
    # greedy search algorithm
    d_dict = {1: [(1,0),(2, 15), (3, 30), (8, 20)], 2:[(1,15)]}  # dict of lists of tuples such that nodei : [ (neighbourj, distancej), .... ]
    currentCity = 1
    tour = []   # list of covered nodes
    tour.append(currentCity)
    distanceTravelled = 0   # distance travelled in tour
    while len(set([neighbourCity for (neighbourCity, distance) in d_dict.get(currentCity, [])]).difference(set(tour))) > 0:  # set(currentCityNeighbours) - set(visitedNodes)
        # way 1 starts
        # minDistanceNeighbour = None
        # minDistance = None
        # for eachNeighbour, eachNeighbourdDistance in d_dict[currentCity]:
        #     if eachNeighbour != currentCity and eachNeighbour not in tour:
        #         if minDistance is not None:
        #             if minDistance > eachNeighbourdDistance:
        #                 minDistance = eachNeighbourdDistance
        #                 minDistanceNeighbour = eachNeighbour
        #         else:
        #             minDistance = eachNeighbourdDistance
        #             minDistanceNeighbour = eachNeighbour
        # nearestNeigbhourCity = (minDistanceNeighbour, minDistance)
        # way 1 ends
        # way 2 starts
        nearestNeigbhourCity = min(d_dict[currentCity], key=lambda someList: someList[1] if someList[0] not in tour else 1000000000)  # else part returns some very large number
        # way 2 ends
        tour.append(nearestNeigbhourCity[0])
        currentCity = nearestNeigbhourCity[0]
        distanceTravelled += nearestNeigbhourCity[1]
    print(tour)
    print(distanceTravelled)
"""
prune leaves from graph
"""
def prune_leaf(adjacency_matrix, list_of_homes, list_of_locations):
    new = adjacency_matrix
    for x in range(0,len(adjacency_matrix)):
        is_empty = True
        is_leaf = True
        is_prune = False
        for y in adjacency_matrix[x]:
            if y != 'x' and is_empty == False:
                is_leaf = False
            if y != 'x':
                is_empty = False
        if is_leaf:
            if list_of_locations[x] not in list_of_homes:
                is_prune = True
        if is_empty:
            is_prune = True
        if is_prune:
            new[x] = [0] * len(adjacency_matrix)
    return new
"""preprocess"""
def preProcess(adjacency_matrix, list_of_homes, list_of_locations):
    newMatrix = prune_leaf(adjacency_matrix, list_of_homes, list_of_locations)

    arr_of_ones = np.apply_along_axis(check_if_zero, 1, newMatrix)
    combine_dict = {}
    for x in arr_of_ones:
        count_of_index_changes = 0
        if x == 1:
            # delete row
            deleted_row_matrix = np.delete(newMatrix, x, 0)
            deleted_col_matrix = np.delete(deleted_row_matrix, x, 1)
            count_of_index_changes -= 1

            # merge with previous
            to_merge_loc = list_of_locations[x + count_of_index_changes]
            to_merge_to_loc = list_of_locations[x - 1 + count_of_index_changes]
            combine_dict[to_merge_to_loc] = to_merge_loc
    return deleted_col_matrix


def check_if_zero(arr):
    count = 0
    for x in range(len(arr)):
        if arr[x] != 0:
            count += 1
    return count

def decimal_digits_check(number):
    number = str(number)
    parts = number.split('.')
    if len(parts) == 1:
        return True
    else:
        return len(parts[1]) <= 5


def data_parser(input_data):
    number_of_locations = int(input_data[0][0])
    number_of_houses = int(input_data[1][0])
    list_of_locations = input_data[2]
    list_of_houses = input_data[3]
    starting_location = input_data[4][0]

    adjacency_matrix = [[entry if entry == 'x' else float(entry) for entry in row] for row in input_data[5:]]
    return number_of_locations, number_of_houses, list_of_locations, list_of_houses, starting_location, adjacency_matrix


def adjacency_matrix_to_graph(adjacency_matrix):
    node_weights = [adjacency_matrix[i][i] for i in range(len(adjacency_matrix))]
    adjacency_matrix_formatted = [[0 if entry == 'x' else entry for entry in row] for row in adjacency_matrix]

    for i in range(len(adjacency_matrix_formatted)):
        adjacency_matrix_formatted[i][i] = 0

    G = nx.convert_matrix.from_numpy_matrix(np.matrix(adjacency_matrix_formatted))

    message = ''

    for node, datadict in G.nodes.items():
        if node_weights[node] != 'x':
            message += 'The location {} has a road to itself. This is not allowed.\n'.format(node)
        datadict['weight'] = node_weights[node]

    return G, message


def is_metric(G):
    shortest = dict(nx.floyd_warshall(G))
    for u, v, datadict in G.edges(data=True):
        if abs(shortest[u][v] - datadict['weight']) >= 0.00001:
            return False
    return True


def adjacency_matrix_to_edge_list(adjacency_matrix):
    edge_list = []
    for i in range(len(adjacency_matrix)):
        for j in range(len(adjacency_matrix[0])):
            if adjacency_matrix[i][j] == 1:
                edge_list.append((i, j))
    return edge_list


def is_valid_walk(G, closed_walk):
    if len(closed_walk) == 2:
        return closed_walk[0] == closed_walk[1]
    return all([(closed_walk[i], closed_walk[i+1]) in G.edges for i in range(len(closed_walk) - 1)])


def get_edges_from_path(path):
    return [(path[i], path[i+1]) for i in range(len(path) - 1)]

"""
G is the adjacency matrix.
car_cycle is the cycle of the car in terms of indices.
dropoff_mapping is a dictionary of dropoff location to list of TAs that got off at said droppoff location
in terms of indices.
"""
def cost_of_solution(G, car_cycle, dropoff_mapping):
    cost = 0
    message = ''
    dropoffs = dropoff_mapping.keys()
    if not is_valid_walk(G, car_cycle):
        message += 'This is not a valid walk for the given graph.\n'
        cost = 'infinite'

    if not car_cycle[0] == car_cycle[-1]:
        message += 'The start and end vertices are not the same.\n'
        cost = 'infinite'
    if cost != 'infinite':
        if len(car_cycle) == 1:
            car_cycle = []
        else:
            car_cycle = get_edges_from_path(car_cycle[:-1]) + [(car_cycle[-2], car_cycle[-1])]
        if len(car_cycle) != 1:
            driving_cost = sum([G.edges[e]['weight'] for e in car_cycle]) * 2 / 3
        else:
            driving_cost = 0
        walking_cost = 0
        shortest = dict(nx.floyd_warshall(G))

        for drop_location in dropoffs:
            for house in dropoff_mapping[drop_location]:
                walking_cost += shortest[drop_location][house]

        message += f'The driving cost of your solution is {driving_cost}.\n'
        message += f'The walking cost of your solution is {walking_cost}.\n'
        cost = driving_cost + walking_cost

    message += f'The total cost of your solution is {cost}.\n'
    return cost, message


def convert_locations_to_indices(list_to_convert, list_of_locations):
    return [list_of_locations.index(name) if name in list_of_locations else None for name in list_to_convert]
