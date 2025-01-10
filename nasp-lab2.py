from math import floor, log, pow

def DSW(tree: BinaryTree) -> None:
    tree.right_backbone()
    n = tree.node_count()
    m = 2 ** floor(log(n + 1, 2)) - 1
    curr = tree.root
    for _ in range(n - m):
        if curr is not None:
            right = curr.right
            curr.left_rotate(tree)
            curr = right.right if right else None
    
    while m > 1:
        m //= 2
        curr = tree.root
        for _ in range(m):
            if curr is not None:
                right = curr.right
                curr.left_rotate(tree)
                curr = right.right if right else None
