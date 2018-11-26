from copy import deepcopy


class Node:
    def __init__(self, name, avail, type):
        self.name = name
        self.type = type
        self.avail = avail
        self.children = []
        self.parent = None

    def add_child(self, node):
        self.children.append(node)

    def add_parent(self, node):
        self.parent = node


class ShortestTree:
    def __init__(self, vertices, edges, starting_vertex, AvN):
        self.vertices = deepcopy(vertices)
        self.edges = deepcopy(edges)
        self.start_vertex = starting_vertex
        self.AvN = AvN
        self.max_height = None

    def get_neighbors(self, vertex):
        neighbors = []
        for e in self.edges:
            if vertex in e:
                for n in e:
                    if n != vertex:
                        neighbors.append(n)
        return neighbors

    # build a shortest tree from one node to all nodes from a graph
    def build_shortest_tree(self):
        visited_vertices = set()
        all_vertices = deepcopy(self.vertices)
        root = Node(self.start_vertex, self.AvN[self.start_vertex], 'root')
        current_nodes = list()
        current_nodes.append(root)
        self.max_height = -1

        while all_vertices:
            self.max_height += 1
            for node in current_nodes:
                visited_vertices.add(node.name)
            new_current_nodes = list()
            for node in current_nodes:
                neighbors = self.get_neighbors(node.name)
                for n in neighbors:
                    if n not in visited_vertices:

                        child_node = Node(n, self.AvN[n], 'node')
                        node.add_child(child_node)
                        child_node.add_parent(node)
                        new_current_nodes.append(child_node)
            current_nodes = new_current_nodes
            for vertex in visited_vertices:
                if vertex in all_vertices:
                    all_vertices.remove(vertex)
        return root

    # get all branches which have the length of k
    def get_k_length_branches(self, root, k):
        all_branches = []
        output_nodes = []
        self.get_k_level_nodes(root, k, output_nodes)
        for node in output_nodes:
            reverse_path = []
            self.traverse_back(node, reverse_path)
            all_branches.append(reverse_path)
        return all_branches

    # get the reverse path to root from arbitrary node
    def traverse_back(self, node, reverse_path):
        reverse_path.append(node.name)
        if node.type != 'root':
            self.traverse_back(node.parent, reverse_path)

    # get all nodes at level k, root has level 0
    def get_k_level_nodes(self, root, k, output_nodes):
        if k == 0:
            output_nodes.append(root)
        else:
            for node in root.children:
                self.get_k_level_nodes(node, k-1, output_nodes)
