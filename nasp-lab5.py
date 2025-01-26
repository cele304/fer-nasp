import heapq

TOL_DEC = 3
TOLERANCE = 10**-TOL_DEC


class Node:

    def __init__(self, prob, symbol, left=None, right=None):
        self.prob = prob
        self.symbol = symbol
        self.left = left
        self.right = right
        self.code = ''

    def __lt__(self, other: 'Node') -> bool:
        if abs(self.prob - other.prob) > TOLERANCE:
            return self.prob < other.prob
        return self.symbol < other.symbol


def Huffman_tree(symbol_with_probs: dict) -> Node:
    nodes_queue = []

    for symbol, prob in symbol_with_probs.items():
        heapq.heappush(nodes_queue, Node(prob, symbol))

    while len(nodes_queue) > 1:
        left = heapq.heappop(nodes_queue)
        right = heapq.heappop(nodes_queue)

        combined_symbol = ''.join(sorted(left.symbol + right.symbol))
        combined_prob = left.prob + right.prob
        new_node = Node(combined_prob, combined_symbol, left, right)

        left.code = '0'
        right.code = '1'

        heapq.heappush(nodes_queue, new_node)

    return nodes_queue[0]


####################### IT'S BETTER NOT TO MODIFY THE CODE BELOW ##############

def calculate_codes(node: Node, val: str = '', codes=dict()) -> dict:
    newVal = val + str(node.code)

    if(node.left):
        calculate_codes(node.left, newVal, codes)
    if(node.right):
        calculate_codes(node.right, newVal, codes)

    if(not node.left and not node.right):
        codes[node.symbol] = newVal

    return codes


def Huffman_encode(data: str, coding: dict) -> str:
    encoding_output = []
    for c in data:
        encoding_output.append(coding[c])
    string = ''.join([str(item) for item in encoding_output])
    return string


def Huffman_decode(encoded_data: str, huffman_tree: Node) -> str:
    tree_head = huffman_tree
    decoded_output = []
    for x in encoded_data:
        if x == '1':
            huffman_tree = huffman_tree.right
        elif x == '0':
            huffman_tree = huffman_tree.left
        # check if leaf
        if huffman_tree.left is None and huffman_tree.right is None:
            decoded_output.append(huffman_tree.symbol)
            huffman_tree = tree_head

    string = ''.join([str(item) for item in decoded_output])
    return string


def roundToDecimals(num: float, decimals: int) -> float:
    return round(num*10**decimals)/10**decimals






symbols_with_probs={'A':0.13,'B':0.21,'C':0.39,'D':0.19,'E':0.08}
print('problem: ', symbols_with_probs)
tree=Huffman_tree(symbols_with_probs)
huffman_code = calculate_codes(tree)
print('encoding:',huffman_code)

data = 'DEBADE'
print('original text: ',data)

print('-------ENCODE--------')
enc=Huffman_encode(data,huffman_code)
print('data encoded: ',enc)

print('-------DECODE--------')
print('data decoded back: ',Huffman_decode(enc,tree))

""" # ispravan izlaz
problem:  {'A': 0.13, 'B': 0.21, 'C': 0.39, 'D': 0.19, 'E': 0.08}
encoding: {'D': '00', 'E': '010', 'A': '011', 'B': '10', 'C': '11'}
original text:  DEBADE
-------ENCODE--------
data encoded:  000101001100010
-------DECODE--------
data decoded back:  DEBADE
"""
