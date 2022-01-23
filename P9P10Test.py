import unittest

from visualization import TieredGraph, Vertex, GraphMatcherByLabel
import networkx as nx


class P9P10Test(unittest.TestCase):
    def setUp(self):
        v1 = (-1, 1)
        v2 = (1, 1)
        v3 = (-1, -1)
        v4 = (1, -1)
        self.graph = TieredGraph((v1, v2, v3, v4))

    def validate_tiers(self, graph, expectedTiers):
        self.assertEqual(expectedTiers, list(map(lambda vertex: vertex.__repr__(), graph.tiers)))

    def validate_graph(self, expected_nodes, expected_edges):
        self.validate_nodes(expected_nodes)
        self.validate_edges(expected_edges)

    def validate_nodes(self, expected_nodes):
        self.assertEqual(expected_nodes, [node.__repr__() for node in dict(self.graph.graph.nodes).keys()])

    def validate_edges(self, expected_edges):
        self.assertEqual(expected_edges,
                         [(pair[0].__repr__(), pair[1].__repr__()) for pair in list(self.graph.graph.edges)])

    def test_p9_pass_3(self):
        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))

        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        RHS = nx.Graph()

        RHS.add_node(v0 := Vertex((0, 1), "E", 1))
        RHS.add_node(v1 := Vertex((0, 0.5), "E", 1))
        RHS.add_node(v1_1 := Vertex((0, 0.5), "E", 1))
        RHS.add_node(v2 := Vertex((0, 0.0), "E", 1))
        RHS.add_node(v2_2 := Vertex((0, 0.0), "E", 1))
        RHS.add_node(v3 := Vertex((0, -0.5), "E", 1))
        RHS.add_node(v3_3 := Vertex((0, -0.5), "E", 1))
        RHS.add_node(I_1 := Vertex((-1, 0.25), "I", 1))
        RHS.add_node(I_2 := Vertex((-1, -0.25), "I", 1))
        RHS.add_node(I_3 := Vertex((1, 0.25), "I", 1))
        RHS.add_node(I_4 := Vertex((1, -0.25), "I", 1))

        RHS.add_node(I_0_1 := Vertex((-0.75, 0.75), "I", 1))
        RHS.add_node(I_0_2 := Vertex((0.75, 0.75), "I", 1))

        RHS.add_edges_from(
            [(I_0_1, I_1), (I_0_1, I_2), (I_0_2, I_3), (I_0_2, I_4), (v0, I_0_1), (v0, I_0_2), (I_1, v1), (I_1, v2),
             (I_2, v2), (I_2, v3), (I_3, v1_1), (I_3, v2_2), (I_4, v2_2), (I_4, v3_3), (v1, v2),
             (v2, v3), (v1_1, v2_2), (v2_2, v3_3)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append(
            [v0, v1, v1_1, v2, v2_2, v3, v3_3, I_0_1, I_1, I_0_2, I_2, I_3, I_4])  # appending RHS to first level

        self.graph.graph = RHS
        expected_tiers = ['[E vertex at (0, 1) and level 1]',
                          '[E vertex at (0, 1) and level 1, E vertex at (-0.5, 0.5) and level 1, E '
                          'vertex at (0.5, 0.5) and level 1, E vertex at (-0.5, 0.0) and level 1, E '
                          'vertex at (0.5, 0.0) and level 1, E vertex at (-0.5, -0.5) and level 1, E '
                          'vertex at (0.5, -0.5) and level 1, I vertex at (-0.75, 0.75) and level 1, I '
                          'vertex at (-1, 0.25) and level 1, I vertex at (0.75, 0.75) and level 1, I '
                          'vertex at (-1, -0.25) and level 1, I vertex at (1, 0.25) and level 1, I '
                          'vertex at (1, -0.25) and level 1]',
                          '[E vertex at (0, 1) and level 2, E vertex at (-0.5, 0.5) and level 2, E '
                          'vertex at (-0.5, 0.0) and level 2, E vertex at (-0.5, -0.5) and level 2, E '
                          'vertex at (-0.5, -0.5) and level 2, I vertex at (-1, 0.25) and level 2, I '
                          'vertex at (-1, -0.25) and level 2, I vertex at (1, 0.25) and level 2, I '
                          'vertex at (1, -0.25) and level 2, I vertex at (-0.75, 0.75) and level 2, I '
                          'vertex at (0.75, 0.75) and level 2]']

        expected_nodes = ['E vertex at (0, 1) and level 1',
                          'E vertex at (-0.5, 0.5) and level 1',
                          'E vertex at (-0.5, 0.0) and level 1',
                          'E vertex at (-0.5, -0.5) and level 1',
                          'I vertex at (-1, 0.25) and level 1',
                          'I vertex at (-1, -0.25) and level 1',
                          'I vertex at (1, 0.25) and level 1',
                          'I vertex at (1, -0.25) and level 1',
                          'I vertex at (-0.75, 0.75) and level 1',
                          'I vertex at (0.75, 0.75) and level 1',
                          'E vertex at (-0.5, 0.5) and level 2',
                          'I vertex at (-1, 0.25) and level 2',
                          'I vertex at (1, 0.25) and level 2',
                          'E vertex at (-0.5, 0.0) and level 2',
                          'I vertex at (-1, -0.25) and level 2',
                          'I vertex at (1, -0.25) and level 2',
                          'E vertex at (-0.5, -0.5) and level 2',
                          'E vertex at (0, 1) and level 2',
                          'I vertex at (-0.75, 0.75) and level 2',
                          'I vertex at (0.75, 0.75) and level 2']

        expected_edges = [('E vertex at (0, 1) and level 1', 'I vertex at (-0.75, 0.75) and level 1'),
                          ('E vertex at (0, 1) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (-0.5, 0.5) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (-0.5, 0.5) and level 1', 'E vertex at (-0.5, 0.0) and level 1'),
                          ('E vertex at (-0.5, 0.0) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (-0.5, 0.0) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('E vertex at (-0.5, 0.0) and level 1',
                           'E vertex at (-0.5, -0.5) and level 1'),
                          ('E vertex at (-0.5, -0.5) and level 1',
                           'I vertex at (-1, -0.25) and level 1'),
                          ('I vertex at (-1, 0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (-1, -0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (1, 0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('I vertex at (1, -0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (-0.5, 0.5) and level 2', 'I vertex at (-1, 0.25) and level 2'),
                          ('E vertex at (-0.5, 0.5) and level 2', 'I vertex at (1, 0.25) and level 2'),
                          ('E vertex at (-0.5, 0.5) and level 2', 'E vertex at (-0.5, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2', 'E vertex at (-0.5, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'E vertex at (-0.5, 0.0) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (-0.5, 0.0) and level 2', 'I vertex at (-1, -0.25) and level 2'),
                          ('E vertex at (-0.5, 0.0) and level 2', 'I vertex at (1, -0.25) and level 2'),
                          ('E vertex at (-0.5, 0.0) and level 2',
                           'E vertex at (-0.5, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2',
                           'E vertex at (-0.5, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'E vertex at (-0.5, -0.5) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (-0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (0.75, 0.75) and level 2')]
        g = self.graph
        g.showLevel(1)
        g = g.P9(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p9_failed_separated(self):
        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))

        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        RHS = nx.Graph()

        RHS.add_node(v0 := Vertex((0, 1), "E", 1))
        RHS.add_node(v1 := Vertex((-0.5, 0.5), "E", 1))
        RHS.add_node(v1_1 := Vertex((0.5, 0.5), "E", 1))
        RHS.add_node(v2 := Vertex((-0.5, 0.0), "E", 1))
        RHS.add_node(v2_2 := Vertex((0.5, 0.0), "E", 1))
        RHS.add_node(v3 := Vertex((-0.5, -0.5), "E", 1))
        RHS.add_node(v3_3 := Vertex((0.5, -0.5), "E", 1))
        RHS.add_node(I_1 := Vertex((-1, 0.25), "I", 1))
        RHS.add_node(I_2 := Vertex((-1, -0.25), "I", 1))
        RHS.add_node(I_3 := Vertex((1, 0.25), "I", 1))
        RHS.add_node(I_4 := Vertex((1, -0.25), "I", 1))

        RHS.add_node(I_0_1 := Vertex((-0.75, 0.75), "I", 1))
        RHS.add_node(I_0_2 := Vertex((0.75, 0.75), "I", 1))

        RHS.add_edges_from(
            [(I_0_1, I_1), (I_0_1, I_2), (I_0_2, I_3), (I_0_2, I_4), (v0, I_0_1), (v0, I_0_2), (I_1, v1), (I_1, v2),
             (I_2, v2), (I_2, v3), (I_3, v1_1), (I_3, v2_2), (I_4, v2_2), (I_4, v3_3), (v1, v2),
             (v2, v3), (v1_1, v2_2), (v2_2, v3_3)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append(
            [v0, v1, v1_1, v2, v2_2, v3, v3_3, I_0_1, I_1, I_0_2, I_2, I_3, I_4])  # appending RHS to first level

        self.graph.graph = RHS
        expected_tiers = ['[E vertex at (0, 1) and level 1]',
                          '[E vertex at (0, 1) and level 1, E vertex at (-0.5, 0.5) and level 1, E '
                          'vertex at (0.5, 0.5) and level 1, E vertex at (-0.5, 0.0) and level 1, E '
                          'vertex at (0.5, 0.0) and level 1, E vertex at (-0.5, -0.5) and level 1, E '
                          'vertex at (0.5, -0.5) and level 1, I vertex at (-0.75, 0.75) and level 1, I '
                          'vertex at (-1, 0.25) and level 1, I vertex at (0.75, 0.75) and level 1, I '
                          'vertex at (-1, -0.25) and level 1, I vertex at (1, 0.25) and level 1, I '
                          'vertex at (1, -0.25) and level 1]',
                          '[E vertex at (0, 1) and level 2, E vertex at (-0.5, 0.5) and level 2, E '
                          'vertex at (-0.5, 0.0) and level 2, E vertex at (-0.5, -0.5) and level 2, E '
                          'vertex at (-0.5, -0.5) and level 2, I vertex at (-1, 0.25) and level 2, I '
                          'vertex at (-1, -0.25) and level 2, I vertex at (1, 0.25) and level 2, I '
                          'vertex at (1, -0.25) and level 2, I vertex at (-0.75, 0.75) and level 2, I '
                          'vertex at (0.75, 0.75) and level 2]']

        expected_nodes = ['E vertex at (0, 1) and level 1',
                          'E vertex at (-0.5, 0.5) and level 1',
                          'E vertex at (-0.5, 0.0) and level 1',
                          'E vertex at (-0.5, -0.5) and level 1',
                          'I vertex at (-1, 0.25) and level 1',
                          'I vertex at (-1, -0.25) and level 1',
                          'I vertex at (1, 0.25) and level 1',
                          'I vertex at (1, -0.25) and level 1',
                          'I vertex at (-0.75, 0.75) and level 1',
                          'I vertex at (0.75, 0.75) and level 1',
                          'E vertex at (-0.5, 0.5) and level 2',
                          'I vertex at (-1, 0.25) and level 2',
                          'I vertex at (1, 0.25) and level 2',
                          'E vertex at (-0.5, 0.0) and level 2',
                          'I vertex at (-1, -0.25) and level 2',
                          'I vertex at (1, -0.25) and level 2',
                          'E vertex at (-0.5, -0.5) and level 2',
                          'E vertex at (0, 1) and level 2',
                          'I vertex at (-0.75, 0.75) and level 2',
                          'I vertex at (0.75, 0.75) and level 2']

        expected_edges = [('E vertex at (0, 1) and level 1', 'I vertex at (-0.75, 0.75) and level 1'),
                          ('E vertex at (0, 1) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (-0.5, 0.5) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (-0.5, 0.5) and level 1', 'E vertex at (-0.5, 0.0) and level 1'),
                          ('E vertex at (-0.5, 0.0) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (-0.5, 0.0) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('E vertex at (-0.5, 0.0) and level 1',
                           'E vertex at (-0.5, -0.5) and level 1'),
                          ('E vertex at (-0.5, -0.5) and level 1',
                           'I vertex at (-1, -0.25) and level 1'),
                          ('I vertex at (-1, 0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (-1, -0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (1, 0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('I vertex at (1, -0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (-0.5, 0.5) and level 2', 'I vertex at (-1, 0.25) and level 2'),
                          ('E vertex at (-0.5, 0.5) and level 2', 'I vertex at (1, 0.25) and level 2'),
                          ('E vertex at (-0.5, 0.5) and level 2', 'E vertex at (-0.5, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2', 'E vertex at (-0.5, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'E vertex at (-0.5, 0.0) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (-0.5, 0.0) and level 2', 'I vertex at (-1, -0.25) and level 2'),
                          ('E vertex at (-0.5, 0.0) and level 2', 'I vertex at (1, -0.25) and level 2'),
                          ('E vertex at (-0.5, 0.0) and level 2',
                           'E vertex at (-0.5, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2',
                           'E vertex at (-0.5, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'E vertex at (-0.5, -0.5) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (-0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (0.75, 0.75) and level 2')]
        g = self.graph
        g.showLevel(1)
        g = g.P9(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p9_pass_additional(self):
        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))

        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        RHS = nx.Graph()

        RHS.add_node(v0 := Vertex((0, 1), "E", 1))
        RHS.add_node(v1 := Vertex((0, 0.5), "E", 1))
        RHS.add_node(v1_1 := Vertex((0, 0.5), "E", 1))
        RHS.add_node(v2 := Vertex((0, 0.0), "E", 1))
        RHS.add_node(v2_2 := Vertex((0, 0.0), "E", 1))
        RHS.add_node(v3 := Vertex((0, -0.5), "E", 1))
        RHS.add_node(v3_3 := Vertex((0, -0.5), "E", 1))
        RHS.add_node(I_1 := Vertex((-1, 0.25), "I", 1))
        RHS.add_node(I_2 := Vertex((-1, -0.25), "I", 1))
        RHS.add_node(I_3 := Vertex((1, 0.25), "I", 1))
        RHS.add_node(I_4 := Vertex((1, -0.25), "I", 1))

        RHS.add_node(additional_1 := Vertex((1, -1), "I", 1))
        RHS.add_node(additional_2 := Vertex((1, 1), "I", 1))
        RHS.add_node(additional_3 := Vertex((-1, 1), "I", 1))

        RHS.add_node(I_0_1 := Vertex((-0.75, 0.75), "I", 1))
        RHS.add_node(I_0_2 := Vertex((0.75, 0.75), "I", 1))

        RHS.add_edges_from(
            [(I_0_1, I_1), (I_0_1, I_2), (I_0_2, I_3), (I_0_2, I_4), (v0, I_0_1), (v0, I_0_2), (I_1, v1), (I_1, v2),
             (I_2, v2), (I_2, v3), (I_3, v1_1), (I_3, v2_2), (I_4, v2_2), (I_4, v3_3), (v1, v2),
             (v2, v3), (v1_1, v2_2), (v2_2, v3_3), (additional_1, I_0_1), (additional_2, I_0_1), (additional_3, I_0_1)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append(
            [v0, v1, v1_1, v2, v2_2, v3, v3_3, I_0_1, I_1, I_0_2, I_2, I_3, I_4, additional_1, additional_2,
             additional_3])  # appending RHS to first level

        self.graph.graph = RHS
        expected_tiers = ['[E vertex at (0, 1) and level 1]',
                          '[E vertex at (0, 1) and level 1, E vertex at (0, 0.5) and level 1, E vertex '
                          'at (0, 0.5) and level 1, E vertex at (0, 0.0) and level 1, E vertex at (0, '
                          '0.0) and level 1, E vertex at (0, -0.5) and level 1, E vertex at (0, -0.5) '
                          'and level 1, I vertex at (-0.75, 0.75) and level 1, I vertex at (-1, 0.25) '
                          'and level 1, I vertex at (0.75, 0.75) and level 1, I vertex at (-1, -0.25) '
                          'and level 1, I vertex at (1, 0.25) and level 1, I vertex at (1, -0.25) and '
                          'level 1, I vertex at (1, -1) and level 1, I vertex at (1, 1) and level 1, I '
                          'vertex at (-1, 1) and level 1]',
                          '[E vertex at (0, 1) and level 2, E vertex at (0, 0.5) and level 2, E vertex '
                          'at (0, 0.0) and level 2, E vertex at (0, -0.5) and level 2, E vertex at (0, '
                          '-0.5) and level 2, I vertex at (-1, 0.25) and level 2, I vertex at (-1, '
                          '-0.25) and level 2, I vertex at (1, 0.25) and level 2, I vertex at (1, '
                          '-0.25) and level 2, I vertex at (-0.75, 0.75) and level 2, I vertex at '
                          '(0.75, 0.75) and level 2]']

        expected_nodes = ['E vertex at (0, 1) and level 1',
                          'E vertex at (0, 0.5) and level 1',
                          'E vertex at (0, 0.0) and level 1',
                          'E vertex at (0, -0.5) and level 1',
                          'I vertex at (-1, 0.25) and level 1',
                          'I vertex at (-1, -0.25) and level 1',
                          'I vertex at (1, 0.25) and level 1',
                          'I vertex at (1, -0.25) and level 1',
                          'I vertex at (1, -1) and level 1',
                          'I vertex at (1, 1) and level 1',
                          'I vertex at (-1, 1) and level 1',
                          'I vertex at (-0.75, 0.75) and level 1',
                          'I vertex at (0.75, 0.75) and level 1',
                          'E vertex at (0, 0.5) and level 2',
                          'I vertex at (-1, 0.25) and level 2',
                          'I vertex at (1, 0.25) and level 2',
                          'E vertex at (0, 0.0) and level 2',
                          'I vertex at (-1, -0.25) and level 2',
                          'I vertex at (1, -0.25) and level 2',
                          'E vertex at (0, -0.5) and level 2',
                          'E vertex at (0, 1) and level 2',
                          'I vertex at (-0.75, 0.75) and level 2',
                          'I vertex at (0.75, 0.75) and level 2']

        expected_edges = [('E vertex at (0, 1) and level 1', 'I vertex at (-0.75, 0.75) and level 1'),
                          ('E vertex at (0, 1) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (0, 0.5) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (0, 0.5) and level 1', 'E vertex at (0, 0.0) and level 1'),
                          ('E vertex at (0, 0.0) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (0, 0.0) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('E vertex at (0, 0.0) and level 1', 'E vertex at (0, -0.5) and level 1'),
                          ('E vertex at (0, -0.5) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('I vertex at (-1, 0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (-1, -0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (1, 0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('I vertex at (1, -0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('I vertex at (1, -1) and level 1', 'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (1, 1) and level 1', 'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (-1, 1) and level 1', 'I vertex at (-0.75, 0.75) and level 1'),
                          ('E vertex at (0, 0.5) and level 2', 'I vertex at (-1, 0.25) and level 2'),
                          ('E vertex at (0, 0.5) and level 2', 'I vertex at (1, 0.25) and level 2'),
                          ('E vertex at (0, 0.5) and level 2', 'E vertex at (0, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2', 'E vertex at (0, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'E vertex at (0, 0.0) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0, 0.0) and level 2', 'I vertex at (-1, -0.25) and level 2'),
                          ('E vertex at (0, 0.0) and level 2', 'I vertex at (1, -0.25) and level 2'),
                          ('E vertex at (0, 0.0) and level 2', 'E vertex at (0, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2', 'E vertex at (0, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'E vertex at (0, -0.5) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (-0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (0.75, 0.75) and level 2')]
        g = self.graph
        g.showLevel(1)
        g = g.P9(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p9_failed_remove_edge2(self):
        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))

        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        RHS = nx.Graph()

        RHS.add_node(v0 := Vertex((0, 1), "E", 1))
        RHS.add_node(v1 := Vertex((0, 0.5), "E", 1))
        RHS.add_node(v1_1 := Vertex((0, 0.5), "E", 1))
        RHS.add_node(v2 := Vertex((0, 0.0), "E", 1))
        RHS.add_node(v2_2 := Vertex((0, 0.0), "E", 1))
        RHS.add_node(v3 := Vertex((0, -0.5), "E", 1))
        RHS.add_node(v3_3 := Vertex((0, -0.5), "E", 1))
        RHS.add_node(I_1 := Vertex((-1, 0.25), "I", 1))
        RHS.add_node(I_2 := Vertex((-1, -0.25), "I", 1))
        RHS.add_node(I_3 := Vertex((1, 0.25), "I", 1))
        RHS.add_node(I_4 := Vertex((1, -0.25), "I", 1))

        RHS.add_node(I_0_1 := Vertex((-0.75, 0.75), "I", 1))
        RHS.add_node(I_0_2 := Vertex((0.75, 0.75), "I", 1))

        RHS.add_edges_from(
            [(I_0_1, I_1), (I_0_1, I_2), (I_0_2, I_3), (I_0_2, I_4), (v0, I_0_1), (v0, I_0_2), (I_1, v1), (I_1, v2),
             (I_2, v2), (I_3, v1_1), (I_3, v2_2), (I_4, v2_2), (I_4, v3_3), (v1, v2),
             (v2, v3), (v1_1, v2_2), (v2_2, v3_3)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append(
            [v0, v1, v1_1, v2, v2_2, v3, v3_3, I_0_1, I_1, I_0_2, I_2, I_3, I_4])  # appending RHS to first level

        self.graph.graph = RHS
        self.graph.show()
        expected_tiers = ['[E vertex at (0, 1) and level 1]',
                          '[E vertex at (0, 1) and level 1, E vertex at (0, 0.5) and level 1, E vertex '
                          'at (0, 0.5) and level 1, E vertex at (0, 0.0) and level 1, E vertex at (0, '
                          '0.0) and level 1, E vertex at (0, -0.5) and level 1, E vertex at (0, -0.5) '
                          'and level 1, I vertex at (-0.75, 0.75) and level 1, I vertex at (-1, 0.25) '
                          'and level 1, I vertex at (0.75, 0.75) and level 1, I vertex at (-1, -0.25) '
                          'and level 1, I vertex at (1, 0.25) and level 1, I vertex at (1, -0.25) and '
                          'level 1]',
                          '[E vertex at (0, 1) and level 2, E vertex at (0, 0.5) and level 2, E vertex '
                          'at (0, 0.0) and level 2, E vertex at (0, -0.5) and level 2, E vertex at (0, '
                          '-0.5) and level 2, I vertex at (-1, 0.25) and level 2, I vertex at (-1, '
                          '-0.25) and level 2, I vertex at (1, 0.25) and level 2, I vertex at (1, '
                          '-0.25) and level 2, I vertex at (-0.75, 0.75) and level 2, I vertex at '
                          '(0.75, 0.75) and level 2]']

        expected_nodes = ['E vertex at (0, 1) and level 1',
                          'E vertex at (0, 0.5) and level 1',
                          'E vertex at (0, 0.0) and level 1',
                          'E vertex at (0, -0.5) and level 1',
                          'I vertex at (-1, 0.25) and level 1',
                          'I vertex at (-1, -0.25) and level 1',
                          'I vertex at (1, 0.25) and level 1',
                          'I vertex at (1, -0.25) and level 1',
                          'I vertex at (-0.75, 0.75) and level 1',
                          'I vertex at (0.75, 0.75) and level 1',
                          'E vertex at (0, 0.5) and level 2',
                          'I vertex at (-1, 0.25) and level 2',
                          'I vertex at (1, 0.25) and level 2',
                          'E vertex at (0, 0.0) and level 2',
                          'I vertex at (-1, -0.25) and level 2',
                          'I vertex at (1, -0.25) and level 2',
                          'E vertex at (0, -0.5) and level 2',
                          'E vertex at (0, 1) and level 2',
                          'I vertex at (-0.75, 0.75) and level 2',
                          'I vertex at (0.75, 0.75) and level 2']

        expected_edges = [('E vertex at (0, 1) and level 1', 'I vertex at (-0.75, 0.75) and level 1'),
                          ('E vertex at (0, 1) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (0, 0.5) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (0, 0.5) and level 1', 'E vertex at (0, 0.0) and level 1'),
                          ('E vertex at (0, 0.0) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (0, 0.0) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('E vertex at (0, 0.0) and level 1', 'E vertex at (0, -0.5) and level 1'),
                          ('E vertex at (0, -0.5) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('I vertex at (-1, 0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (-1, -0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (1, 0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('I vertex at (1, -0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (0, 0.5) and level 2', 'I vertex at (-1, 0.25) and level 2'),
                          ('E vertex at (0, 0.5) and level 2', 'I vertex at (1, 0.25) and level 2'),
                          ('E vertex at (0, 0.5) and level 2', 'E vertex at (0, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2', 'E vertex at (0, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'E vertex at (0, 0.0) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0, 0.0) and level 2', 'I vertex at (-1, -0.25) and level 2'),
                          ('E vertex at (0, 0.0) and level 2', 'I vertex at (1, -0.25) and level 2'),
                          ('E vertex at (0, 0.0) and level 2', 'E vertex at (0, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2', 'E vertex at (0, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'E vertex at (0, -0.5) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (-0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (0.75, 0.75) and level 2')]
        g = self.graph
        g.showLevel(1)
        g = g.P9(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p9_failed_et(self):
        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))

        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        RHS = nx.Graph()

        RHS.add_node(v0 := Vertex((0, 1), "E", 1))
        RHS.add_node(v1 := Vertex((0, 0.5), "E", 1))
        RHS.add_node(v1_1 := Vertex((0, 0.5), "E", 1))
        RHS.add_node(v2 := Vertex((0, 0.0), "E", 1))
        RHS.add_node(v2_2 := Vertex((0, 0.0), "E", 1))
        RHS.add_node(v3 := Vertex((0, -0.5), "I", 1))
        RHS.add_node(v3_3 := Vertex((0, -0.5), "I", 1))
        RHS.add_node(I_1 := Vertex((-1, 0.25), "I", 1))
        RHS.add_node(I_2 := Vertex((-1, -0.25), "I", 1))
        RHS.add_node(I_3 := Vertex((1, 0.25), "I", 1))
        RHS.add_node(I_4 := Vertex((1, -0.25), "I", 1))

        RHS.add_node(I_0_1 := Vertex((-0.75, 0.75), "I", 1))
        RHS.add_node(I_0_2 := Vertex((0.75, 0.75), "I", 1))

        RHS.add_edges_from(
            [(I_0_1, I_1), (I_0_1, I_2), (I_0_2, I_3), (I_0_2, I_4), (v0, I_0_1), (v0, I_0_2), (I_1, v1), (I_1, v2),
             (I_2, v2), (I_2, v3), (I_3, v1_1), (I_3, v2_2), (I_4, v2_2), (I_4, v3_3), (v1, v2),
             (v2, v3), (v1_1, v2_2), (v2_2, v3_3)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append(
            [v0, v1, v1_1, v2, v2_2, v3, v3_3, I_0_1, I_1, I_0_2, I_2, I_3, I_4])  # appending RHS to first level

        self.graph.graph = RHS

        self.graph.show()
        expected_tiers = ['[E vertex at (0, 1) and level 1]',
                          '[E vertex at (0, 1) and level 1, E vertex at (0, 0.5) and level 1, E vertex '
                          'at (0, 0.5) and level 1, E vertex at (0, 0.0) and level 1, E vertex at (0, '
                          '0.0) and level 1, E vertex at (0, -0.5) and level 1, E vertex at (0, -0.5) '
                          'and level 1, I vertex at (-0.75, 0.75) and level 1, I vertex at (-1, 0.25) '
                          'and level 1, I vertex at (0.75, 0.75) and level 1, I vertex at (-1, -0.25) '
                          'and level 1, I vertex at (1, 0.25) and level 1, I vertex at (1, -0.25) and '
                          'level 1]',
                          '[E vertex at (0, 1) and level 2, E vertex at (0, 0.5) and level 2, E vertex '
                          'at (0, 0.0) and level 2, E vertex at (0, -0.5) and level 2, E vertex at (0, '
                          '-0.5) and level 2, I vertex at (-1, 0.25) and level 2, I vertex at (-1, '
                          '-0.25) and level 2, I vertex at (1, 0.25) and level 2, I vertex at (1, '
                          '-0.25) and level 2, I vertex at (-0.75, 0.75) and level 2, I vertex at '
                          '(0.75, 0.75) and level 2]']

        expected_nodes = ['E vertex at (0, 1) and level 1',
                          'E vertex at (0, 0.5) and level 1',
                          'E vertex at (0, 0.0) and level 1',
                          'E vertex at (0, -0.5) and level 1',
                          'I vertex at (-1, 0.25) and level 1',
                          'I vertex at (-1, -0.25) and level 1',
                          'I vertex at (1, 0.25) and level 1',
                          'I vertex at (1, -0.25) and level 1',
                          'I vertex at (-0.75, 0.75) and level 1',
                          'I vertex at (0.75, 0.75) and level 1',
                          'E vertex at (0, 0.5) and level 2',
                          'I vertex at (-1, 0.25) and level 2',
                          'I vertex at (1, 0.25) and level 2',
                          'E vertex at (0, 0.0) and level 2',
                          'I vertex at (-1, -0.25) and level 2',
                          'I vertex at (1, -0.25) and level 2',
                          'E vertex at (0, -0.5) and level 2',
                          'E vertex at (0, 1) and level 2',
                          'I vertex at (-0.75, 0.75) and level 2',
                          'I vertex at (0.75, 0.75) and level 2']

        expected_edges = [('E vertex at (0, 1) and level 1', 'I vertex at (-0.75, 0.75) and level 1'),
                          ('E vertex at (0, 1) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (0, 0.5) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (0, 0.5) and level 1', 'E vertex at (0, 0.0) and level 1'),
                          ('E vertex at (0, 0.0) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (0, 0.0) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('E vertex at (0, 0.0) and level 1', 'E vertex at (0, -0.5) and level 1'),
                          ('E vertex at (0, -0.5) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('I vertex at (-1, 0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (-1, -0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (1, 0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('I vertex at (1, -0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (0, 0.5) and level 2', 'I vertex at (-1, 0.25) and level 2'),
                          ('E vertex at (0, 0.5) and level 2', 'I vertex at (1, 0.25) and level 2'),
                          ('E vertex at (0, 0.5) and level 2', 'E vertex at (0, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2', 'E vertex at (0, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'E vertex at (0, 0.0) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0, 0.0) and level 2', 'I vertex at (-1, -0.25) and level 2'),
                          ('E vertex at (0, 0.0) and level 2', 'I vertex at (1, -0.25) and level 2'),
                          ('E vertex at (0, 0.0) and level 2', 'E vertex at (0, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2', 'E vertex at (0, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'E vertex at (0, -0.5) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (-0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (0.75, 0.75) and level 2')]
        g = self.graph
        g.showLevel(1)
        g = g.P9(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p9_fail(self):
        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))

        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        RHS = nx.Graph()

        RHS.add_node(v0 := Vertex((0, 1), "E", 1))
        RHS.add_node(v1 := Vertex((0, 0.5), "E", 1))
        RHS.add_node(v1_1 := Vertex((0, 0.5), "E", 1))
        RHS.add_node(v2 := Vertex((0, 0.25), "E", 1))
        RHS.add_node(v2_2 := Vertex((0, 0.25), "E", 1))
        RHS.add_node(v3 := Vertex((0, 2 - 0.5), "E", 1))
        RHS.add_node(v3_3 := Vertex((0, -0.5), "E", 1))
        RHS.add_node(I_1 := Vertex((-1, 0.25), "I", 1))
        RHS.add_node(I_2 := Vertex((-1, -0.25), "I", 1))
        RHS.add_node(I_3 := Vertex((1, 0.25), "I", 1))
        RHS.add_node(I_4 := Vertex((1, -0.25), "I", 1))

        RHS.add_node(I_0_1 := Vertex((-0.75, 0.75), "I", 1))
        RHS.add_node(I_0_2 := Vertex((0.75, 0.75), "I", 1))

        RHS.add_edges_from(
            [(I_0_1, I_1), (I_0_1, I_2), (I_0_2, I_3), (I_0_2, I_4), (v0, I_0_1), (v0, I_0_2), (I_1, v1), (I_1, v2),
             (I_2, v2), (I_2, v3), (I_3, v1_1), (I_3, v2_2), (I_4, v2_2), (I_4, v3_3), (v1, v2),
             (v2, v3), (v1_1, v2_2), (v2_2, v3_3)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append(
            [v0, v1, v1_1, v2, v2_2, v3, v3_3, I_0_1, I_1, I_0_2, I_2, I_3, I_4])  # appending RHS to first level

        self.graph.graph = RHS
        expected_tiers = ['[E vertex at (0, 1) and level 1]',
                          '[E vertex at (0, 1) and level 1, E vertex at (0, 0.5) and level 1, E vertex '
                          'at (0, 0.5) and level 1, E vertex at (0, 0.0) and level 1, E vertex at (0, '
                          '0.0) and level 1, E vertex at (0, -0.5) and level 1, E vertex at (0, -0.5) '
                          'and level 1, I vertex at (-0.75, 0.75) and level 1, I vertex at (-1, 0.25) '
                          'and level 1, I vertex at (0.75, 0.75) and level 1, I vertex at (-1, -0.25) '
                          'and level 1, I vertex at (1, 0.25) and level 1, I vertex at (1, -0.25) and '
                          'level 1]',
                          '[E vertex at (0, 1) and level 2, E vertex at (0, 0.5) and level 2, E vertex '
                          'at (0, 0.0) and level 2, E vertex at (0, -0.5) and level 2, E vertex at (0, '
                          '-0.5) and level 2, I vertex at (-1, 0.25) and level 2, I vertex at (-1, '
                          '-0.25) and level 2, I vertex at (1, 0.25) and level 2, I vertex at (1, '
                          '-0.25) and level 2, I vertex at (-0.75, 0.75) and level 2, I vertex at '
                          '(0.75, 0.75) and level 2]']

        expected_nodes = ['E vertex at (0, 1) and level 1',
                          'E vertex at (0, 0.5) and level 1',
                          'E vertex at (0, 0.0) and level 1',
                          'E vertex at (0, -0.5) and level 1',
                          'I vertex at (-1, 0.25) and level 1',
                          'I vertex at (-1, -0.25) and level 1',
                          'I vertex at (1, 0.25) and level 1',
                          'I vertex at (1, -0.25) and level 1',
                          'I vertex at (-0.75, 0.75) and level 1',
                          'I vertex at (0.75, 0.75) and level 1',
                          'E vertex at (0, 0.5) and level 2',
                          'I vertex at (-1, 0.25) and level 2',
                          'I vertex at (1, 0.25) and level 2',
                          'E vertex at (0, 0.0) and level 2',
                          'I vertex at (-1, -0.25) and level 2',
                          'I vertex at (1, -0.25) and level 2',
                          'E vertex at (0, -0.5) and level 2',
                          'E vertex at (0, 1) and level 2',
                          'I vertex at (-0.75, 0.75) and level 2',
                          'I vertex at (0.75, 0.75) and level 2']

        expected_edges = [('E vertex at (0, 1) and level 1', 'I vertex at (-0.75, 0.75) and level 1'),
                          ('E vertex at (0, 1) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (0, 0.5) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (0, 0.5) and level 1', 'E vertex at (0, 0.0) and level 1'),
                          ('E vertex at (0, 0.0) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (0, 0.0) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('E vertex at (0, 0.0) and level 1', 'E vertex at (0, -0.5) and level 1'),
                          ('E vertex at (0, -0.5) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('I vertex at (-1, 0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (-1, -0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (1, 0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('I vertex at (1, -0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (0, 0.5) and level 2', 'I vertex at (-1, 0.25) and level 2'),
                          ('E vertex at (0, 0.5) and level 2', 'I vertex at (1, 0.25) and level 2'),
                          ('E vertex at (0, 0.5) and level 2', 'E vertex at (0, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2', 'E vertex at (0, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'E vertex at (0, 0.0) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0, 0.0) and level 2', 'I vertex at (-1, -0.25) and level 2'),
                          ('E vertex at (0, 0.0) and level 2', 'I vertex at (1, -0.25) and level 2'),
                          ('E vertex at (0, 0.0) and level 2', 'E vertex at (0, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2', 'E vertex at (0, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'E vertex at (0, -0.5) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (-0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (0.75, 0.75) and level 2')]
        g = self.graph
        g.showLevel(1)
        g = g.P9(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p10_fail(self):
        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))

        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        RHS = nx.Graph()

        RHS.add_node(v0 := Vertex((0, 1), "E", 1))
        RHS.add_node(v1 := Vertex((0.0, 0.5), "E", 1))
        RHS.add_node(v2 := Vertex((-0.5, 0.0), "E", 1))
        RHS.add_node(v2_2 := Vertex((0.5, 0.0), "E", 1))
        RHS.add_node(v3 := Vertex((-0.5, -0.5), "E", 1))
        RHS.add_node(v3_3 := Vertex((0.5, -0.5), "E", 1))
        RHS.add_node(I_1 := Vertex((-1, 0.25), "I", 1))
        RHS.add_node(I_2 := Vertex((-1, -0.25), "I", 1))
        RHS.add_node(I_3 := Vertex((1, 0.25), "I", 1))
        RHS.add_node(I_4 := Vertex((1, -0.25), "I", 1))

        RHS.add_node(I_0_1 := Vertex((-0.75, 0.75), "I", 1))
        RHS.add_node(I_0_2 := Vertex((0.75, 0.75), "I", 1))

        RHS.add_edges_from(
            [(I_0_1, I_1), (I_0_1, I_2), (I_0_2, I_3), (I_0_2, I_4), (v0, I_0_1), (v0, I_0_2), (I_1, v1), (I_1, v2),
             (I_2, v2), (I_2, v3), (I_3, v1), (I_3, v2_2), (I_4, v2_2), (I_4, v3_3), (v1, v2),
             (v2, v3), (v1, v2_2), (v2_2, v3_3)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append(
            [v0, v1, v2, v2_2, v3, v3_3, I_0_1, I_1, I_0_2, I_2, I_3, I_4])  # appending RHS to first level

        self.graph.graph = RHS
        expected_tiers = ['[E vertex at (0, 1) and level 1]',
                          '[E vertex at (0, 1) and level 1, E vertex at (0.0, 0.5) and level 1, E '
                          'vertex at (-0.5, 0.0) and level 1, E vertex at (0.5, 0.0) and level 1, E '
                          'vertex at (-0.5, -0.5) and level 1, E vertex at (0.5, -0.5) and level 1, I '
                          'vertex at (-0.75, 0.75) and level 1, I vertex at (-1, 0.25) and level 1, I '
                          'vertex at (0.75, 0.75) and level 1, I vertex at (-1, -0.25) and level 1, I '
                          'vertex at (1, 0.25) and level 1, I vertex at (1, -0.25) and level 1]',
                          '[E vertex at (0, 1) and level 2, E vertex at (0.0, 0.5) and level 2, E '
                          'vertex at (-0.5, 0.0) and level 2, E vertex at (-0.5, -0.5) and level 2, E '
                          'vertex at (-0.5, -0.5) and level 2, I vertex at (-1, 0.25) and level 2, I '
                          'vertex at (-1, -0.25) and level 2, I vertex at (1, 0.25) and level 2, I '
                          'vertex at (1, -0.25) and level 2, I vertex at (-0.75, 0.75) and level 2, I '
                          'vertex at (0.75, 0.75) and level 2]']

        expected_nodes = ['E vertex at (0, 1) and level 1',
                          'E vertex at (0.0, 0.5) and level 1',
                          'E vertex at (-0.5, 0.0) and level 1',
                          'E vertex at (-0.5, -0.5) and level 1',
                          'I vertex at (-1, 0.25) and level 1',
                          'I vertex at (-1, -0.25) and level 1',
                          'I vertex at (1, 0.25) and level 1',
                          'I vertex at (1, -0.25) and level 1',
                          'I vertex at (-0.75, 0.75) and level 1',
                          'I vertex at (0.75, 0.75) and level 1',
                          'E vertex at (0.0, 0.5) and level 2',
                          'I vertex at (-1, 0.25) and level 2',
                          'I vertex at (1, 0.25) and level 2',
                          'E vertex at (-0.5, 0.0) and level 2',
                          'I vertex at (-1, -0.25) and level 2',
                          'I vertex at (1, -0.25) and level 2',
                          'E vertex at (-0.5, -0.5) and level 2',
                          'E vertex at (0, 1) and level 2',
                          'I vertex at (-0.75, 0.75) and level 2',
                          'I vertex at (0.75, 0.75) and level 2']

        expected_edges = [('E vertex at (0, 1) and level 1', 'I vertex at (-0.75, 0.75) and level 1'),
                          ('E vertex at (0, 1) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 1', 'I vertex at (1, 0.25) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 1', 'E vertex at (-0.5, 0.0) and level 1'),
                          ('E vertex at (-0.5, 0.0) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (-0.5, 0.0) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('E vertex at (-0.5, 0.0) and level 1',
                           'E vertex at (-0.5, -0.5) and level 1'),
                          ('E vertex at (-0.5, -0.5) and level 1',
                           'I vertex at (-1, -0.25) and level 1'),
                          ('I vertex at (-1, 0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (-1, -0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (1, 0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('I vertex at (1, -0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 2', 'I vertex at (-1, 0.25) and level 2'),
                          ('E vertex at (0.0, 0.5) and level 2', 'I vertex at (1, 0.25) and level 2'),
                          ('E vertex at (0.0, 0.5) and level 2', 'E vertex at (-0.5, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2', 'E vertex at (-0.5, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'E vertex at (-0.5, 0.0) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (-0.5, 0.0) and level 2', 'I vertex at (-1, -0.25) and level 2'),
                          ('E vertex at (-0.5, 0.0) and level 2', 'I vertex at (1, -0.25) and level 2'),
                          ('E vertex at (-0.5, 0.0) and level 2',
                           'E vertex at (-0.5, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2',
                           'E vertex at (-0.5, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'E vertex at (-0.5, -0.5) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (-0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (0.75, 0.75) and level 2')]
        g = self.graph
        g.showLevel(1)
        g = g.P10(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p10_pass(self):
        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))

        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        RHS = nx.Graph()

        RHS.add_node(v0 := Vertex((0, 1), "E", 1))
        RHS.add_node(v1 := Vertex((0.0, 0.5), "E", 1))
        RHS.add_node(v2 := Vertex((0.0, 0.0), "E", 1))
        RHS.add_node(v2_2 := Vertex((0.0, 0.0), "E", 1))
        RHS.add_node(v3 := Vertex((0.0, -0.5), "E", 1))
        RHS.add_node(v3_3 := Vertex((0.0, -0.5), "E", 1))
        RHS.add_node(I_1 := Vertex((-1, 0.25), "I", 1))
        RHS.add_node(I_2 := Vertex((-1, -0.25), "I", 1))
        RHS.add_node(I_3 := Vertex((1, 0.25), "I", 1))
        RHS.add_node(I_4 := Vertex((1, -0.25), "I", 1))

        RHS.add_node(I_0_1 := Vertex((-0.75, 0.75), "I", 1))
        RHS.add_node(I_0_2 := Vertex((0.75, 0.75), "I", 1))

        RHS.add_edges_from(
            [(I_0_1, I_1), (I_0_1, I_2), (I_0_2, I_3), (I_0_2, I_4), (v0, I_0_1), (v0, I_0_2), (I_1, v1), (I_1, v2),
             (I_2, v2), (I_2, v3), (I_3, v1), (I_3, v2_2), (I_4, v2_2), (I_4, v3_3), (v1, v2),
             (v2, v3), (v1, v2_2), (v2_2, v3_3)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append(
            [v0, v1, v2, v2_2, v3, v3_3, I_0_1, I_1, I_0_2, I_2, I_3, I_4])  # appending RHS to first level

        self.graph.graph = RHS
        expected_tiers = ['[E vertex at (0, 1) and level 1]',
                          '[E vertex at (0, 1) and level 1, E vertex at (0.0, 0.5) and level 1, E '
                          'vertex at (0.0, 0.0) and level 1, E vertex at (0.0, 0.0) and level 1, E '
                          'vertex at (0.0, -0.5) and level 1, E vertex at (0.0, -0.5) and level 1, I '
                          'vertex at (-0.75, 0.75) and level 1, I vertex at (-1, 0.25) and level 1, I '
                          'vertex at (0.75, 0.75) and level 1, I vertex at (-1, -0.25) and level 1, I '
                          'vertex at (1, 0.25) and level 1, I vertex at (1, -0.25) and level 1]',
                          '[E vertex at (0, 1) and level 2, E vertex at (0.0, 0.5) and level 2, E '
                          'vertex at (0.0, 0.0) and level 2, E vertex at (0.0, -0.5) and level 2, E '
                          'vertex at (0.0, -0.5) and level 2, I vertex at (-1, 0.25) and level 2, I '
                          'vertex at (-1, -0.25) and level 2, I vertex at (1, 0.25) and level 2, I '
                          'vertex at (1, -0.25) and level 2, I vertex at (-0.75, 0.75) and level 2, I '
                          'vertex at (0.75, 0.75) and level 2]']

        expected_nodes = ['E vertex at (0, 1) and level 1',
                          'E vertex at (0.0, 0.5) and level 1',
                          'E vertex at (0.0, 0.0) and level 1',
                          'E vertex at (0.0, -0.5) and level 1',
                          'I vertex at (-1, 0.25) and level 1',
                          'I vertex at (-1, -0.25) and level 1',
                          'I vertex at (1, 0.25) and level 1',
                          'I vertex at (1, -0.25) and level 1',
                          'I vertex at (-0.75, 0.75) and level 1',
                          'I vertex at (0.75, 0.75) and level 1',
                          'E vertex at (0.0, 0.5) and level 2',
                          'I vertex at (-1, 0.25) and level 2',
                          'I vertex at (1, 0.25) and level 2',
                          'E vertex at (0.0, 0.0) and level 2',
                          'I vertex at (-1, -0.25) and level 2',
                          'I vertex at (1, -0.25) and level 2',
                          'E vertex at (0.0, -0.5) and level 2',
                          'E vertex at (0, 1) and level 2',
                          'I vertex at (-0.75, 0.75) and level 2',
                          'I vertex at (0.75, 0.75) and level 2']
        expected_edges = [('E vertex at (0, 1) and level 1', 'I vertex at (-0.75, 0.75) and level 1'),
                          ('E vertex at (0, 1) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 1', 'I vertex at (1, 0.25) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 1', 'E vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (0.0, 0.0) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (0.0, 0.0) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('E vertex at (0.0, 0.0) and level 1', 'E vertex at (0.0, -0.5) and level 1'),
                          ('E vertex at (0.0, -0.5) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('I vertex at (-1, 0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (-1, -0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (1, 0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('I vertex at (1, -0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 2', 'I vertex at (-1, 0.25) and level 2'),
                          ('E vertex at (0.0, 0.5) and level 2', 'I vertex at (1, 0.25) and level 2'),
                          ('E vertex at (0.0, 0.5) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0.0, 0.0) and level 2', 'I vertex at (-1, -0.25) and level 2'),
                          ('E vertex at (0.0, 0.0) and level 2', 'I vertex at (1, -0.25) and level 2'),
                          ('E vertex at (0.0, 0.0) and level 2', 'E vertex at (0.0, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2', 'E vertex at (0.0, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'E vertex at (0.0, -0.5) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (-0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (0.75, 0.75) and level 2')]

        g = self.graph
        g.showLevel(1)
        g = g.P10(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p10_fail_remove_edge(self):
        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))

        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        RHS = nx.Graph()

        RHS.add_node(v0 := Vertex((0, 1), "E", 1))
        RHS.add_node(v1 := Vertex((0.0, 0.5), "E", 1))
        RHS.add_node(v2 := Vertex((0.0, 0.0), "E", 1))
        RHS.add_node(v2_2 := Vertex((0.0, 0.0), "E", 1))
        RHS.add_node(v3 := Vertex((0.0, -0.5), "E", 1))
        RHS.add_node(v3_3 := Vertex((0.0, -0.5), "E", 1))
        RHS.add_node(I_1 := Vertex((-1, 0.25), "I", 1))
        RHS.add_node(I_2 := Vertex((-1, -0.25), "I", 1))
        RHS.add_node(I_3 := Vertex((1, 0.25), "I", 1))
        RHS.add_node(I_4 := Vertex((1, -0.25), "I", 1))

        RHS.add_node(I_0_1 := Vertex((-0.75, 0.75), "I", 1))
        RHS.add_node(I_0_2 := Vertex((0.75, 0.75), "I", 1))

        RHS.add_edges_from(
            [(I_0_1, I_1), (I_0_1, I_2), (I_0_2, I_3), (I_0_2, I_4), (v0, I_0_1), (v0, I_0_2), (I_1, v1), (I_1, v2),
             (I_2, v2), (I_3, v1), (I_3, v2_2), (I_4, v2_2), (I_4, v3_3), (v1, v2),
             (v2, v3), (v1, v2_2)])

        self.graph.tiers[0] = [v0]
        self.graph.tiers.append(
            [v0, v1, v2, v2_2, v3, v3_3, I_0_1, I_1, I_0_2, I_2, I_3, I_4])  # appending RHS to first level

        self.graph.graph = RHS
        self.graph.show()
        expected_tiers = ['[E vertex at (0, 1) and level 1]',
                          '[E vertex at (0, 1) and level 1, E vertex at (0.0, 0.5) and level 1, E '
                          'vertex at (0.0, 0.0) and level 1, E vertex at (0.0, 0.0) and level 1, E '
                          'vertex at (0.0, -0.5) and level 1, E vertex at (0.0, -0.5) and level 1, I '
                          'vertex at (-0.75, 0.75) and level 1, I vertex at (-1, 0.25) and level 1, I '
                          'vertex at (0.75, 0.75) and level 1, I vertex at (-1, -0.25) and level 1, I '
                          'vertex at (1, 0.25) and level 1, I vertex at (1, -0.25) and level 1]',
                          '[E vertex at (0, 1) and level 2, E vertex at (0.0, 0.5) and level 2, E '
                          'vertex at (0.0, 0.0) and level 2, E vertex at (0.0, -0.5) and level 2, E '
                          'vertex at (0.0, -0.5) and level 2, I vertex at (-1, 0.25) and level 2, I '
                          'vertex at (-1, -0.25) and level 2, I vertex at (1, 0.25) and level 2, I '
                          'vertex at (1, -0.25) and level 2, I vertex at (-0.75, 0.75) and level 2, I '
                          'vertex at (0.75, 0.75) and level 2]']

        expected_nodes = ['E vertex at (0, 1) and level 1',
                          'E vertex at (0.0, 0.5) and level 1',
                          'E vertex at (0.0, 0.0) and level 1',
                          'E vertex at (0.0, -0.5) and level 1',
                          'I vertex at (-1, 0.25) and level 1',
                          'I vertex at (-1, -0.25) and level 1',
                          'I vertex at (1, 0.25) and level 1',
                          'I vertex at (1, -0.25) and level 1',
                          'I vertex at (-0.75, 0.75) and level 1',
                          'I vertex at (0.75, 0.75) and level 1',
                          'E vertex at (0.0, 0.5) and level 2',
                          'I vertex at (-1, 0.25) and level 2',
                          'I vertex at (1, 0.25) and level 2',
                          'E vertex at (0.0, 0.0) and level 2',
                          'I vertex at (-1, -0.25) and level 2',
                          'I vertex at (1, -0.25) and level 2',
                          'E vertex at (0.0, -0.5) and level 2',
                          'E vertex at (0, 1) and level 2',
                          'I vertex at (-0.75, 0.75) and level 2',
                          'I vertex at (0.75, 0.75) and level 2']
        expected_edges = [('E vertex at (0, 1) and level 1', 'I vertex at (-0.75, 0.75) and level 1'),
                          ('E vertex at (0, 1) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 1', 'I vertex at (1, 0.25) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 1', 'E vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (0.0, 0.0) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (0.0, 0.0) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('E vertex at (0.0, 0.0) and level 1', 'E vertex at (0.0, -0.5) and level 1'),
                          ('E vertex at (0.0, -0.5) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('I vertex at (-1, 0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (-1, -0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (1, 0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('I vertex at (1, -0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 2', 'I vertex at (-1, 0.25) and level 2'),
                          ('E vertex at (0.0, 0.5) and level 2', 'I vertex at (1, 0.25) and level 2'),
                          ('E vertex at (0.0, 0.5) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0.0, 0.0) and level 2', 'I vertex at (-1, -0.25) and level 2'),
                          ('E vertex at (0.0, 0.0) and level 2', 'I vertex at (1, -0.25) and level 2'),
                          ('E vertex at (0.0, 0.0) and level 2', 'E vertex at (0.0, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2', 'E vertex at (0.0, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'E vertex at (0.0, -0.5) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (-0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (0.75, 0.75) and level 2')]

        g = self.graph
        g.showLevel(1)
        g = g.P10(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p10_failed_eth(self):
        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))

        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        RHS = nx.Graph()

        RHS.add_node(v0 := Vertex((0, 1), "E", 1))
        RHS.add_node(v1 := Vertex((0.0, 0.5), "E", 1))
        RHS.add_node(v2 := Vertex((0.0, 0.0), "E", 1))
        RHS.add_node(v2_2 := Vertex((0.0, 0.0), "E", 1))
        RHS.add_node(v3 := Vertex((0.0, -0.5), "E", 1))
        RHS.add_node(v3_3 := Vertex((0.0, -0.5), "I", 1))
        RHS.add_node(I_1 := Vertex((-1, 0.25), "I", 1))
        RHS.add_node(I_2 := Vertex((-1, -0.25), "I", 1))
        RHS.add_node(I_3 := Vertex((1, 0.25), "I", 1))
        RHS.add_node(I_4 := Vertex((1, -0.25), "I", 1))

        RHS.add_node(I_0_1 := Vertex((-0.75, 0.75), "I", 1))
        RHS.add_node(I_0_2 := Vertex((0.75, 0.75), "I", 1))

        RHS.add_edges_from(
            [(I_0_1, I_1), (I_0_1, I_2), (I_0_2, I_3), (I_0_2, I_4), (v0, I_0_1), (v0, I_0_2), (I_1, v1), (I_1, v2),
             (I_2, v2), (I_2, v3), (I_3, v1), (I_3, v2_2), (I_4, v2_2), (I_4, v3_3), (v1, v2),
             (v2, v3), (v1, v2_2), (v2_2, v3_3)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append(
            [v0, v1, v2, v2_2, v3, v3_3, I_0_1, I_1, I_0_2, I_2, I_3, I_4])  # appending RHS to first level

        self.graph.graph = RHS
        self.graph.show()
        expected_tiers = ['[E vertex at (0, 1) and level 1]',
                          '[E vertex at (0, 1) and level 1, E vertex at (0.0, 0.5) and level 1, E '
                          'vertex at (0.0, 0.0) and level 1, E vertex at (0.0, 0.0) and level 1, E '
                          'vertex at (0.0, -0.5) and level 1, E vertex at (0.0, -0.5) and level 1, I '
                          'vertex at (-0.75, 0.75) and level 1, I vertex at (-1, 0.25) and level 1, I '
                          'vertex at (0.75, 0.75) and level 1, I vertex at (-1, -0.25) and level 1, I '
                          'vertex at (1, 0.25) and level 1, I vertex at (1, -0.25) and level 1]',
                          '[E vertex at (0, 1) and level 2, E vertex at (0.0, 0.5) and level 2, E '
                          'vertex at (0.0, 0.0) and level 2, E vertex at (0.0, -0.5) and level 2, E '
                          'vertex at (0.0, -0.5) and level 2, I vertex at (-1, 0.25) and level 2, I '
                          'vertex at (-1, -0.25) and level 2, I vertex at (1, 0.25) and level 2, I '
                          'vertex at (1, -0.25) and level 2, I vertex at (-0.75, 0.75) and level 2, I '
                          'vertex at (0.75, 0.75) and level 2]']

        expected_nodes = ['E vertex at (0, 1) and level 1',
                          'E vertex at (0.0, 0.5) and level 1',
                          'E vertex at (0.0, 0.0) and level 1',
                          'E vertex at (0.0, -0.5) and level 1',
                          'I vertex at (-1, 0.25) and level 1',
                          'I vertex at (-1, -0.25) and level 1',
                          'I vertex at (1, 0.25) and level 1',
                          'I vertex at (1, -0.25) and level 1',
                          'I vertex at (-0.75, 0.75) and level 1',
                          'I vertex at (0.75, 0.75) and level 1',
                          'E vertex at (0.0, 0.5) and level 2',
                          'I vertex at (-1, 0.25) and level 2',
                          'I vertex at (1, 0.25) and level 2',
                          'E vertex at (0.0, 0.0) and level 2',
                          'I vertex at (-1, -0.25) and level 2',
                          'I vertex at (1, -0.25) and level 2',
                          'E vertex at (0.0, -0.5) and level 2',
                          'E vertex at (0, 1) and level 2',
                          'I vertex at (-0.75, 0.75) and level 2',
                          'I vertex at (0.75, 0.75) and level 2']
        expected_edges = [('E vertex at (0, 1) and level 1', 'I vertex at (-0.75, 0.75) and level 1'),
                          ('E vertex at (0, 1) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 1', 'I vertex at (1, 0.25) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 1', 'E vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (0.0, 0.0) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (0.0, 0.0) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('E vertex at (0.0, 0.0) and level 1', 'E vertex at (0.0, -0.5) and level 1'),
                          ('E vertex at (0.0, -0.5) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('I vertex at (-1, 0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (-1, -0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (1, 0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('I vertex at (1, -0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 2', 'I vertex at (-1, 0.25) and level 2'),
                          ('E vertex at (0.0, 0.5) and level 2', 'I vertex at (1, 0.25) and level 2'),
                          ('E vertex at (0.0, 0.5) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0.0, 0.0) and level 2', 'I vertex at (-1, -0.25) and level 2'),
                          ('E vertex at (0.0, 0.0) and level 2', 'I vertex at (1, -0.25) and level 2'),
                          ('E vertex at (0.0, 0.0) and level 2', 'E vertex at (0.0, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2', 'E vertex at (0.0, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'E vertex at (0.0, -0.5) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (-0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (0.75, 0.75) and level 2')]

        g = self.graph
        g.showLevel(1)
        g = g.P10(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p10_pass_additional(self):
        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))

        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        RHS = nx.Graph()

        RHS.add_node(v0 := Vertex((0, 1), "E", 1))
        RHS.add_node(v1 := Vertex((0.0, 0.5), "E", 1))
        RHS.add_node(v2 := Vertex((0.0, 0.0), "E", 1))
        RHS.add_node(v2_2 := Vertex((0.0, 0.0), "E", 1))
        RHS.add_node(v3 := Vertex((0.0, -0.5), "E", 1))
        RHS.add_node(v3_3 := Vertex((0.0, -0.5), "E", 1))
        RHS.add_node(I_1 := Vertex((-1, 0.25), "I", 1))
        RHS.add_node(I_2 := Vertex((-1, -0.25), "I", 1))
        RHS.add_node(I_3 := Vertex((1, 0.25), "I", 1))
        RHS.add_node(I_4 := Vertex((1, -0.25), "I", 1))

        RHS.add_node(additional1 := Vertex((1, -1), "I", 1))
        RHS.add_node(additional2 := Vertex((-1, 1), "I", 1))

        RHS.add_node(I_0_1 := Vertex((-0.75, 0.75), "I", 1))
        RHS.add_node(I_0_2 := Vertex((0.75, 0.75), "I", 1))

        RHS.add_edges_from(
            [(I_0_1, I_1), (I_0_1, I_2), (I_0_2, I_3), (I_0_2, I_4), (v0, I_0_1), (v0, I_0_2), (I_1, v1), (I_1, v2),
             (I_2, v2), (I_2, v3), (I_3, v1), (I_3, v2_2), (I_4, v2_2), (I_4, v3_3), (v1, v2),
             (v2, v3), (v1, v2_2), (v2_2, v3_3), (I_0_2, additional1), (I_0_2, additional2)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append(
            [v0, v1, v2, v2_2, v3, v3_3, I_0_1, I_1, I_0_2, I_2, I_3, I_4, additional1,
             additional2])  # appending RHS to first level

        self.graph.graph = RHS
        expected_tiers = ['[E vertex at (0, 1) and level 1]',
                          '[E vertex at (0, 1) and level 1, E vertex at (0.0, 0.5) and level 1, E '
                          'vertex at (0.0, 0.0) and level 1, E vertex at (0.0, 0.0) and level 1, E '
                          'vertex at (0.0, -0.5) and level 1, E vertex at (0.0, -0.5) and level 1, I '
                          'vertex at (-0.75, 0.75) and level 1, I vertex at (-1, 0.25) and level 1, I '
                          'vertex at (0.75, 0.75) and level 1, I vertex at (-1, -0.25) and level 1, I '
                          'vertex at (1, 0.25) and level 1, I vertex at (1, -0.25) and level 1, I '
                          'vertex at (1, -1) and level 1, I vertex at (-1, 1) and level 1]',
                          '[E vertex at (0, 1) and level 2, E vertex at (0.0, 0.5) and level 2, E '
                          'vertex at (0.0, 0.0) and level 2, E vertex at (0.0, -0.5) and level 2, E '
                          'vertex at (0.0, -0.5) and level 2, I vertex at (-1, 0.25) and level 2, I '
                          'vertex at (-1, -0.25) and level 2, I vertex at (1, 0.25) and level 2, I '
                          'vertex at (1, -0.25) and level 2, I vertex at (-0.75, 0.75) and level 2, I '
                          'vertex at (0.75, 0.75) and level 2]']

        expected_nodes = ['E vertex at (0, 1) and level 1',
                          'E vertex at (0.0, 0.5) and level 1',
                          'E vertex at (0.0, 0.0) and level 1',
                          'E vertex at (0.0, -0.5) and level 1',
                          'I vertex at (-1, 0.25) and level 1',
                          'I vertex at (-1, -0.25) and level 1',
                          'I vertex at (1, 0.25) and level 1',
                          'I vertex at (1, -0.25) and level 1',
                          'I vertex at (1, -1) and level 1',
                          'I vertex at (-1, 1) and level 1',
                          'I vertex at (-0.75, 0.75) and level 1',
                          'I vertex at (0.75, 0.75) and level 1',
                          'E vertex at (0.0, 0.5) and level 2',
                          'I vertex at (-1, 0.25) and level 2',
                          'I vertex at (1, 0.25) and level 2',
                          'E vertex at (0.0, 0.0) and level 2',
                          'I vertex at (-1, -0.25) and level 2',
                          'I vertex at (1, -0.25) and level 2',
                          'E vertex at (0.0, -0.5) and level 2',
                          'E vertex at (0, 1) and level 2',
                          'I vertex at (-0.75, 0.75) and level 2',
                          'I vertex at (0.75, 0.75) and level 2']

        expected_edges = [('E vertex at (0, 1) and level 1', 'I vertex at (-0.75, 0.75) and level 1'),
                          ('E vertex at (0, 1) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 1', 'I vertex at (1, 0.25) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 1', 'E vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (0.0, 0.0) and level 1', 'I vertex at (-1, 0.25) and level 1'),
                          ('E vertex at (0.0, 0.0) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('E vertex at (0.0, 0.0) and level 1', 'E vertex at (0.0, -0.5) and level 1'),
                          ('E vertex at (0.0, -0.5) and level 1', 'I vertex at (-1, -0.25) and level 1'),
                          ('I vertex at (-1, 0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (-1, -0.25) and level 1',
                           'I vertex at (-0.75, 0.75) and level 1'),
                          ('I vertex at (1, 0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('I vertex at (1, -0.25) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('I vertex at (1, -1) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('I vertex at (-1, 1) and level 1', 'I vertex at (0.75, 0.75) and level 1'),
                          ('E vertex at (0.0, 0.5) and level 2', 'I vertex at (-1, 0.25) and level 2'),
                          ('E vertex at (0.0, 0.5) and level 2', 'I vertex at (1, 0.25) and level 2'),
                          ('E vertex at (0.0, 0.5) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
                          ('I vertex at (-1, 0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
                          ('I vertex at (1, 0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0.0, 0.0) and level 2', 'I vertex at (-1, -0.25) and level 2'),
                          ('E vertex at (0.0, 0.0) and level 2', 'I vertex at (1, -0.25) and level 2'),
                          ('E vertex at (0.0, 0.0) and level 2', 'E vertex at (0.0, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2', 'E vertex at (0.0, -0.5) and level 2'),
                          ('I vertex at (-1, -0.25) and level 2',
                           'I vertex at (-0.75, 0.75) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'E vertex at (0.0, -0.5) and level 2'),
                          ('I vertex at (1, -0.25) and level 2', 'I vertex at (0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (-0.75, 0.75) and level 2'),
                          ('E vertex at (0, 1) and level 2', 'I vertex at (0.75, 0.75) and level 2')]
        g = self.graph
        g.showLevel(1)
        g = g.P10(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)


if __name__ == "__main__":
    #unittest.main()
    a = P9P10Test()
    a.setUp()
    a.test_p9_pass_3()
    a.test_p9_pass_additional()

