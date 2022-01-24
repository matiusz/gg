import unittest
from visualization import *
import networkx as nx


class P12P13Test(unittest.TestCase):
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

    def test_P13_pass(self):
        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))

        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P13: No match for {v0} found!"

        RHS = nx.Graph()

        RHS.add_node(v0 := Vertex((0, 1), "E", 1))
        RHS.add_node(v1 := Vertex((0.0, 0.5), "E", 1))
        RHS.add_node(v1_2 := Vertex((0.0, 0.0), "E", 1))
        RHS.add_node(v2 := Vertex((0.0, -0.5), "E", 1))
        RHS.add_node(v3_1 := Vertex((0.0, 0.5), "E", 1))
        RHS.add_node(v3_2 := Vertex((0.0, -0.5), "E", 1))
        RHS.add_node(I0_1 := Vertex((-0.25, 0.75), "I", 1))
        RHS.add_node(I0_2 := Vertex((0.25, 0.75), "I", 1))
        RHS.add_node(I1 := Vertex((-0.5, 0.25), "I", 1))
        RHS.add_node(I2 := Vertex((-0.5, -0.25), "I", 1))
        RHS.add_node(I3 := Vertex((0.5, 0.0), "I", 1))

        RHS.add_edges_from(
            [(v0, I0_1), (v0, I0_2), (I0_1, I1), (I0_1, I2), (I1, v1), (I1, v1_2),
             (I2, v1_2), (I2, v2), (v1, v1_2), (v1_2, v2), (I0_2, I3), (I3, v3_1),
             (I3, v3_2), (v3_1, v3_2)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append(
            [v0, v1, v2, v1_2, v3_1, v3_2, I0_1, I0_2, I1, I2, I3])  # appending RHS to first level

        self.graph.graph = RHS
        expected_tiers = ['[E vertex at (0, 1) and level 1]',
                          '[E vertex at (0, 1) and level 1, '
                          'E vertex at (0.0, 0.0) and level 1, '
                          'E vertex at (0.0, 0.5) and level 1, E vertex at (0.0, -0.5) and level 1, '
                          'I vertex at (-0.25, 0.75) and level 1, I vertex at (0.25, 0.75) and level 1, '
                          'I vertex at (-0.5, 0.25) and level 1, I vertex at (-0.5, -0.25) and level 1, '
                          'I vertex at (0.5, 0.0) and level 1]']

        expected_nodes = ['E vertex at (0, 1) and level 1',
                          'E vertex at (0.0, 0.5) and level 1',
                          'E vertex at (0.0, 0.0) and level 1',
                          'E vertex at (0.0, -0.5) and level 1',
                          'I vertex at (-0.25, 0.75) and level 1',
                          'I vertex at (0.25, 0.75) and level 1',
                          'I vertex at (-0.5, 0.25) and level 1',
                          'I vertex at (-0.5, -0.25) and level 1',
                          'I vertex at (0.5, 0.0) and level 1']

        expected_edges = [
            ('E vertex at (0, 1) and level 1', 'I vertex at (-0.25, 0.75) and level 1'),
            ('E vertex at (0, 1) and level 1', 'I vertex at (0.25, 0.75) and level 1'),
            ('E vertex at (0.0, 0.5) and level 1', 'I vertex at (-0.5, 0.25) and level 1'),
            ('E vertex at (0.0, 0.5) and level 1', 'E vertex at (0.0, 0.0) and level 1'),
            ('E vertex at (0.0, 0.5) and level 1', 'I vertex at (0.5, 0.0) and level 1'),
            ('E vertex at (0.0, 0.0) and level 1', 'I vertex at (-0.5, 0.25) and level 1'),
            ('E vertex at (0.0, 0.0) and level 1', 'I vertex at (-0.5, -0.25) and level 1'),
            ('E vertex at (0.0, 0.0) and level 1', 'E vertex at (0.0, -0.5) and level 1'),
            ('E vertex at (0.0, -0.5) and level 1', 'I vertex at (-0.5, -0.25) and level 1'),
            ('E vertex at (0.0, -0.5) and level 1', 'I vertex at (0.5, 0.0) and level 1'),
            ('I vertex at (-0.25, 0.75) and level 1', 'I vertex at (-0.5, 0.25) and level 1'),
            ('I vertex at (-0.25, 0.75) and level 1', 'I vertex at (-0.5, -0.25) and level 1'),
            ('I vertex at (0.25, 0.75) and level 1', 'I vertex at (0.5, 0.0) and level 1')
        ]

        g = self.graph
        g.showLevel(1)
        g = g.P13(1)
        g.showLevel(1)
        #g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)



    def test_P13_additional(self):
        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))

        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P13: No match for {v0} found!"

        RHS = nx.Graph()

        RHS.add_node(v0 := Vertex((0, 1), "E", 1))
        RHS.add_node(v1 := Vertex((0.0, 0.5), "E", 1))
        RHS.add_node(v1_2 := Vertex((0.0, 0.0), "E", 1))
        RHS.add_node(v2 := Vertex((0.0, -0.5), "E", 1))
        RHS.add_node(v3_1 := Vertex((0.0, 0.5), "E", 1))
        RHS.add_node(v3_2 := Vertex((0.0, -0.5), "E", 1))
        RHS.add_node(I0_1 := Vertex((-0.25, 0.75), "I", 1))
        RHS.add_node(I0_2 := Vertex((0.25, 0.75), "I", 1))
        RHS.add_node(I1 := Vertex((-0.5, 0.25), "I", 1))
        RHS.add_node(I2 := Vertex((-0.5, -0.25), "I", 1))
        RHS.add_node(I3 := Vertex((0.5, 0.0), "I", 1))
        RHS.add_node(v_add := Vertex((-0.5, -0.5), "E", 1))

        RHS.add_edges_from(
            [(v0, I0_1), (v0, I0_2), (I0_1, I1), (I0_1, I2), (I1, v1), (I1, v1_2),
             (I2, v1_2), (I2, v2), (v1, v1_2), (v1_2, v2), (I0_2, I3), (I3, v3_1),
             (I3, v3_2), (v3_1, v3_2), (v_add, I2)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append(
            [v0, v1, v2, v1_2, v3_1, v3_2, I0_1, I0_2, I1, I2, I3, v_add])  # appending RHS to first level

        self.graph.graph = RHS
        expected_tiers = ['[E vertex at (0, 1) and level 1]',
                          '[E vertex at (0, 1) and level 1, '
                          'E vertex at (0.0, 0.0) and level 1, '
                          'E vertex at (0.0, 0.5) and level 1, E vertex at (0.0, -0.5) and level 1, '
                          'I vertex at (-0.25, 0.75) and level 1, I vertex at (0.25, 0.75) and level 1, '
                          'I vertex at (-0.5, 0.25) and level 1, I vertex at (-0.5, -0.25) and level 1, '
                          'I vertex at (0.5, 0.0) and level 1, E vertex at (-0.5, -0.5) and level 1]']

        expected_nodes = ['E vertex at (0, 1) and level 1',
                          'E vertex at (0.0, 0.5) and level 1',
                          'E vertex at (0.0, 0.0) and level 1',
                          'E vertex at (0.0, -0.5) and level 1',
                          'I vertex at (-0.25, 0.75) and level 1',
                          'I vertex at (0.25, 0.75) and level 1',
                          'I vertex at (-0.5, 0.25) and level 1',
                          'I vertex at (-0.5, -0.25) and level 1',
                          'I vertex at (0.5, 0.0) and level 1',
                          'E vertex at (-0.5, -0.5) and level 1']

        expected_edges = [
            ('E vertex at (0, 1) and level 1', 'I vertex at (-0.25, 0.75) and level 1'),
            ('E vertex at (0, 1) and level 1', 'I vertex at (0.25, 0.75) and level 1'),
            ('E vertex at (0.0, 0.5) and level 1', 'I vertex at (-0.5, 0.25) and level 1'),
            ('E vertex at (0.0, 0.5) and level 1', 'E vertex at (0.0, 0.0) and level 1'),
            ('E vertex at (0.0, 0.5) and level 1', 'I vertex at (0.5, 0.0) and level 1'),
            ('E vertex at (0.0, 0.0) and level 1', 'I vertex at (-0.5, 0.25) and level 1'),
            ('E vertex at (0.0, 0.0) and level 1', 'I vertex at (-0.5, -0.25) and level 1'),
            ('E vertex at (0.0, 0.0) and level 1', 'E vertex at (0.0, -0.5) and level 1'),
            ('E vertex at (0.0, -0.5) and level 1', 'I vertex at (-0.5, -0.25) and level 1'),
            ('E vertex at (0.0, -0.5) and level 1', 'I vertex at (0.5, 0.0) and level 1'),
            ('I vertex at (-0.25, 0.75) and level 1', 'I vertex at (-0.5, 0.25) and level 1'),
            ('I vertex at (-0.25, 0.75) and level 1', 'I vertex at (-0.5, -0.25) and level 1'),
            ('I vertex at (0.25, 0.75) and level 1', 'I vertex at (0.5, 0.0) and level 1'),
            ('I vertex at (-0.5, -0.25) and level 1', 'E vertex at (-0.5, -0.5) and level 1')
        ]

        g = self.graph
        g.showLevel(1)
        g = g.P13(1)
        g.showLevel(1)
        #g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_P13_fail(self):
        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))

        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P13: No match for {v0} found!"

        RHS = nx.Graph()

        RHS.add_node(v0 := Vertex((0, 1), "E", 1))
        RHS.add_node(v1 := Vertex((0.0, 0.5), "E", 1))
        RHS.add_node(v1_2 := Vertex((0.0, 0.0), "E", 1))
        RHS.add_node(v2 := Vertex((0.0, -0.5), "E", 1))
        RHS.add_node(v3_1 := Vertex((0.0, 0.5), "E", 1))
        RHS.add_node(v3_2 := Vertex((0.0, -0.5), "E", 1))
        RHS.add_node(I0_1 := Vertex((-0.25, 0.75), "I", 1))
        RHS.add_node(I0_2 := Vertex((0.25, 0.75), "I", 1))
        RHS.add_node(I1 := Vertex((-0.5, 0.25), "I", 1))
        RHS.add_node(I3 := Vertex((0.5, 0.0), "I", 1))

        RHS.add_edges_from(
            [(v0, I0_1), (v0, I0_2), (I0_1, I1), (I1, v1), (I1, v1_2),
             (v1, v1_2), (v1_2, v2), (I0_2, I3), (I3, v3_1),
             (I3, v3_2)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append(
            [v0, v1, v2, v1_2, v3_1, v3_2, I0_1, I0_2, I1, I3])  # appending RHS to first level

        self.graph.graph = RHS
        expected_tiers = ['[E vertex at (0, 1) and level 1]',
                          '[E vertex at (0, 1) and level 1, E vertex at (0.0, 0.5) and level 1, '
                          'E vertex at (0.0, -0.5) and level 1, E vertex at (0.0, 0.0) and level 1, '
                          'E vertex at (0.0, 0.5) and level 1, E vertex at (0.0, -0.5) and level 1, '
                          'I vertex at (-0.25, 0.75) and level 1, I vertex at (0.25, 0.75) and level 1, '
                          'I vertex at (-0.5, 0.25) and level 1, '
                          'I vertex at (0.5, 0.0) and level 1]']

        expected_nodes = ['E vertex at (0, 1) and level 1',
                          'E vertex at (0.0, 0.5) and level 1',
                          'E vertex at (0.0, 0.0) and level 1',
                          'E vertex at (0.0, -0.5) and level 1',
                          'E vertex at (0.0, 0.5) and level 1',
                          'E vertex at (0.0, -0.5) and level 1',
                          'I vertex at (-0.25, 0.75) and level 1',
                          'I vertex at (0.25, 0.75) and level 1',
                          'I vertex at (-0.5, 0.25) and level 1',
                          'I vertex at (0.5, 0.0) and level 1']

        expected_edges = [
            ('E vertex at (0, 1) and level 1', 'I vertex at (-0.25, 0.75) and level 1'),
            ('E vertex at (0, 1) and level 1', 'I vertex at (0.25, 0.75) and level 1'),
            ('E vertex at (0.0, 0.5) and level 1', 'I vertex at (-0.5, 0.25) and level 1'),
            ('E vertex at (0.0, 0.5) and level 1', 'E vertex at (0.0, 0.0) and level 1'),
            ('E vertex at (0.0, 0.0) and level 1', 'I vertex at (-0.5, 0.25) and level 1'),
            ('E vertex at (0.0, 0.0) and level 1', 'E vertex at (0.0, -0.5) and level 1'),
            ('E vertex at (0.0, 0.5) and level 1', 'I vertex at (0.5, 0.0) and level 1'),
            ('E vertex at (0.0, -0.5) and level 1', 'I vertex at (0.5, 0.0) and level 1'),
            ('I vertex at (-0.25, 0.75) and level 1', 'I vertex at (-0.5, 0.25) and level 1'),
            ('I vertex at (0.25, 0.75) and level 1', 'I vertex at (0.5, 0.0) and level 1')
        ]

        g = self.graph
        #g.showLevel(1)
        try:
            g = g.P13(1)
        except(AssertionError):
            pass
        g.showLevel(1)
        #g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)


if __name__ == "_main_":
    #unittest.main()
    a = P12P13Test()
    a.test_P13_fail()