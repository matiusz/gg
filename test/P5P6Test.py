import unittest
import networkx as nx
from visu import TieredGraph, Vertex, GraphMatcherByLabel
from collections import deque

def double_key_sort(l):
    return sorted(sorted(l, key = lambda x: x[1]), key = lambda x: x[0])

class P5P6Test(unittest.TestCase):

    def setUp(self):
        v1 = (-1, 1)
        v2 = (1, 1)
        v3 = (-1, -1)
        v4 = (1, -1)
        self.graph = TieredGraph((v1, v2, v3, v4))

    def validate_tiers(self, graph, expectedTiers):
        self.assertEqual(sorted(expectedTiers), sorted(
            list(map(lambda vertex: vertex.__repr__(), graph.tiers))))

    def validate_graph(self, expected_nodes, expected_edges):
        self.validate_nodes(expected_nodes)
        self.validate_edges(expected_edges)

    def validate_nodes(self, expected_nodes):
        self.assertEqual(sorted(expected_nodes),
                         sorted([node.__repr__() for node in dict(self.graph.graph.nodes).keys()]))


    def validate_edges(self, expected_edges):
        self.assertEqual(double_key_sort(expected_edges),
                         double_key_sort([(pair[0].__repr__(), pair[1].__repr__()) for pair in list(self.graph.graph.edges)]))
        
    
    # def test_p5(self):
    #     expected_tiers = ['[e vertex at (0, 0) and level 0]',
    #                       '[E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex at (-1, -1) and level 1, E vertex at (1, -1) and level 1, I vertex at (0.0, 0.0) and level 1]']

    #     expected_nodes = ['e vertex at (0, 0) and level 0',
    #                       'E vertex at (-1, 1) and level 1',
    #                       'E vertex at (1, 1) and level 1',
    #                       'E vertex at (-1, -1) and level 1',
    #                       'E vertex at (1, -1) and level 1',
    #                       'I vertex at (0.0, 0.0) and level 1']

    #     expected_edges = [('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
    #                       ('E vertex at (-1, 1) and level 1',
    #                        'E vertex at (-1, -1) and level 1'),
    #                       ('E vertex at (-1, 1) and level 1',
    #                        'I vertex at (0.0, 0.0) and level 1'),
    #                       ('E vertex at (1, 1) and level 1',
    #                        'E vertex at (1, -1) and level 1'),
    #                       ('E vertex at (1, 1) and level 1',
    #                        'I vertex at (0.0, 0.0) and level 1'),
    #                       ('E vertex at (-1, -1) and level 1',
    #                        'E vertex at (1, -1) and level 1'),
    #                       ('E vertex at (-1, -1) and level 1',
    #                        'I vertex at (0.0, 0.0) and level 1'),
    #                       ('E vertex at (1, -1) and level 1', 'I vertex at (0.0, 0.0) and level 1')]
        
    #     LHS = nx.Graph()
    #     LHS.add_node(v0 := Vertex(None, "E", 0))
    #     matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
    #     match = next(matches)
    #     assert match is not None, f"P1: No match for {v0} found!"
    #     RHS = nx.Graph()
    #     RHS.add_node(v0 := Vertex(list(match.keys())[0].position, "e", 0))
    #     RHS.add_node(v1 := Vertex(self.graph.corners[0], "E", 1))
    #     RHS.add_node(v2 := Vertex(self.graph.corners[1], "E", 1))
    #     RHS.add_node(v3 := Vertex(self.graph.corners[2], "E", 1))
    #     RHS.add_node(v13 := Vertex(((self.graph.corners[0][0] + self.graph.corners[2][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2), "E", 1))
    #     RHS.add_node(v4 := Vertex(self.graph.corners[3], "E", 1))
        

    #     RHS.add_node(i := Vertex(((self.graph.corners[0][0] + self.graph.corners[1][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2), "I", 1))
    #     RHS.add_edges_from([(v1, v2), (v2, v4), (v4, v3), (v3, v13), (v13, v1),
    #                         (v2, i), (v3, i), (v4, i), (v1, i)])
    #     self.graph.tiers[0] = [v0]
    #     self.graph.tiers.append([v1, v2, v3, v4, v13, i])  # appending RHS to first level
    #     self.graph.graph = RHS
    #     self.graph.show()
        
    #     g = self.graph.P5(1)
    #     g.showLevel(0)
    #     g.showLevel(1)
    #     g.showLevel(2)
    #     g.show()
        
        
    # def test_p5_90(self):
    #     expected_tiers = ['[e vertex at (0, 0) and level 0]',
    #                       '[E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex at (-1, -1) and level 1, E vertex at (1, -1) and level 1, I vertex at (0.0, 0.0) and level 1]']

    #     expected_nodes = ['e vertex at (0, 0) and level 0',
    #                       'E vertex at (-1, 1) and level 1',
    #                       'E vertex at (1, 1) and level 1',
    #                       'E vertex at (-1, -1) and level 1',
    #                       'E vertex at (1, -1) and level 1',
    #                       'I vertex at (0.0, 0.0) and level 1']

    #     expected_edges = [('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
    #                       ('E vertex at (-1, 1) and level 1',
    #                        'E vertex at (-1, -1) and level 1'),
    #                       ('E vertex at (-1, 1) and level 1',
    #                        'I vertex at (0.0, 0.0) and level 1'),
    #                       ('E vertex at (1, 1) and level 1',
    #                        'E vertex at (1, -1) and level 1'),
    #                       ('E vertex at (1, 1) and level 1',
    #                        'I vertex at (0.0, 0.0) and level 1'),
    #                       ('E vertex at (-1, -1) and level 1',
    #                        'E vertex at (1, -1) and level 1'),
    #                       ('E vertex at (-1, -1) and level 1',
    #                        'I vertex at (0.0, 0.0) and level 1'),
    #                       ('E vertex at (1, -1) and level 1', 'I vertex at (0.0, 0.0) and level 1')]
        
    #     LHS = nx.Graph()

    #     LHS.add_node(v0 := Vertex(None, "E", 0))
    #     matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
    #     match = next(matches)
    #     assert match is not None, f"P5: No match for {v0} found!"
    #     RHS = nx.Graph()
    #     RHS.add_node(v0 := Vertex(list(match.keys())[0].position, "e", 0))
    #     RHS.add_node(v1 := Vertex(self.graph.corners[0], "E", 1))
    #     RHS.add_node(v2 := Vertex(self.graph.corners[1], "E", 1))
    #     RHS.add_node(v3 := Vertex(self.graph.corners[2], "E", 1))
    #     RHS.add_node(v12 := Vertex(((self.graph.corners[0][0] + self.graph.corners[1][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[1][1]) / 2), "E", 1))
    #     RHS.add_node(v4 := Vertex(self.graph.corners[3], "E", 1))
        

    #     RHS.add_node(i := Vertex(((self.graph.corners[0][0] + self.graph.corners[1][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2), "I", 1))
    #     RHS.add_edges_from([(v1, v12), (v12, v2), (v2, v4), (v4, v3), (v3, v1),
    #                         (v2, i), (v3, i), (v4, i), (v1, i)])
    #     self.graph.tiers[0] = [v0]
    #     self.graph.tiers.append([v1, v2, v3, v4, v12, i])  # appending RHS to first level
    #     self.graph.graph = RHS
    #     self.graph.show()
        
    #     g = self.graph.P5(1)
    #     g.showLevel(0)
    #     g.showLevel(1)
    #     g.showLevel(2)
    #     g.show()

    
    # def test_p5_after_vertex_has_been_added(self):
    #     expected_tiers = ['[e vertex at (0, 0) and level 0]',
    #                       '[E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex at (-1, -1) and level 1, E vertex at (1, -1) and level 1, I vertex at (0.0, 0.0) and level 1]']

    #     expected_nodes = ['e vertex at (0, 0) and level 0',
    #                       'E vertex at (-1, 1) and level 1',
    #                       'E vertex at (1, 1) and level 1',
    #                       'E vertex at (-1, -1) and level 1',
    #                       'E vertex at (1, -1) and level 1',
    #                       'I vertex at (0.0, 0.0) and level 1']

    #     expected_edges = [('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
    #                       ('E vertex at (-1, 1) and level 1',
    #                        'E vertex at (-1, -1) and level 1'),
    #                       ('E vertex at (-1, 1) and level 1',
    #                        'I vertex at (0.0, 0.0) and level 1'),
    #                       ('E vertex at (1, 1) and level 1',
    #                        'E vertex at (1, -1) and level 1'),
    #                       ('E vertex at (1, 1) and level 1',
    #                        'I vertex at (0.0, 0.0) and level 1'),
    #                       ('E vertex at (-1, -1) and level 1',
    #                        'E vertex at (1, -1) and level 1'),
    #                       ('E vertex at (-1, -1) and level 1',
    #                        'I vertex at (0.0, 0.0) and level 1'),
    #                       ('E vertex at (1, -1) and level 1', 'I vertex at (0.0, 0.0) and level 1')]
        
    #     LHS = nx.Graph()
    #     LHS.add_node(v0 := Vertex(None, "E", 0))
    #     matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
    #     match = next(matches)
    #     assert match is not None, f"P1: No match for {v0} found!"
    #     RHS = nx.Graph()
    #     RHS.add_node(v0 := Vertex(list(match.keys())[0].position, "e", 0))
    #     RHS.add_node(v1 := Vertex(self.graph.corners[0], "E", 1))
    #     RHS.add_node(v2 := Vertex(self.graph.corners[1], "E", 1))
    #     RHS.add_node(v3 := Vertex(self.graph.corners[2], "E", 1))
    #     RHS.add_node(v13 := Vertex(((self.graph.corners[0][0] + self.graph.corners[2][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2), "E", 1))
    #     RHS.add_node(v4 := Vertex(self.graph.corners[3], "E", 1))
    #     RHS.add_node(v14 := Vertex(((self.graph.corners[0][0] + self.graph.corners[2][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2 - 2), "E", 1))
        

    #     RHS.add_node(i := Vertex(((self.graph.corners[0][0] + self.graph.corners[1][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2), "I", 1))
    #     RHS.add_edges_from([(v1, v2), (v2, v4), (v4, v3), (v3, v13), (v13, v1), (v3, v14),
    #                         (v2, i), (v3, i), (v4, i), (v1, v14), (v14, v4), (v1, i)])
    #     self.graph.tiers[0] = [v0]
    #     self.graph.tiers.append([v1, v2, v3, v4, v13, i, v14])  # appending RHS to first level
    #     self.graph.graph = RHS
    #     self.graph.show()
        
    #     g = self.graph.P5(1)
    #     g.showLevel(0)
    #     g.showLevel(1)
    #     g.showLevel(2)
    #     g.show()
    
    
    # def test_p6(self):
    #     expected_tiers = ['[e vertex at (0, 0) and level 0]', 
    #                       '[E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex at (-1, -1) and level 1, E vertex at (1, -1) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (0.0, 1.0) and level 1, i vertex at (0.0, 0.0) and level 1]', 
    #                       '[E vertex at (-1, 1) and level 2, E vertex at (1, 1) and level 2, E vertex at (-1, -1) and level 2, E vertex at (1, -1) and level 2, E vertex at (0.0, 1.0) and level 2, E vertex at (-1.0, 0.0) and level 2, E vertex at (1.0, 0.0) and level 2, E vertex at (0.0, -1.0) and level 2, E vertex at (0.0, 0.0) and level 2, I vertex at (-0.5, 0.5) and level 2, I vertex at (0.5, 0.5) and level 2, I vertex at (-0.5, -0.5) and level 2, I vertex at (0.5, -0.5) and level 2]',
    #                       ]

    #     expected_nodes = ['e vertex at (0, 0) and level 0',
    #                     'E vertex at (-1, 1) and level 1',
    #                     'E vertex at (1, 1) and level 1',
    #                     'E vertex at (-1, -1) and level 1',
    #                     'E vertex at (1, -1) and level 1',
    #                     'I vertex at (0.0, 0.0) and level 1']

    #     expected_edges = [('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
    #                     ('E vertex at (-1, 1) and level 1',
    #                     'E vertex at (-1, -1) and level 1'),
    #                     ('E vertex at (-1, 1) and level 1',
    #                     'I vertex at (0.0, 0.0) and level 1'),
    #                     ('E vertex at (1, 1) and level 1',
    #                     'E vertex at (1, -1) and level 1'),
    #                     ('E vertex at (1, 1) and level 1',
    #                     'I vertex at (0.0, 0.0) and level 1'),
    #                     ('E vertex at (-1, -1) and level 1',
    #                     'E vertex at (1, -1) and level 1'),
    #                     ('E vertex at (-1, -1) and level 1',
    #                     'I vertex at (0.0, 0.0) and level 1'),
    #                     ('E vertex at (1, -1) and level 1', 'I vertex at (0.0, 0.0) and level 1')]
        
    #     LHS = nx.Graph()
    #     LHS.add_node(v0 := Vertex(None, "E", 0))
    #     matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
    #     match = next(matches)
    #     assert match is not None, f"P6: No match for {v0} found!"
    #     RHS = nx.Graph()
    #     RHS.add_node(v0 := Vertex(list(match.keys())[0].position, "e", 0))
    #     RHS.add_node(v1 := Vertex(self.graph.corners[0], "E", 1))
    #     RHS.add_node(v12 := Vertex(((self.graph.corners[0][0] + self.graph.corners[1][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[1][1]) / 2), "E", 1))
    #     RHS.add_node(v2 := Vertex(self.graph.corners[1], "E", 1))
    #     RHS.add_node(v3 := Vertex(self.graph.corners[2], "E", 1))
    #     RHS.add_node(v13 := Vertex(((self.graph.corners[0][0] + self.graph.corners[2][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2), "E", 1))
    #     RHS.add_node(v4 := Vertex(self.graph.corners[3], "E", 1))

        
        
        
    #     RHS.add_node(i := Vertex(((self.graph.corners[0][0] + self.graph.corners[1][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2), "I", 1))
    #     RHS.add_edges_from([(v1, v12), (v12, v2), (v2, v4), (v4, v3), (v3, v13), (v13, v1),
    #                         (v1, i), (v2, i), (v3, i), (v4, i)])
    #     self.graph.tiers[0] = [v0]
    #     self.graph.tiers.append([v1, v2, v3, v4, v12, v13, i])  # appending RHS to first level
    #     self.graph.graph = RHS
        
    #     g = self.graph.P6(1)
    #     g.showLevel(0)
    #     g.showLevel(1)
    #     g.showLevel(2)
    #     g.show()
        
        
    # def test_6_vertex_has_been_added(self):
    #     expected_tiers = ['[e vertex at (0, 0) and level 0]', 
    #                       '[E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex at (-1, -1) and level 1, E vertex at (1, -1) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (0.0, 1.0) and level 1, i vertex at (0.0, 0.0) and level 1]', 
    #                       '[E vertex at (-1, 1) and level 2, E vertex at (1, 1) and level 2, E vertex at (-1, -1) and level 2, E vertex at (1, -1) and level 2, E vertex at (0.0, 1.0) and level 2, E vertex at (-1.0, 0.0) and level 2, E vertex at (1.0, 0.0) and level 2, E vertex at (0.0, -1.0) and level 2, E vertex at (0.0, 0.0) and level 2, I vertex at (-0.5, 0.5) and level 2, I vertex at (0.5, 0.5) and level 2, I vertex at (-0.5, -0.5) and level 2, I vertex at (0.5, -0.5) and level 2]',
    #                       ]

    #     expected_nodes = ['e vertex at (0, 0) and level 0',
    #                     'E vertex at (-1, 1) and level 1',
    #                     'E vertex at (1, 1) and level 1',
    #                     'E vertex at (-1, -1) and level 1',
    #                     'E vertex at (1, -1) and level 1',
    #                     'I vertex at (0.0, 0.0) and level 1']

    #     expected_edges = [('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
    #                     ('E vertex at (-1, 1) and level 1',
    #                     'E vertex at (-1, -1) and level 1'),
    #                     ('E vertex at (-1, 1) and level 1',
    #                     'I vertex at (0.0, 0.0) and level 1'),
    #                     ('E vertex at (1, 1) and level 1',
    #                     'E vertex at (1, -1) and level 1'),
    #                     ('E vertex at (1, 1) and level 1',
    #                     'I vertex at (0.0, 0.0) and level 1'),
    #                     ('E vertex at (-1, -1) and level 1',
    #                     'E vertex at (1, -1) and level 1'),
    #                     ('E vertex at (-1, -1) and level 1',
    #                     'I vertex at (0.0, 0.0) and level 1'),
    #                     ('E vertex at (1, -1) and level 1', 'I vertex at (0.0, 0.0) and level 1')]
        
    #     LHS = nx.Graph()
    #     LHS.add_node(v0 := Vertex(None, "E", 0))
    #     matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
    #     match = next(matches)
    #     assert match is not None, f"P6: No match for {v0} found!"
    #     RHS = nx.Graph()
    #     RHS.add_node(v0 := Vertex(list(match.keys())[0].position, "e", 0))
    #     RHS.add_node(v1 := Vertex(self.graph.corners[0], "E", 1))
    #     RHS.add_node(v12 := Vertex(((self.graph.corners[0][0] + self.graph.corners[1][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[1][1]) / 2), "E", 1))
    #     RHS.add_node(v2 := Vertex(self.graph.corners[1], "E", 1))
    #     RHS.add_node(v3 := Vertex(self.graph.corners[2], "E", 1))
    #     RHS.add_node(v13 := Vertex(((self.graph.corners[0][0] + self.graph.corners[2][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2), "E", 1))
    #     RHS.add_node(v4 := Vertex(self.graph.corners[3], "E", 1))
    #     RHS.add_node(v14 := Vertex(((self.graph.corners[0][0] + self.graph.corners[2][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2 - 2), "E", 1))
    #     RHS.add_node(i := Vertex(((self.graph.corners[0][0] + self.graph.corners[1][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2), "I", 1))
    #     RHS.add_edges_from([(v1, v12), (v12, v2), (v2, v4), (v4, v3), (v3, v13), (v13, v1), (v1, v14), (v14, v4),
    #                         (v1, i), (v2, i), (v3, i), (v4, i)])
    #     self.graph.tiers[0] = [v0]
    #     self.graph.tiers.append([v1, v2, v3, v4, v12, v13, i, v14])  # appending RHS to first level
    #     self.graph.graph = RHS
        
    #     g = self.graph.P6(1)
    #     g.showLevel(0)
    #     g.showLevel(1)
    #     g.showLevel(2)
    #     g.show()
        
    def test_p6_to_p5(self):
        expected_tiers = ['[e vertex at (0, 0) and level 0]',
                          '[E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex at (-1, -1) and level 1, E vertex at (1, -1) and level 1, I vertex at (0.0, 0.0) and level 1]']

        expected_nodes = ['e vertex at (0, 0) and level 0',
                          'E vertex at (-1, 1) and level 1',
                          'E vertex at (1, 1) and level 1',
                          'E vertex at (-1, -1) and level 1',
                          'E vertex at (1, -1) and level 1',
                          'I vertex at (0.0, 0.0) and level 1']

        expected_edges = [('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
                          ('E vertex at (-1, 1) and level 1',
                           'E vertex at (-1, -1) and level 1'),
                          ('E vertex at (-1, 1) and level 1',
                           'I vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (1, 1) and level 1',
                           'E vertex at (1, -1) and level 1'),
                          ('E vertex at (1, 1) and level 1',
                           'I vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (-1, -1) and level 1',
                           'E vertex at (1, -1) and level 1'),
                          ('E vertex at (-1, -1) and level 1',
                           'I vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (1, -1) and level 1', 'I vertex at (0.0, 0.0) and level 1')]
        
        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))
        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"
        RHS = nx.Graph()
        RHS.add_node(v0 := Vertex(list(match.keys())[0].position, "e", 0))
        RHS.add_node(v1 := Vertex(self.graph.corners[0], "E", 1))
        RHS.add_node(v2 := Vertex(self.graph.corners[1], "E", 1))
        RHS.add_node(v3 := Vertex(self.graph.corners[2], "E", 1))
        RHS.add_node(v13 := Vertex(((self.graph.corners[0][0] + self.graph.corners[2][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2), "E", 1))
        RHS.add_node(v4 := Vertex(self.graph.corners[3], "E", 1))
        

        RHS.add_node(i := Vertex(((self.graph.corners[0][0] + self.graph.corners[1][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2), "I", 1))
        RHS.add_edges_from([(v1, v2), (v2, v4), (v4, v3), (v3, v13), (v13, v1),
                            (v2, i), (v3, i), (v4, i), (v1, i)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append([v1, v2, v3, v4, v13, i])  # appending RHS to first level
        self.graph.graph = RHS
        self.graph.show()
        
        g = self.graph.P6(1)
        g.showLevel(0)
        g.showLevel(1)
        g.showLevel(2)
        g.show()
        
        
        
    def test_p5_to_p6(self):
        expected_tiers = ['[e vertex at (0, 0) and level 0]', 
                            '[E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex at (-1, -1) and level 1, E vertex at (1, -1) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (0.0, 1.0) and level 1, i vertex at (0.0, 0.0) and level 1]', 
                            '[E vertex at (-1, 1) and level 2, E vertex at (1, 1) and level 2, E vertex at (-1, -1) and level 2, E vertex at (1, -1) and level 2, E vertex at (0.0, 1.0) and level 2, E vertex at (-1.0, 0.0) and level 2, E vertex at (1.0, 0.0) and level 2, E vertex at (0.0, -1.0) and level 2, E vertex at (0.0, 0.0) and level 2, I vertex at (-0.5, 0.5) and level 2, I vertex at (0.5, 0.5) and level 2, I vertex at (-0.5, -0.5) and level 2, I vertex at (0.5, -0.5) and level 2]',
                            ]

        expected_nodes = ['e vertex at (0, 0) and level 0',
                        'E vertex at (-1, 1) and level 1',
                        'E vertex at (1, 1) and level 1',
                        'E vertex at (-1, -1) and level 1',
                        'E vertex at (1, -1) and level 1',
                        'I vertex at (0.0, 0.0) and level 1']

        expected_edges = [('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
                        ('E vertex at (-1, 1) and level 1',
                        'E vertex at (-1, -1) and level 1'),
                        ('E vertex at (-1, 1) and level 1',
                        'I vertex at (0.0, 0.0) and level 1'),
                        ('E vertex at (1, 1) and level 1',
                        'E vertex at (1, -1) and level 1'),
                        ('E vertex at (1, 1) and level 1',
                        'I vertex at (0.0, 0.0) and level 1'),
                        ('E vertex at (-1, -1) and level 1',
                        'E vertex at (1, -1) and level 1'),
                        ('E vertex at (-1, -1) and level 1',
                        'I vertex at (0.0, 0.0) and level 1'),
                        ('E vertex at (1, -1) and level 1', 'I vertex at (0.0, 0.0) and level 1')]
        
        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))
        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P6: No match for {v0} found!"
        RHS = nx.Graph()
        RHS.add_node(v0 := Vertex(list(match.keys())[0].position, "e", 0))
        RHS.add_node(v1 := Vertex(self.graph.corners[0], "E", 1))
        RHS.add_node(v12 := Vertex(((self.graph.corners[0][0] + self.graph.corners[1][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[1][1]) / 2), "E", 1))
        RHS.add_node(v2 := Vertex(self.graph.corners[1], "E", 1))
        RHS.add_node(v3 := Vertex(self.graph.corners[2], "E", 1))
        RHS.add_node(v13 := Vertex(((self.graph.corners[0][0] + self.graph.corners[2][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2), "E", 1))
        RHS.add_node(v4 := Vertex(self.graph.corners[3], "E", 1))

        
        
        
        RHS.add_node(i := Vertex(((self.graph.corners[0][0] + self.graph.corners[1][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2), "I", 1))
        RHS.add_edges_from([(v1, v12), (v12, v2), (v2, v4), (v4, v3), (v3, v13), (v13, v1),
                            (v1, i), (v2, i), (v3, i), (v4, i)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append([v1, v2, v3, v4, v12, v13, i])  # appending RHS to first level
        self.graph.graph = RHS
        
        g = self.graph.P5(1)
        g.showLevel(0)
        g.showLevel(1)
        g.showLevel(2)
        g.show()
        
    
    
    # def test_6_90(self):
    #     expected_tiers = ['[e vertex at (0, 0) and level 0]', 
    #                       '[E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex at (-1, -1) and level 1, E vertex at (1, -1) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (0.0, 1.0) and level 1, i vertex at (0.0, 0.0) and level 1]', 
    #                       '[E vertex at (-1, 1) and level 2, E vertex at (1, 1) and level 2, E vertex at (-1, -1) and level 2, E vertex at (1, -1) and level 2, E vertex at (0.0, 1.0) and level 2, E vertex at (-1.0, 0.0) and level 2, E vertex at (1.0, 0.0) and level 2, E vertex at (0.0, -1.0) and level 2, E vertex at (0.0, 0.0) and level 2, I vertex at (-0.5, 0.5) and level 2, I vertex at (0.5, 0.5) and level 2, I vertex at (-0.5, -0.5) and level 2, I vertex at (0.5, -0.5) and level 2]',
    #                       ]

    #     expected_nodes = ['e vertex at (0, 0) and level 0',
    #                     'E vertex at (-1, 1) and level 1',
    #                     'E vertex at (1, 1) and level 1',
    #                     'E vertex at (-1, -1) and level 1',
    #                     'E vertex at (1, -1) and level 1',
    #                     'I vertex at (0.0, 0.0) and level 1']

    #     expected_edges = [('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
    #                     ('E vertex at (-1, 1) and level 1',
    #                     'E vertex at (-1, -1) and level 1'),
    #                     ('E vertex at (-1, 1) and level 1',
    #                     'I vertex at (0.0, 0.0) and level 1'),
    #                     ('E vertex at (1, 1) and level 1',
    #                     'E vertex at (1, -1) and level 1'),
    #                     ('E vertex at (1, 1) and level 1',
    #                     'I vertex at (0.0, 0.0) and level 1'),
    #                     ('E vertex at (-1, -1) and level 1',
    #                     'E vertex at (1, -1) and level 1'),
    #                     ('E vertex at (-1, -1) and level 1',
    #                     'I vertex at (0.0, 0.0) and level 1'),
    #                     ('E vertex at (1, -1) and level 1', 'I vertex at (0.0, 0.0) and level 1')]
        
    #     LHS = nx.Graph()
    #     LHS.add_node(v0 := Vertex(None, "E", 0))
    #     matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
    #     match = next(matches)
    #     assert match is not None, f"P6: No match for {v0} found!"
    #     RHS = nx.Graph()
    #     RHS.add_node(v0 := Vertex(list(match.keys())[0].position, "e", 0))
    #     RHS.add_node(v1 := Vertex(self.graph.corners[0], "E", 1))
    #     RHS.add_node(v12 := Vertex(((self.graph.corners[0][0] + self.graph.corners[1][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[1][1]) / 2), "E", 1))
    #     RHS.add_node(v2 := Vertex(self.graph.corners[1], "E", 1))
    #     RHS.add_node(v3 := Vertex(self.graph.corners[2], "E", 1))
    #     RHS.add_node(v24 := Vertex(((self.graph.corners[1][0] + self.graph.corners[3][0]) / 2, (self.graph.corners[1][1] + self.graph.corners[3][1]) / 2), "E", 1))
    #     RHS.add_node(v4 := Vertex(self.graph.corners[3], "E", 1))

    #     RHS.add_node(i := Vertex(((self.graph.corners[0][0] + self.graph.corners[1][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2), "I", 1))
    #     RHS.add_edges_from([(v1, v12), (v12, v2), (v4, v3), (v1, v3), (v4, v24), (v24, v2),
    #                         (v1, i), (v2, i), (v3, i), (v4, i)])
    #     self.graph.tiers[0] = [v0]
    #     self.graph.tiers.append([v1, v2, v3, v4, v12, v24, i])  # appending RHS to first level
    #     self.graph.graph = RHS
        
    #     g = self.graph.P6(1)
    #     g.showLevel(0)
    #     g.showLevel(1)
    #     g.showLevel(2)
        
        
    # def test_6_without_edge(self):
    
    #     expected_tiers = ['[e vertex at (0, 0) and level 0]', 
    #                       '[E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex at (-1, -1) and level 1, E vertex at (1, -1) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (0.0, 1.0) and level 1, i vertex at (0.0, 0.0) and level 1]', 
    #                       '[E vertex at (-1, 1) and level 2, E vertex at (1, 1) and level 2, E vertex at (-1, -1) and level 2, E vertex at (1, -1) and level 2, E vertex at (0.0, 1.0) and level 2, E vertex at (-1.0, 0.0) and level 2, E vertex at (1.0, 0.0) and level 2, E vertex at (0.0, -1.0) and level 2, E vertex at (0.0, 0.0) and level 2, I vertex at (-0.5, 0.5) and level 2, I vertex at (0.5, 0.5) and level 2, I vertex at (-0.5, -0.5) and level 2, I vertex at (0.5, -0.5) and level 2]',
    #                       ]

    #     expected_nodes = ['e vertex at (0, 0) and level 0',
    #                     'E vertex at (-1, 1) and level 1',
    #                     'E vertex at (1, 1) and level 1',
    #                     'E vertex at (-1, -1) and level 1',
    #                     'E vertex at (1, -1) and level 1',
    #                     'I vertex at (0.0, 0.0) and level 1']

    #     expected_edges = [('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
    #                     ('E vertex at (-1, 1) and level 1',
    #                     'E vertex at (-1, -1) and level 1'),
    #                     ('E vertex at (-1, 1) and level 1',
    #                     'I vertex at (0.0, 0.0) and level 1'),
    #                     ('E vertex at (1, 1) and level 1',
    #                     'E vertex at (1, -1) and level 1'),
    #                     ('E vertex at (1, 1) and level 1',
    #                     'I vertex at (0.0, 0.0) and level 1'),
    #                     ('E vertex at (-1, -1) and level 1',
    #                     'E vertex at (1, -1) and level 1'),
    #                     ('E vertex at (-1, -1) and level 1',
    #                     'I vertex at (0.0, 0.0) and level 1'),
    #                     ('E vertex at (1, -1) and level 1', 'I vertex at (0.0, 0.0) and level 1')]
        
    #     LHS = nx.Graph()
    #     LHS.add_node(v0 := Vertex(None, "E", 0))
    #     matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
    #     match = next(matches)
    #     assert match is not None, f"P1: No match for {v0} found!"
    #     RHS = nx.Graph()
    #     RHS.add_node(v0 := Vertex(list(match.keys())[0].position, "e", 0))
    #     RHS.add_node(v1 := Vertex(self.graph.corners[0], "E", 1))
    #     RHS.add_node(v12 := Vertex(((self.graph.corners[0][0] + self.graph.corners[1][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[1][1]) / 2), "E", 1))
    #     RHS.add_node(v2 := Vertex(self.graph.corners[1], "E", 1))
    #     RHS.add_node(v3 := Vertex(self.graph.corners[2], "E", 1))
    #     # RHS.add_node(v13 := Vertex(((self.graph.corners[0][0] + self.graph.corners[2][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2), "E", 1))
    #     RHS.add_node(v4 := Vertex(self.graph.corners[3], "E", 1))

    #     RHS.add_node(i := Vertex(((self.graph.corners[0][0] + self.graph.corners[1][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2), "I", 1))
    #     RHS.add_edges_from([(v1, v12), (v12, v2), (v2, v4), (v4, v3), #(v3, v13), (v13, v1),
    #                         (v1, i), (v2, i), (v3, i), (v4, i)])
    #     self.graph.tiers[0] = [v0]
    #     self.graph.tiers.append([v1, v2, v3, v4, v12, i])  # appending RHS to first level
    #     self.graph.graph = RHS
        
    #     g = self.graph.P5(1)
    #     g.showLevel(0)
    #     g.showLevel(1)
    #     g.showLevel(2)

if __name__ == '__main__':
    unittest.main()

    # TODO:
    #  - ogarnąć znajdowanie grafów izomorficznych - żeby się dało wybrać, na którym poziomie i w którym miejscu wykonujemy produkcję
    #  - ogarnąc łamania w pionie i poziomie w P2
    #  - test do P1 P2 P2 P2
    #  - lepsze testy: z grafami, do których nie da się podgrafów dodać, ogólnie dla większego grafu ma działać, zmienić etykietę jednego wierzchołka, brak jakiejś krawędzi
    #  - czy __eq__ jest ok??
