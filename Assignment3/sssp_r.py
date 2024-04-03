"""
File that includes code for the single source shortest paths algorithm,
and the all-pairs shortest paths algorithm.
"""

import numpy as np


def sssp_r(source, target, adj_dict):

    frontier = [(source, 0, None)]
    explored = []
    while len(frontier) > 0:
        frontier.sort(key=lambda x: x[1])

        #print(f'sorted frontier is {frontier}')
        curr_node = frontier[0]
        #print(f'current node {curr_node}')
        del frontier[0]
        #print(f'updated frontier is {frontier}')
        

        if curr_node[0] == target:
            #print(f'solution found!, {curr_node}')
            return curr_node[1]
        
        explored += [curr_node]
        explored_nodes = [node for node, cost, parent in explored]
        #print(f'explored nodes {explored}')

        neighbors = adj_dict[curr_node[0]]
        # Neighbors with cost from source
        neighbs_wcfs = [(node, cost + curr_node[1], curr_node[0]) for node, cost in neighbors]
        #print(f'neighbors with cost {neighbs_wcfs}')

        frontier_nodes = [node for node, cost, parent in frontier]
        for neighbor in neighbs_wcfs:
            if neighbor[0] not in explored_nodes:
                if neighbor[0] in frontier_nodes:
                    # Node in frontier index
                    nif_ind = frontier_nodes.index(neighbor[0])
                    if frontier[nif_ind][1] > neighbor[1]:
                        # if neighbor is better than established, replace

                        #print(f'found better cost to get to {neighbor[0]}, \
                            #in frontier {frontier[nif_ind]} and now {neighbor}')
                        del frontier[nif_ind]
                        frontier += [neighbor]

                else:
                    #print(f'adding node {neighbor[0]} to frontier it wasnt there.')
                    frontier += [neighbor]
    print('no solution found')
    return -1


def apsp_r(S, adj_mat):
    # I convert C to an adjacency dictionary for ease to call dijkstra.
    # Adjacency matrix shape
    adjm_shape = adj_mat.shape
    adj_dict = {}
    for i in range(adjm_shape[0]):
        adj_dict[S[i]] = []
        for j in range(adjm_shape[1]):
            adj_dict[S[i]] += [(S[j], adj_mat[i, j])]

    v = len(S)
    apsp_r = np.zeros((v, v))
    for target in S:
        ind_t = S.index(target)
        for char in S:
            ind_char = S.index(char)
            # Replacement cost
            rc = sssp_r(char, target, adj_dict)            
            apsp_r[ind_char, ind_t] = rc

    return apsp_r

#adj_dict = {'a': [('a', 0), ('b', 100), ('c', 1), ('d', 100)], 
# 'b': [('a', 0), ('b', 0), ('c', 0), ('d', 0)],
# 'c': [('a', 0), ('b', 10), ('c', 0), ('d', 0)],
# 'd': [('a', 0), ('b', 0), ('c', 0), ('d', 0)]}

#xd, xdd = sssp('a', 'd', adj_dict)
#print(f'frontier {xd}')
#print(f'explored {xdd}')