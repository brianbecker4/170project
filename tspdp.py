
import sys
import copy

class TSP():
    def __init__(self, adjacency_matrix, locations):
        self.matrix = adjacency_matrix
        self.data = locations
        self.n = len(self.data)
        self.all_sets = []
        self.g = {}
        self.p = []



    def main(self):
        for x in range(1, self.n):
            self.g[x + 1, ()] = self.matrix[x][0]
        print(self.n)
        print(list(range(2, self.n)))
        print(tuple(list(range(2, self.n))))
        self.get_minimum(1, tuple(list(range(2, self.n))))
        print('\n\nSolution to TSP: {1, ', end='')
        solution = self.p.pop()
        print(solution[1][0], end=', ')
        for x in range(self.n - 2):
            for new_solution in self.p:
                if tuple(solution[1]) == new_solution[0]:
                    solution = new_solution
                    print(solution[1][0], end=', ')
                    break
        print('1}')
        return


    def get_minimum(self, k, a):
        if (k, a) in self.g:
            # Already calculated Set g[%d, (%s)]=%d' % (k, str(a), g[k, a]))
            return self.g[k, a]
        values = []
        all_min = []
        for j in a:
            set_a = copy.deepcopy(list(a))
            set_a.remove(j)
            all_min.append([j, tuple(set_a)])
            result = self.get_minimum(j, tuple(set_a))
            values.append(self.matrix[k-1][j-1] + result)
        # get minimun value from set as optimal solution for
        self.g[k, a] = min(values)
        self.p.append(((k, a), all_min[values.index(self.g[k, a])]))

        return self.g[k, a]
