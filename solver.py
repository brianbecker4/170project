import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import MSTgraph
import tspdp
import greedy
from student_utils import *

"""
======================================================================
  Complete the following function.
======================================================================
"""

def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
        NOTE: both outputs should be in terms of indices not the names of the locations themselves
    """
    # g = MSTgraph.Graph(len(adjacency_matrix))
    # g.graph = adjacency_matrix
    # g.primMST()
    #basic_greedy()
    adjlen = len(adjacency_matrix)
    for x in range(0,len(adjacency_matrix)):
        for y in range(0,len(adjacency_matrix)):
            if adjacency_matrix[x][y] == 'x':
                adjacency_matrix[x][y] = float("inf")
    #------
    # scout = 0
    # removelist = []
    # copy = []
    # temp = []
    # while scout < adjlen:
    #     if adjacency_matrix[scout].count(float("inf")) == len(adjacency_matrix):
    #         removelist.append(scout)
    #     scout += 1
    # point = 0
    # scout = 0
    #
    # while scout < adjlen and point < len(removelist):
    #     if scout == removelist[point]:
    #         point += 1
    #         for x in range(0,adjlen):
    #             if x != scout:
    #                 for y in range(0,len(adjacency_matrix)):
    #                     if y != scout:
    #                         temp.append(adjacency_matrix[x][y])
    #                 copy.append(temp)
    #                 temp = []
    #     else:
    #         temp.append(adja)
    #     scout += 1
    #
    # print(len(copy))
    # print(len(adjacency_matrix))
    donk = greedy.solve_tsp(adjacency_matrix)
    #-----
    print(donk)


    gonk = donk + list(reversed(donk[:-1]))
    val = donk.index(list_of_locations.index(starting_car_location))
    donk1 = donk[:val+1]
    donk2 = donk[val:]
    donk = list(reversed(donk1[1:])) + donk + list(reversed(donk2[:-1]))
    print(donk)
    # print(adjacency_matrix)
    # #boy = preProcess(adjacency_matrix, list_of_homes, list_of_locations)
    # #print(boy)

    # print(adjacency_matrix)
    # g = tspdp.TSP(adjacency_matrix, list_of_locations)
    # path = g.main()

    my_dict = {}
    for x in list_of_homes:
    	my_dict[list_of_locations.index(x)] = [list_of_locations.index(x)]
    print(my_dict)
    print(donk)
    print(list_of_locations.index(starting_car_location))
    print(val)
    #gonk.index(list_of_locations.index(starting_car_location))
    return donk, my_dict


"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)

    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)

    convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
