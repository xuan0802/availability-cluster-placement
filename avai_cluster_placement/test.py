# class ShortestTree:
#     def __init__(self, vertices, edges, starting_vertex):
#         self.vertices = vertices
#         self.edges = edges
#         self.start_vertex = starting_vertex
#         # self.AvN = AvN
#
#     def get_neighbors(self, vertex):
#         neighbors = []
#         for e in self.edges:
#             if vertex in e:
#                 for n in e:
#                     if n != vertex:
#                         neighbors.append()
#         return neighbors
#
#     def test(self):
#         root_pair = []
#         # get list root
#         for edge in self.edges:
#             if edge[0] == self.start_vertex:
#                 root_pair.append(self.merge(edge, self.start_vertex, True))
#
#         lst_output = []
#
#         for root in root_pair:
#             remain = self.edges
#             new_root = root
#             temp = remain
#             while(True):
#                 output, remain, new_root = self.make_road(new_root, remain, temp)
#                 if len(output) < 1:
#                     set_tmp = (int(root.split(",")[0]), int(root.split(",")[1]))
#                     if set_tmp not in remain:
#                         print("END!")
#                         break
#                     else:
#                         new_root = root
#                 else:
#                     lst_output.append(output)
#
#         for element in lst_output:
#             ele_len = len(element)
#             print(element[ele_len-1])
#
#         return
#
#     def make_road(self, new_root, tedges, temp):
#         output = []
#         for edge in tedges:
#             if self.merge(new_root, edge) is not None:
#                 print(edge)
#                 temp.remove(edge)
#                 output.append(self.merge(new_root, edge))
#                 new_root = self.merge(new_root, edge)
#
#         return output, temp, new_root
#
#
#     def merge(self, root, edge, start=False):
#         if type(edge) is int:
#             return "%s,%s" % (root[0], root[1])
#         else:
#             if int(root.split(",")[-1]) == edge[0]:
#                 # Add new
#                 return "%s,%s" % (root, edge[1])
#         return None
#
# vertices = [1, 2, 3, 4, 5, 6, 7, 8]
# edges = [(1,2), (2,3), (2,8), (3,8), (3,6), (1,4), (4,3), (4,5), (5,6), (5,7)]
# st = ShortestTree(vertices, edges, 1)
# print(st.test())

#
# vertices = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 't', 'k']
# AvN = dict()
# for vertex in vertices:
#     AvN[vertex] = 0.9
# edges = [('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('c', 'd'), ('c', 'e'), ('d', 'e'), ('b', 'f'),
#          ('c', 'g'), ('e', 't'), ('g', 't'), ('k', 't')]
# t = ShortestTree(vertices, edges, 'a', AvN)
# root = t.build_shortest_tree()from collections import deque, namedtuple
# print(t.max_height)
# d = [1, 2, 3]
#
# # print(d.pop(1))
# dc = ['dc11', 'dc3', 'dc5', 'dc9', 'dc10', 'dc12', 'dc13', 'dc14', 'dc22', 'dc2', 'dc4', 'dc15', 'dc18', 'dc19', 'dc20', 'dc21', 'dc23', 'dc24', 'dc1', 'dc8']
# ed = [('dc1', 'dc2'), ('dc2', 'dc3'), ('dc3', 'dc5'), ('dc3', 'dc4'), ('dc4', 'dc5'), ('dc5', 'dc8'), ('dc9', 'dc10'), ('dc9', 'dc11'), ('dc11', 'dc19'), ('dc11', 'dc15'), ('dc15', 'dc20'), ('dc19', 'dc22'), ('dc11', 'dc12'), ('dc20', 'dc21'), ('dc9', 'dc12'), ('dc10', 'dc13'), ('dc12', 'dc13'), ('dc21', 'dc22'), ('dc22', 'dc23'), ('dc10', 'dc14'), ('dc13', 'dc14'), ('dc14', 'dc18'), ('dc18', 'dc24'), ('dc23', 'dc24')]
# visited = {'dc14', 'dc22', 'dc12', 'dc9', 'dc21', 'dc10', 'dc18', 'dc19', 'dc23', 'dc24', 'dc20', 'dc11', 'dc13', 'dc15'}
# all_vertices = ['dc3', 'dc5', 'dc2', 'dc4', 'dc1', 'dc8']
# for e in ed:
#     if (e[0] in all_vertices and e [1]) in visited or (e[1] in all_vertices and e [0] in visited):
#         print(e)

a = [1, 2]
b = [3, 4]
c = a + b
c[0] = 0
print(c)
print(a)
print(b)