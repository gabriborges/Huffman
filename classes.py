class Leave:
    def __init__(self, freq, caractere) -> None:
        self.freq = freq
        self.caractere = caractere
        self.left = None
        self.right = None
        
    def __str__(self) -> str:
        return f"{self.freq} {self.caractere}"

class Node:
    def __init__(self, freq, noleft, noRight) -> None:
        self.freq = freq
        self.left = noleft
        self.right = noRight

    def __str__(self) -> str:
        return str(self.freq)

def imprimir_arvore(node, prefix="", is_left=True):
    if node:
        print(prefix + ("|-- " if is_left else "`-- ") + str(node))
        imprimir_arvore(node.left, prefix + ("|   " if is_left else "    "), True)
        imprimir_arvore(node.right, prefix + ("|   " if is_left else "    "), False)