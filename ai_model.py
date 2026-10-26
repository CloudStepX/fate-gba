class Node:
    def __init__(self, value):
        self.value = value
        self.children = {}

class AI:
    def __init__(self):
        self.root = Node(None)
    def add_node(self, path, value):
        current = self.root
        for key in path:
            if key not in current.children:
                current.children[key] = Node(None)
            current = current.children[key]
        current.value = value
    def query(self, path):
        current = self.root
        for key in path:
            if key not in current.children:
                return None
            current = current.children[key]
        return current.value