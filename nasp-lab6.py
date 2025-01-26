from typing import Tuple, List, Union, Generator

INF = float('inf')
AdjMatrix = List[List[int]]

def create_adj_matrix(n_nodes: int) -> AdjMatrix:
    return [[0] * n_nodes for _ in range(n_nodes)]


class BellmanFordNode:
    def __init__(self, d_value=INF, prev_node=None):
        self.d = d_value
        self.prev = prev_node

    def __str__(self):
        return f'{self.prev}/{self.d}'

    def __repr__(self):
        return f'BellmanFordNode(d={self.d}, prev={self.prev})'

    def __eq__(self, other):
        if isinstance(other, BellmanFordNode):
            return (self.d, self.prev) == (other.d, other.prev)
        return False


class NegativeCycleError(Exception):
    pass

EdgeIterator = Generator[Tuple[int, int, int], None, None]

class BellmanFordSolution:
    def __init__(self, start: int, solution: List[BellmanFordNode]) -> None:
        self.start = start
        self.distances = solution

    def path_to(self, node: int) -> Tuple[List[int], int]:
        if node >= len(self.distances) or node < 0:
            raise ValueError(f'Invalid node passed as argument to function, must be within: [0, {len(self.distances) - 1}]')

        path = []
        current_node = node
        distance = self.distances[node].d

        if distance == INF:
            return [], INF

        while current_node is not None:
            path.append(current_node)
            current_node = self.distances[current_node].prev

        return path[::-1], distance

    @staticmethod
    def _create_initial_solution(nodes: int) -> List[BellmanFordNode]:
        return [BellmanFordNode() for _ in range(nodes)]

    @staticmethod
    def edges(W: AdjMatrix) -> EdgeIterator:
        for i, row in enumerate(W):
            for j, val in enumerate(row):
                if val != 0:
                    yield i, j, val

    @staticmethod 
    def solve(W: AdjMatrix, start: int) -> 'BellmanFordSolution':
        n_nodes = len(W)
        D = BellmanFordSolution._create_initial_solution(n_nodes)
        D[start].d = 0

        for _ in range(n_nodes - 1):
            for u, v, weight in BellmanFordSolution.edges(W):
                if D[u].d != INF and D[u].d + weight < D[v].d:
                    D[v].d = D[u].d + weight
                    D[v].prev = u

        for u, v, weight in BellmanFordSolution.edges(W):
            if D[u].d != INF and D[u].d + weight < D[v].d:
                raise NegativeCycleError("Negative cycle detected in the graph.")

        return BellmanFordSolution(start, D)

    def __repr__(self) -> str:
        return f'BellmanFordSolution({self.start}, {self.distances})'



if __name__ == "__main__":
    # Test 1: Graf bez negativnog ciklusa
    W = create_adj_matrix(9)
    W[0] = [0, 1, 0, 0, 0, 0, 0, 0, 0]
    W[1] = [0, 0, 0, 0, -5, 0, 0, 0, 0]
    W[2] = [0, 0, 0, 1, 0, 0, 1, 1, 0]
    W[3] = [2, 0, 0, 0, 4, 0, 0, 0, 1]
    W[4] = [0, 0, 0, 0, 0, 4, 0, 0, 0]
    W[5] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    W[6] = [0, 0, 0, -1, 0, 0, 0, 0, 0]
    W[7] = [0, 0, 0, 0, 0, 0, -1, 0, 0]
    W[8] = [0, 0, 0, 0, 0, 1, 0, 0, 0]

    solution = BellmanFordSolution.solve(W, 2)
    path, distance = solution.path_to(5)
    print(f"Path to 5: {path}, Distance: {distance}")
    assert path == [2, 7, 6, 3, 8, 5], "Test 1 failed: Path to node 5 is incorrect."
    assert distance == 1, "Test 1 failed: Distance to node 5 is incorrect."

    # Test 2: Graf s negativnim ciklusom
    W = create_adj_matrix(6)
    W[0] = [0, 10, 0, 0, 0, 0]
    W[1] = [0, 0, 1, 0, 0, 0]
    W[2] = [0, 0, 0, 0, 3, 0]
    W[3] = [0, 4, 0, 0, 0, 0]
    W[4] = [0, 0, 0, -10, 0, 22]
    W[5] = [0, 0, 0, 0, 0, 0]

    was_thrown = False
    try:
        solution = BellmanFordSolution.solve(W, 0)
    except NegativeCycleError:
        was_thrown = True

    print(f"Test 2: Negative cycle detected: {was_thrown}")
    assert was_thrown, "Test 2 failed: NegativeCycleError was not raised for a graph with a negative cycle."

    print("All tests passed!")
