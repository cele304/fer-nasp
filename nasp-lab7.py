from typing import Dict, Hashable, List, Set
import collections
import random

class DirectedGraph(object):
    def _init_(self, adjacency_list: Dict[Hashable, Set] = None):
        if adjacency_list is None:
            adjacency_list = {}
        self.vertex_dict = adjacency_list
		  
    def get_vertices(self) -> List:
        return list(self.vertex_dict.keys())

    def get_neighbors(self, vertex: Hashable) -> Set:
        if vertex not in self.vertex_dict.keys():
            raise ValueError(f'Vertex {vertex} does not exist in this graph')
        return self.vertex_dict[vertex]


def detect_cycle(graph):
    visited = set()
    stack = collections.deque()
    def dfs(vertex):
        visited.add(vertex)
        stack.append(vertex)
        for neighbor in graph.get_neighbors(vertex):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in stack:
                return True
        stack.pop()
        return False
    for source in graph.get_vertices():
        if source not in visited:
            if dfs(source):
                return True
    return False


def detect_cycle_recursive(graph, current_vertex, visited, stack):
    visited.append(current_vertex)
    stack.append(current_vertex)
    for neighbor in graph.get_neighbors(current_vertex):
        if neighbor not in visited:
            if detect_cycle_recursive(graph, neighbor, visited, stack):
                return True
        elif neighbor in stack:
            return True
    stack.pop()
    return False

'''
def construct_deterministic1():
    graph_adjacency = {}
    graph_adjacency['a'] = {'b'}
    graph_adjacency['b'] = {'c'}
    graph_adjacency['c'] = {'d', 'e', 'f'}
    graph_adjacency['d'] = set()
    graph_adjacency['e'] = {'b'}
    graph_adjacency['f'] = {'b'}
    return DirectedGraph(graph_adjacency)


def construct_deterministic2():
    graph_adjacency = {}
    graph_adjacency['a'] = {'b'}
    graph_adjacency['b'] = {'c'}
    graph_adjacency['c'] = set()
    graph_adjacency['d'] = set()
    graph_adjacency['e'] = {'b'}
    graph_adjacency['f'] = {'b'}
    return DirectedGraph(graph_adjacency)


def test_detect_cycle(constructor):
    return detect_cycle(constructor())


assert True == test_detect_cycle(construct_deterministic1)
assert False == test_detect_cycle(construct_deterministic2)
print("All tests passed!")
'''
