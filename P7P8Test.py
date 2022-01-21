import unittest

from visualization import TieredGraph, Vertex, GraphMatcherByLabel
import networkx as nx
from collections import deque


def P8RHS(graph):
    corners = graph.corners

    RHS = nx.Graph()
    RHS.add_node(v0 := Vertex((0, 0), "e", 0))
    RHS.add_node(v1 := Vertex(corners[0], "E", 1))

    RHS.add_node(v1_5 := Vertex(((corners[0][0] + corners[1][0]) / 2,
                                 (corners[0][1] + corners[1][1]) / 2), "E", 1))
    RHS.add_node(v2 := Vertex(corners[1], "E", 1))
    RHS.add_node(v2_5 := Vertex(((corners[1][0] + corners[2][0]) / 2,
                                 (corners[1][1] + corners[2][1]) / 2), "E", 1))
    RHS.add_node(v3 := Vertex(corners[2], "E", 1))
    RHS.add_node(v3_5 := Vertex(((corners[2][0] + corners[3][0]) / 2,
                                 (corners[2][1] + corners[3][1]) / 2), "E", 1))

    RHS.add_node(v4_5 := Vertex(((corners[0][0] + corners[3][0]) / 2,
                                 (corners[0][1] + corners[3][1]) / 2), "E", 1))
    RHS.add_node(v4 := Vertex(corners[3], "E", 1))

    RHS.add_node(i := Vertex(((corners[0][0] + corners[2][0]) / 2,
                              (corners[0][1] + corners[2][1]) / 2), "I", 1))
    RHS.add_edges_from([(v1, v1_5), (v1_5, v2), (v2, v2_5), (v2_5, v3), (v3, v3_5), (v3_5, v4), (v1, v4_5), (v4, v4_5),
                        (v1, i), (v2, i), (v3, i), (v4, i)])
    graph.tiers[0] = [v0]
    graph.tiers.append([v1, v1_5, v2, v2_5, v3, v3_5, v4_5, v4, i])  # appending RHS to first level
    graph.graph = RHS


def P7RHS(graph, rotation: int):
    corners = deque(graph.corners)
    corners.rotate(rotation)

    RHS = nx.Graph()
    RHS.add_node(v0 := Vertex((0, 0), "e", 0))
    RHS.add_node(v1 := Vertex(corners[0], "E", 1))

    RHS.add_node(v1_5 := Vertex(((corners[0][0] + corners[1][0]) / 2,
                                 (corners[0][1] + corners[1][1]) / 2), "E", 1))
    RHS.add_node(v2 := Vertex(corners[1], "E", 1))
    RHS.add_node(v2_5 := Vertex(((corners[1][0] + corners[2][0]) / 2,
                                 (corners[1][1] + corners[2][1]) / 2), "E", 1))
    RHS.add_node(v3 := Vertex(corners[2], "E", 1))
    RHS.add_node(v4_5 := Vertex(((corners[0][0] + corners[3][0]) / 2,
                                 (corners[0][1] + corners[3][1]) / 2), "E", 1))
    RHS.add_node(v4 := Vertex(corners[3], "E", 1))

    RHS.add_node(i := Vertex(((corners[0][0] + corners[2][0]) / 2,
                              (corners[0][1] + corners[2][1]) / 2), "I", 1))
    RHS.add_edges_from([(v1, v1_5), (v1_5, v2), (v2, v2_5), (v2_5, v3), (v3, v4), (v1, v4_5), (v4, v4_5),
                        (v1, i), (v2, i), (v3, i), (v4, i)])
    graph.tiers[0] = [v0]
    graph.tiers.append([v1, v1_5, v2, v2_5, v3, v4_5, v4, i])  # appending RHS to first level
    graph.graph = RHS


class P7P8Test(unittest.TestCase):
    def setUp(self):
        v1 = (-1, 1)
        v2 = (1, 1)
        v3 = (1, -1)
        v4 = (-1, -1)
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

    def test_p7_rotation_0(self):
        P7RHS(self.graph, rotation=0)

        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (-1, 1) and level 1, E vertex at (0.0, 1.0) and level 1, E vertex at (1, 1) and level 1, E vertex at (1.0, 0.0) and level 1, E vertex at (1, -1) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (-1, -1) and level 1, i vertex at (0.0, 0.0) and level 1]",
            "[E vertex at (-1, 1) and level 2, E vertex at (0.0, 1.0) and level 2, E vertex at (1, 1) and level 2, E vertex at (-1, -1) and level 2, E vertex at (-1.0, 0.0) and level 2, E vertex at (1, -1) and level 2, E vertex at (0.0, 0.0) and level 2, E vertex at (1.0, 0.0) and level 2, E vertex at (0.0, -1.0) and level 2, I vertex at (-0.5, 0.5) and level 2, I vertex at (0.5, 0.5) and level 2, I vertex at (-0.5, -0.5) and level 2, I vertex at (0.5, -0.5) and level 2]"
        ]

        expected_nodes = ["e vertex at (0, 0) and level 0",
                          "E vertex at (-1, 1) and level 1",
                          "E vertex at (0.0, 1.0) and level 1",
                          "E vertex at (1, 1) and level 1",
                          "E vertex at (1.0, 0.0) and level 1",
                          "E vertex at (1, -1) and level 1",
                          "E vertex at (-1.0, 0.0) and level 1",
                          "E vertex at (-1, -1) and level 1",
                          "i vertex at (0.0, 0.0) and level 1",
                          "E vertex at (-1, 1) and level 2",
                          "E vertex at (0.0, 1.0) and level 2",
                          "E vertex at (1, 1) and level 2",
                          "E vertex at (1.0, 0.0) and level 2",
                          "E vertex at (1, -1) and level 2",
                          "E vertex at (0.0, -1.0) and level 2",
                          "E vertex at (-1, -1) and level 2",
                          "E vertex at (-1.0, 0.0) and level 2",
                          "E vertex at (0.0, 0.0) and level 2",
                          "I vertex at (-0.5, 0.5) and level 2",
                          "I vertex at (0.5, 0.5) and level 2",
                          "I vertex at (-0.5, -0.5) and level 2",
                          "I vertex at (0.5, -0.5) and level 2"]

        expected_edges = [("E vertex at (-1, 1) and level 1", "E vertex at (0.0, 1.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "E vertex at (-1.0, 0.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (0.0, 1.0) and level 1", "E vertex at (1, 1) and level 1"),
                          ("E vertex at (1, 1) and level 1", "E vertex at (1.0, 0.0) and level 1"),
                          ("E vertex at (1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (1.0, 0.0) and level 1", "E vertex at (1, -1) and level 1"),
                          ("E vertex at (1, -1) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (-1.0, 0.0) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (-1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("i vertex at (0.0, 0.0) and level 1", "I vertex at (-0.5, 0.5) and level 2"),
                          ("i vertex at (0.0, 0.0) and level 1", "I vertex at (0.5, 0.5) and level 2"),
                          ("i vertex at (0.0, 0.0) and level 1", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (-1, 1) and level 2", "E vertex at (0.0, 1.0) and level 2"),
                          ("E vertex at (-1, 1) and level 2", "E vertex at (-1.0, 0.0) and level 2"),
                          ("E vertex at (-1, 1) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "E vertex at (1, 1) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (1, 1) and level 2", "E vertex at (1.0, 0.0) and level 2"),
                          ("E vertex at (1, 1) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "E vertex at (1, -1) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (1, -1) and level 2", "E vertex at (0.0, -1.0) and level 2"),
                          ("E vertex at (1, -1) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2", "E vertex at (-1, -1) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2",
                           "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (-1, -1) and level 2", "E vertex at (-1.0, 0.0) and level 2"),
                          ("E vertex at (-1, -1) and level 2", "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2",
                           "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (0.5, -0.5) and level 2")]

        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))
        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        g = self.graph.P7(1)

        g.showLevel(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p7_rotation_1(self):
        P7RHS(self.graph, rotation=1)

        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (-1, -1) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (-1, 1) and level 1, E vertex at (0.0, 1.0) and level 1, E vertex at (1, 1) and level 1, E vertex at (0.0, -1.0) and level 1, E vertex at (1, -1) and level 1, i vertex at (0.0, 0.0) and level 1]",
            "[E vertex at (-1, -1) and level 2, E vertex at (-1.0, 0.0) and level 2, E vertex at (-1, 1) and level 2, E vertex at (1, -1) and level 2, E vertex at (0.0, -1.0) and level 2, E vertex at (1, 1) and level 2, E vertex at (0.0, 0.0) and level 2, E vertex at (0.0, 1.0) and level 2, E vertex at (1.0, 0.0) and level 2, I vertex at (-0.5, -0.5) and level 2, I vertex at (-0.5, 0.5) and level 2, I vertex at (0.5, -0.5) and level 2, I vertex at (0.5, 0.5) and level 2]"
        ]

        expected_nodes = ["e vertex at (0, 0) and level 0",
                          "E vertex at (-1, -1) and level 1",
                          "E vertex at (-1.0, 0.0) and level 1",
                          "E vertex at (-1, 1) and level 1",
                          "E vertex at (0.0, 1.0) and level 1",
                          "E vertex at (1, 1) and level 1",
                          "E vertex at (0.0, -1.0) and level 1",
                          "E vertex at (1, -1) and level 1",
                          "i vertex at (0.0, 0.0) and level 1",
                          "E vertex at (-1, -1) and level 2",
                          "E vertex at (-1.0, 0.0) and level 2",
                          "E vertex at (-1, 1) and level 2",
                          "E vertex at (0.0, 1.0) and level 2",
                          "E vertex at (1, 1) and level 2",
                          "E vertex at (1.0, 0.0) and level 2",
                          "E vertex at (1, -1) and level 2",
                          "E vertex at (0.0, -1.0) and level 2",
                          "E vertex at (0.0, 0.0) and level 2",
                          "I vertex at (-0.5, -0.5) and level 2",
                          "I vertex at (-0.5, 0.5) and level 2",
                          "I vertex at (0.5, -0.5) and level 2",
                          "I vertex at (0.5, 0.5) and level 2"]

        expected_edges = [("E vertex at (-1, -1) and level 1", "E vertex at (-1.0, 0.0) and level 1"),
                          ("E vertex at (-1, -1) and level 1", "E vertex at (0.0, -1.0) and level 1"),
                          ("E vertex at (-1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (-1.0, 0.0) and level 1", "E vertex at (-1, 1) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "E vertex at (0.0, 1.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (0.0, 1.0) and level 1", "E vertex at (1, 1) and level 1"),
                          ("E vertex at (1, 1) and level 1", "E vertex at (1, -1) and level 1"),
                          ("E vertex at (1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (0.0, -1.0) and level 1", "E vertex at (1, -1) and level 1"),
                          ("E vertex at (1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("i vertex at (0.0, 0.0) and level 1", "I vertex at (-0.5, -0.5) and level 2"),
                          ("i vertex at (0.0, 0.0) and level 1", "I vertex at (-0.5, 0.5) and level 2"),
                          ("i vertex at (0.0, 0.0) and level 1", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (-1, -1) and level 2", "E vertex at (-1.0, 0.0) and level 2"),
                          ("E vertex at (-1, -1) and level 2", "E vertex at (0.0, -1.0) and level 2"),
                          ("E vertex at (-1, -1) and level 2", "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2", "E vertex at (-1, 1) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2",
                           "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (-1, 1) and level 2", "E vertex at (0.0, 1.0) and level 2"),
                          ("E vertex at (-1, 1) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "E vertex at (1, 1) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (1, 1) and level 2", "E vertex at (1.0, 0.0) and level 2"),
                          ("E vertex at (1, 1) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "E vertex at (1, -1) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (1, -1) and level 2", "E vertex at (0.0, -1.0) and level 2"),
                          ("E vertex at (1, -1) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2",
                           "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (0.5, 0.5) and level 2")]

        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))
        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        g = self.graph.P7(1)

        g.showLevel(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p7_rotation_2(self):
        P7RHS(self.graph, rotation=2)

        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (1, -1) and level 1, E vertex at (0.0, -1.0) and level 1, E vertex at (-1, -1) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (-1, 1) and level 1, E vertex at (1.0, 0.0) and level 1, E vertex at (1, 1) and level 1, i vertex at (0.0, 0.0) and level 1]",
            "[E vertex at (1, -1) and level 2, E vertex at (0.0, -1.0) and level 2, E vertex at (-1, -1) and level 2, E vertex at (1, 1) and level 2, E vertex at (1.0, 0.0) and level 2, E vertex at (-1, 1) and level 2, E vertex at (0.0, 0.0) and level 2, E vertex at (-1.0, 0.0) and level 2, E vertex at (0.0, 1.0) and level 2, I vertex at (0.5, -0.5) and level 2, I vertex at (-0.5, -0.5) and level 2, I vertex at (0.5, 0.5) and level 2, I vertex at (-0.5, 0.5) and level 2]"
        ]

        expected_nodes = ["e vertex at (0, 0) and level 0",
                          "E vertex at (1, -1) and level 1",
                          "E vertex at (0.0, -1.0) and level 1",
                          "E vertex at (-1, -1) and level 1",
                          "E vertex at (-1.0, 0.0) and level 1",
                          "E vertex at (-1, 1) and level 1",
                          "E vertex at (1.0, 0.0) and level 1",
                          "E vertex at (1, 1) and level 1",
                          "i vertex at (0.0, 0.0) and level 1",
                          "E vertex at (1, -1) and level 2",
                          "E vertex at (0.0, -1.0) and level 2",
                          "E vertex at (-1, -1) and level 2",
                          "E vertex at (-1.0, 0.0) and level 2",
                          "E vertex at (-1, 1) and level 2",
                          "E vertex at (0.0, 1.0) and level 2",
                          "E vertex at (1, 1) and level 2",
                          "E vertex at (1.0, 0.0) and level 2",
                          "E vertex at (0.0, 0.0) and level 2",
                          "I vertex at (0.5, -0.5) and level 2",
                          "I vertex at (-0.5, -0.5) and level 2",
                          "I vertex at (0.5, 0.5) and level 2",
                          "I vertex at (-0.5, 0.5) and level 2"]

        expected_edges = [("E vertex at (1, -1) and level 1", "E vertex at (0.0, -1.0) and level 1"),
                          ("E vertex at (1, -1) and level 1", "E vertex at (1.0, 0.0) and level 1"),
                          ("E vertex at (1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (0.0, -1.0) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (-1, -1) and level 1", "E vertex at (-1.0, 0.0) and level 1"),
                          ("E vertex at (-1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (-1.0, 0.0) and level 1", "E vertex at (-1, 1) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "E vertex at (1, 1) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (1.0, 0.0) and level 1", "E vertex at (1, 1) and level 1"),
                          ("E vertex at (1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("i vertex at (0.0, 0.0) and level 1", "I vertex at (0.5, -0.5) and level 2"),
                          ("i vertex at (0.0, 0.0) and level 1", "I vertex at (-0.5, -0.5) and level 2"),
                          ("i vertex at (0.0, 0.0) and level 1", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (1, -1) and level 2", "E vertex at (0.0, -1.0) and level 2"),
                          ("E vertex at (1, -1) and level 2", "E vertex at (1.0, 0.0) and level 2"),
                          ("E vertex at (1, -1) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2", "E vertex at (-1, -1) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2",
                           "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (-1, -1) and level 2", "E vertex at (-1.0, 0.0) and level 2"),
                          ("E vertex at (-1, -1) and level 2", "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2", "E vertex at (-1, 1) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2",
                           "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (-1, 1) and level 2", "E vertex at (0.0, 1.0) and level 2"),
                          ("E vertex at (-1, 1) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "E vertex at (1, 1) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (1, 1) and level 2", "E vertex at (1.0, 0.0) and level 2"),
                          ("E vertex at (1, 1) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (-0.5, 0.5) and level 2")]

        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))
        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        g = self.graph.P7(1)

        g.showLevel(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p7_new_vertex(self):
        corners = self.graph.corners
        RHS = nx.Graph()
        RHS.add_node(v0 := Vertex((0, 0), "e", 0))
        RHS.add_node(v1 := Vertex(corners[0], "E", 1))

        RHS.add_node(v1_5 := Vertex(((corners[0][0] + corners[1][0]) / 2,
                                     (corners[0][1] + corners[1][1]) / 2), "E", 1))
        RHS.add_node(v2 := Vertex(corners[1], "E", 1))
        RHS.add_node(v2_5 := Vertex(((corners[1][0] + corners[2][0]) / 2,
                                     (corners[1][1] + corners[2][1]) / 2), "E", 1))
        RHS.add_node(v3 := Vertex(corners[2], "E", 1))
        RHS.add_node(v4_5 := Vertex(((corners[0][0] + corners[3][0]) / 2,
                                     (corners[0][1] + corners[3][1]) / 2), "E", 1))
        RHS.add_node(v4 := Vertex(corners[3], "E", 1))
        RHS.add_node(v6 := Vertex((-1, 2), "E", 1))

        RHS.add_node(i := Vertex(((corners[0][0] + corners[1][0]) / 2,
                                  (corners[0][1] + corners[2][1]) / 2), "I", 1))
        RHS.add_edges_from([(v1, v1_5), (v1_5, v2), (v2, v2_5), (v2_5, v3), (v3, v4), (v1, v4_5), (v4, v4_5),
                            (v1, i), (v2, i), (v3, i), (v4, i)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append([v1, v1_5, v2, v2_5, v3, v4_5, v4, i, v6])  # appending RHS to first level
        self.graph.graph = RHS

        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (-1, 1) and level 1, E vertex at (0.0, 1.0) and level 1, E vertex at (1, 1) and level 1, E vertex at (1.0, 0.0) and level 1, E vertex at (1, -1) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (-1, -1) and level 1, i vertex at (0.0, 0.0) and level 1, E vertex at (-1, 2) and level 1]",
            "[E vertex at (-1, 1) and level 2, E vertex at (0.0, 1.0) and level 2, E vertex at (1, 1) and level 2, E vertex at (-1, -1) and level 2, E vertex at (-1.0, 0.0) and level 2, E vertex at (1, -1) and level 2, E vertex at (0.0, 0.0) and level 2, E vertex at (1.0, 0.0) and level 2, E vertex at (0.0, -1.0) and level 2, I vertex at (-0.5, 0.5) and level 2, I vertex at (0.5, 0.5) and level 2, I vertex at (-0.5, -0.5) and level 2, I vertex at (0.5, -0.5) and level 2]"
        ]

        expected_nodes = [
            "e vertex at (0, 0) and level 0",
            "E vertex at (-1, 1) and level 1",
            "E vertex at (0.0, 1.0) and level 1",
            "E vertex at (1, 1) and level 1",
            "E vertex at (1.0, 0.0) and level 1",
            "E vertex at (1, -1) and level 1",
            "E vertex at (-1.0, 0.0) and level 1",
            "E vertex at (-1, -1) and level 1",
            "E vertex at (-1, 2) and level 1",
            "i vertex at (0.0, 0.0) and level 1",
            "E vertex at (-1, 1) and level 2",
            "E vertex at (0.0, 1.0) and level 2",
            "E vertex at (1, 1) and level 2",
            "E vertex at (1.0, 0.0) and level 2",
            "E vertex at (1, -1) and level 2",
            "E vertex at (0.0, -1.0) and level 2",
            "E vertex at (-1, -1) and level 2",
            "E vertex at (-1.0, 0.0) and level 2",
            "E vertex at (0.0, 0.0) and level 2",
            "I vertex at (-0.5, 0.5) and level 2",
            "I vertex at (0.5, 0.5) and level 2",
            "I vertex at (-0.5, -0.5) and level 2",
            "I vertex at (0.5, -0.5) and level 2"
        ]

        expected_edges = [
            ("E vertex at (-1, 1) and level 1", "E vertex at (0.0, 1.0) and level 1"),
            ("E vertex at (-1, 1) and level 1", "E vertex at (-1.0, 0.0) and level 1"),
            ("E vertex at (-1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
            ("E vertex at (0.0, 1.0) and level 1", "E vertex at (1, 1) and level 1"),
            ("E vertex at (1, 1) and level 1", "E vertex at (1.0, 0.0) and level 1"),
            ("E vertex at (1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
            ("E vertex at (1.0, 0.0) and level 1", "E vertex at (1, -1) and level 1"),
            ("E vertex at (1, -1) and level 1", "E vertex at (-1, -1) and level 1"),
            ("E vertex at (1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
            ("E vertex at (-1.0, 0.0) and level 1", "E vertex at (-1, -1) and level 1"),
            ("E vertex at (-1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
            ("i vertex at (0.0, 0.0) and level 1", "I vertex at (-0.5, 0.5) and level 2"),
            ("i vertex at (0.0, 0.0) and level 1", "I vertex at (0.5, 0.5) and level 2"),
            ("i vertex at (0.0, 0.0) and level 1", "I vertex at (0.5, -0.5) and level 2"),
            ("E vertex at (-1, 1) and level 2", "E vertex at (0.0, 1.0) and level 2"),
            ("E vertex at (-1, 1) and level 2", "E vertex at (-1.0, 0.0) and level 2"),
            ("E vertex at (-1, 1) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
            ("E vertex at (0.0, 1.0) and level 2", "E vertex at (1, 1) and level 2"),
            ("E vertex at (0.0, 1.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
            ("E vertex at (0.0, 1.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
            ("E vertex at (0.0, 1.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
            ("E vertex at (1, 1) and level 2", "E vertex at (1.0, 0.0) and level 2"),
            ("E vertex at (1, 1) and level 2", "I vertex at (0.5, 0.5) and level 2"),
            ("E vertex at (1.0, 0.0) and level 2", "E vertex at (1, -1) and level 2"),
            ("E vertex at (1.0, 0.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
            ("E vertex at (1.0, 0.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
            ("E vertex at (1.0, 0.0) and level 2", "I vertex at (0.5, -0.5) and level 2"),
            ("E vertex at (1, -1) and level 2", "E vertex at (0.0, -1.0) and level 2"),
            ("E vertex at (1, -1) and level 2", "I vertex at (0.5, -0.5) and level 2"),
            ("E vertex at (0.0, -1.0) and level 2", "E vertex at (-1, -1) and level 2"),
            ("E vertex at (0.0, -1.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
            ("E vertex at (0.0, -1.0) and level 2",
             "I vertex at (-0.5, -0.5) and level 2"),
            ("E vertex at (0.0, -1.0) and level 2", "I vertex at (0.5, -0.5) and level 2"),
            ("E vertex at (-1, -1) and level 2", "E vertex at (-1.0, 0.0) and level 2"),
            ("E vertex at (-1, -1) and level 2", "I vertex at (-0.5, -0.5) and level 2"),
            ("E vertex at (-1.0, 0.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
            ("E vertex at (-1.0, 0.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
            ("E vertex at (-1.0, 0.0) and level 2",
             "I vertex at (-0.5, -0.5) and level 2"),
            ("E vertex at (0.0, 0.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
            ("E vertex at (0.0, 0.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
            ("E vertex at (0.0, 0.0) and level 2", "I vertex at (-0.5, -0.5) and level 2"),
            ("E vertex at (0.0, 0.0) and level 2", "I vertex at (0.5, -0.5) and level 2")
        ]

        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))
        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        g = self.graph.P7(1)

        g.showLevel(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p7_new_edges(self):
        corners = self.graph.corners
        RHS = nx.Graph()
        RHS.add_node(v0 := Vertex((0, 0), "e", 0))
        RHS.add_node(v1 := Vertex(corners[0], "E", 1))

        RHS.add_node(v1_5 := Vertex(((corners[0][0] + corners[1][0]) / 2,
                                     (corners[0][1] + corners[1][1]) / 2), "E", 1))
        RHS.add_node(v2 := Vertex(corners[1], "E", 1))
        RHS.add_node(v2_5 := Vertex(((corners[1][0] + corners[2][0]) / 2,
                                     (corners[1][1] + corners[2][1]) / 2), "E", 1))
        RHS.add_node(v3 := Vertex(corners[2], "E", 1))
        RHS.add_node(v4_5 := Vertex(((corners[0][0] + corners[3][0]) / 2,
                                     (corners[0][1] + corners[3][1]) / 2), "E", 1))
        RHS.add_node(v4 := Vertex(corners[3], "E", 1))
        RHS.add_node(v6 := Vertex((1, 2), "E", 1))

        RHS.add_node(i := Vertex(((corners[0][0] + corners[1][0]) / 2,
                                  (corners[0][1] + corners[2][1]) / 2), "I", 1))
        RHS.add_edges_from([(v1, v1_5), (v1_5, v2), (v2, v2_5), (v2_5, v3), (v3, v4), (v1, v4_5), (v4, v4_5),
                            (v1, i), (v2, i), (v3, i), (v4, i), (v6, v1), (v6, v1_5)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append([v1, v1_5, v2, v2_5, v3, v4_5, v4, i, v6])  # appending RHS to first level
        self.graph.graph = RHS

        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (-1, 1) and level 1, E vertex at (0.0, 1.0) and level 1, E vertex at (1, 1) and level 1, E vertex at (1.0, 0.0) and level 1, E vertex at (1, -1) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (-1, -1) and level 1, i vertex at (0.0, 0.0) and level 1, E vertex at (1, 2) and level 1]",
            "[E vertex at (-1, 1) and level 2, E vertex at (0.0, 1.0) and level 2, E vertex at (1, 1) and level 2, E vertex at (-1, -1) and level 2, E vertex at (-1.0, 0.0) and level 2, E vertex at (1, -1) and level 2, E vertex at (0.0, 0.0) and level 2, E vertex at (1.0, 0.0) and level 2, E vertex at (0.0, -1.0) and level 2, I vertex at (-0.5, 0.5) and level 2, I vertex at (0.5, 0.5) and level 2, I vertex at (-0.5, -0.5) and level 2, I vertex at (0.5, -0.5) and level 2]"
        ]

        expected_nodes = ["e vertex at (0, 0) and level 0",
                          "E vertex at (-1, 1) and level 1",
                          "E vertex at (0.0, 1.0) and level 1",
                          "E vertex at (1, 1) and level 1",
                          "E vertex at (1.0, 0.0) and level 1",
                          "E vertex at (1, -1) and level 1",
                          "E vertex at (-1.0, 0.0) and level 1",
                          "E vertex at (-1, -1) and level 1",
                          "E vertex at (1, 2) and level 1",
                          "i vertex at (0.0, 0.0) and level 1",
                          "E vertex at (-1, 1) and level 2",
                          "E vertex at (0.0, 1.0) and level 2",
                          "E vertex at (1, 1) and level 2",
                          "E vertex at (1.0, 0.0) and level 2",
                          "E vertex at (1, -1) and level 2",
                          "E vertex at (0.0, -1.0) and level 2",
                          "E vertex at (-1, -1) and level 2",
                          "E vertex at (-1.0, 0.0) and level 2",
                          "E vertex at (0.0, 0.0) and level 2",
                          "I vertex at (-0.5, 0.5) and level 2",
                          "I vertex at (0.5, 0.5) and level 2",
                          "I vertex at (-0.5, -0.5) and level 2",
                          "I vertex at (0.5, -0.5) and level 2"]

        expected_edges = [("E vertex at (-1, 1) and level 1", "E vertex at (0.0, 1.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "E vertex at (-1.0, 0.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "E vertex at (1, 2) and level 1"),
                          ("E vertex at (0.0, 1.0) and level 1", "E vertex at (1, 1) and level 1"),
                          ("E vertex at (0.0, 1.0) and level 1", "E vertex at (1, 2) and level 1"),
                          ("E vertex at (1, 1) and level 1", "E vertex at (1.0, 0.0) and level 1"),
                          ("E vertex at (1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (1.0, 0.0) and level 1", "E vertex at (1, -1) and level 1"),
                          ("E vertex at (1, -1) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (-1.0, 0.0) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (-1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("i vertex at (0.0, 0.0) and level 1", "I vertex at (-0.5, 0.5) and level 2"),
                          ("i vertex at (0.0, 0.0) and level 1", "I vertex at (0.5, 0.5) and level 2"),
                          ("i vertex at (0.0, 0.0) and level 1", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (-1, 1) and level 2", "E vertex at (0.0, 1.0) and level 2"),
                          ("E vertex at (-1, 1) and level 2", "E vertex at (-1.0, 0.0) and level 2"),
                          ("E vertex at (-1, 1) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "E vertex at (1, 1) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (1, 1) and level 2", "E vertex at (1.0, 0.0) and level 2"),
                          ("E vertex at (1, 1) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "E vertex at (1, -1) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (1, -1) and level 2", "E vertex at (0.0, -1.0) and level 2"),
                          ("E vertex at (1, -1) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2", "E vertex at (-1, -1) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2",
                           "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (-1, -1) and level 2", "E vertex at (-1.0, 0.0) and level 2"),
                          ("E vertex at (-1, -1) and level 2", "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2",
                           "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (0.5, -0.5) and level 2")]

        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))
        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        g = self.graph.P7(1)

        g.showLevel(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p7_without_vertex(self):
        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (-1, 1) and level 1, E vertex at (0.0, 1.0) and level 1, E vertex at (1, 1) and level 1, E vertex at (1.0, 0.0) and level 1, E vertex at (1, -1) and level 1, E vertex at (-1, -1) and level 1, I vertex at (0.0, 0.0) and level 1, E vertex at (-1, 2) and level 1]"
        ]

        expected_nodes = ["e vertex at (0, 0) and level 0",
                          "E vertex at (-1, 1) and level 1",
                          "E vertex at (0.0, 1.0) and level 1",
                          "E vertex at (1, 1) and level 1",
                          "E vertex at (1.0, 0.0) and level 1",
                          "E vertex at (1, -1) and level 1",
                          "E vertex at (-1, -1) and level 1",
                          "E vertex at (-1, 2) and level 1",
                          "I vertex at (0.0, 0.0) and level 1"]

        expected_edges = [("E vertex at (-1, 1) and level 1", "E vertex at (0.0, 1.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "I vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (0.0, 1.0) and level 1", "E vertex at (1, 1) and level 1"),
                          ("E vertex at (1, 1) and level 1", "E vertex at (1.0, 0.0) and level 1"),
                          ("E vertex at (1, 1) and level 1", "I vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (1.0, 0.0) and level 1", "E vertex at (1, -1) and level 1"),
                          ("E vertex at (1, -1) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (1, -1) and level 1", "I vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (-1, -1) and level 1", "I vertex at (0.0, 0.0) and level 1")]

        corners = self.graph.corners
        RHS = nx.Graph()
        RHS.add_node(v0 := Vertex((0, 0), "e", 0))
        RHS.add_node(v1 := Vertex(corners[0], "E", 1))

        RHS.add_node(v1_5 := Vertex(((corners[0][0] + corners[1][0]) / 2,
                                     (corners[0][1] + corners[1][1]) / 2), "E", 1))
        RHS.add_node(v2 := Vertex(corners[1], "E", 1))
        RHS.add_node(v2_5 := Vertex(((corners[1][0] + corners[2][0]) / 2,
                                     (corners[1][1] + corners[2][1]) / 2), "E", 1))
        RHS.add_node(v3 := Vertex(corners[2], "E", 1))
        RHS.add_node(v4_5 := Vertex(((corners[0][0] + corners[3][0]) / 2,
                                     (corners[0][1] + corners[3][1]) / 2), "E", 1))
        RHS.add_node(v4 := Vertex(corners[3], "E", 1))
        RHS.add_node(v6 := Vertex((-1, 2), "E", 1))

        RHS.add_node(i := Vertex(((corners[0][0] + corners[1][0]) / 2,
                                  (corners[0][1] + corners[2][1]) / 2), "I", 1))
        RHS.add_edges_from([(v1, v1_5), (v1_5, v2), (v2, v2_5), (v2_5, v3), (v3, v4), (v1, v4_5), (v4_5, v1),
                            (v1, i), (v2, i), (v3, i), (v4, i)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append([v1, v1_5, v2, v2_5, v3, v4, i, v6])  # appending RHS to first level
        self.graph.graph = RHS

        g = self.graph.P7(0)

        g.showLevel(1)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p7_changed_label(self):
        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (-1, 1) and level 1, E vertex at (0.0, 1.0) and level 1, E vertex at (1, 1) and level 1, E vertex at (1.0, 0.0) and level 1, E vertex at (1, -1) and level 1, E vertex at (-1, -1) and level 1, E vertex at (0.0, 0.0) and level 1]"
        ]

        expected_nodes = ["e vertex at (0, 0) and level 0",
                          "E vertex at (-1, 1) and level 1",
                          "E vertex at (0.0, 1.0) and level 1",
                          "E vertex at (1, 1) and level 1",
                          "E vertex at (1.0, 0.0) and level 1",
                          "E vertex at (1, -1) and level 1",
                          "E vertex at (-1.0, 0.0) and level 1",
                          "E vertex at (-1, -1) and level 1",
                          "E vertex at (0.0, 0.0) and level 1"
                          ]

        expected_edges = [
            ("E vertex at (-1, 1) and level 1", "E vertex at (0.0, 1.0) and level 1"),
            ("E vertex at (-1, 1) and level 1", "E vertex at (-1.0, 0.0) and level 1"),
            ("E vertex at (-1, 1) and level 1", "E vertex at (0.0, 0.0) and level 1"),
            ("E vertex at (0.0, 1.0) and level 1", "E vertex at (1, 1) and level 1"),
            ("E vertex at (1, 1) and level 1", "E vertex at (1.0, 0.0) and level 1"),
            ("E vertex at (1, 1) and level 1", "E vertex at (0.0, 0.0) and level 1"),
            ("E vertex at (1.0, 0.0) and level 1", "E vertex at (1, -1) and level 1"),
            ("E vertex at (1, -1) and level 1", "E vertex at (-1, -1) and level 1"),
            ("E vertex at (1, -1) and level 1", "E vertex at (0.0, 0.0) and level 1"),
            ("E vertex at (-1.0, 0.0) and level 1", "E vertex at (-1, -1) and level 1"),
            ("E vertex at (-1, -1) and level 1", "E vertex at (0.0, 0.0) and level 1")
        ]

        corners = self.graph.corners
        RHS = nx.Graph()
        RHS.add_node(v0 := Vertex((0, 0), "e", 0))
        RHS.add_node(v1 := Vertex(corners[0], "E", 1))

        RHS.add_node(v1_5 := Vertex(((corners[0][0] + corners[1][0]) / 2,
                                     (corners[0][1] + corners[1][1]) / 2), "E", 1))
        RHS.add_node(v2 := Vertex(corners[1], "E", 1))
        RHS.add_node(v2_5 := Vertex(((corners[1][0] + corners[2][0]) / 2,
                                     (corners[1][1] + corners[2][1]) / 2), "E", 1))
        RHS.add_node(v3 := Vertex(corners[2], "E", 1))
        RHS.add_node(v4_5 := Vertex(((corners[0][0] + corners[3][0]) / 2,
                                     (corners[0][1] + corners[3][1]) / 2), "E", 1))
        RHS.add_node(v4 := Vertex(corners[3], "E", 1))

        RHS.add_node(i := Vertex(((corners[0][0] + corners[1][0]) / 2,
                                  (corners[0][1] + corners[2][1]) / 2), "E", 1))  # changed label
        RHS.add_edges_from([(v1, v1_5), (v1_5, v2), (v2, v2_5), (v2_5, v3), (v3, v4), (v1, v4_5), (v4_5, v4),
                            (v1, i), (v2, i), (v3, i), (v4, i)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append([v1, v1_5, v2, v2_5, v3, v4, i])  # appending RHS to first level
        self.graph.graph = RHS

        g = self.graph.P7(0)

        g.showLevel(1)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p7_not_on_middle(self):
        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (-1, 1) and level 1, E vertex at (0.5, 1.5) and level 1, E vertex at (1, 1) and level 1, E vertex at (1.0, 0.0) and level 1, E vertex at (1, -1) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (-1, -1) and level 1, i vertex at (0.0, 0.0) and level 1]",
        ]

        expected_nodes = ["e vertex at (0, 0) and level 0",
                          "E vertex at (-1, 1) and level 1",
                          "E vertex at (0.5, 1.5) and level 1",
                          "E vertex at (1, 1) and level 1",
                          "E vertex at (1.0, 0.0) and level 1",
                          "E vertex at (1, -1) and level 1",
                          "E vertex at (-1.0, 0.0) and level 1",
                          "E vertex at (-1, -1) and level 1",
                          "i vertex at (0.0, 0.0) and level 1",
                          ]

        expected_edges = [("E vertex at (-1, 1) and level 1", "E vertex at (0.5, 1.5) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "E vertex at (-1.0, 0.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (0.5, 1.5) and level 1", "E vertex at (1, 1) and level 1"),
                          ("E vertex at (1, 1) and level 1", "E vertex at (1.0, 0.0) and level 1"),
                          ("E vertex at (1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (1.0, 0.0) and level 1", "E vertex at (1, -1) and level 1"),
                          ("E vertex at (1, -1) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (-1.0, 0.0) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (-1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ]

        corners = self.graph.corners

        RHS = nx.Graph()
        RHS.add_node(v0 := Vertex((0, 0), "e", 0))
        RHS.add_node(v1 := Vertex(corners[0], "E", 1))

        RHS.add_node(v1_5 := Vertex(((corners[0][0] + corners[1][0]) / 2 + 0.5,
                                     (corners[0][1] + corners[1][1]) / 2 + 0.5), "E", 1))
        RHS.add_node(v2 := Vertex(corners[1], "E", 1))
        RHS.add_node(v2_5 := Vertex(((corners[1][0] + corners[2][0]) / 2,
                                     (corners[1][1] + corners[2][1]) / 2), "E", 1))
        RHS.add_node(v3 := Vertex(corners[2], "E", 1))
        RHS.add_node(v4_5 := Vertex(((corners[0][0] + corners[3][0]) / 2,
                                     (corners[0][1] + corners[3][1]) / 2), "E", 1))
        RHS.add_node(v4 := Vertex(corners[3], "E", 1))

        RHS.add_node(i := Vertex(((corners[0][0] + corners[2][0]) / 2,
                                  (corners[0][1] + corners[2][1]) / 2), "I", 1))
        RHS.add_edges_from([(v1, v1_5), (v1_5, v2), (v2, v2_5), (v2_5, v3), (v3, v4), (v1, v4_5), (v4, v4_5),
                            (v1, i), (v2, i), (v3, i), (v4, i)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append([v1, v1_5, v2, v2_5, v3, v4_5, v4, i])  # appending RHS to first level
        self.graph.graph = RHS

        g = self.graph.P7(0)

        g.showLevel(1)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p8(self):
        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (-1, 1) and level 1, E vertex at (0.0, 1.0) and level 1, E vertex at (1, 1) and level 1, E vertex at (1.0, 0.0) and level 1, E vertex at (1, -1) and level 1, E vertex at (0.0, -1.0) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (-1, -1) and level 1, i vertex at (0.0, 0.0) and level 1]",
            "[E vertex at (-1, 1) and level 2, E vertex at (-1.0, 0.0) and level 2, E vertex at (-1, -1) and level 2, E vertex at (1, 1) and level 2, E vertex at (0.0, 1.0) and level 2, E vertex at (1, -1) and level 2, E vertex at (0.0, 0.0) and level 2, E vertex at (0.0, -1.0) and level 2, E vertex at (1.0, 0.0) and level 2, I vertex at (-0.5, 0.5) and level 2, I vertex at (-0.5, -0.5) and level 2, I vertex at (0.5, 0.5) and level 2, I vertex at (0.5, -0.5) and level 2]"
        ]

        expected_nodes = ["e vertex at (0, 0) and level 0",
                          "E vertex at (-1, 1) and level 1",
                          "E vertex at (0.0, 1.0) and level 1",
                          "E vertex at (1, 1) and level 1",
                          "E vertex at (1.0, 0.0) and level 1",
                          "E vertex at (1, -1) and level 1",
                          "E vertex at (0.0, -1.0) and level 1",
                          "E vertex at (-1.0, 0.0) and level 1",
                          "E vertex at (-1, -1) and level 1",
                          "i vertex at (0.0, 0.0) and level 1",
                          "E vertex at (-1, 1) and level 2",
                          "E vertex at (-1.0, 0.0) and level 2",
                          "E vertex at (-1, -1) and level 2",
                          "E vertex at (0.0, -1.0) and level 2",
                          "E vertex at (1, -1) and level 2",
                          "E vertex at (1.0, 0.0) and level 2",
                          "E vertex at (1, 1) and level 2",
                          "E vertex at (0.0, 1.0) and level 2",
                          "E vertex at (0.0, 0.0) and level 2",
                          "I vertex at (-0.5, 0.5) and level 2",
                          "I vertex at (-0.5, -0.5) and level 2",
                          "I vertex at (0.5, 0.5) and level 2",
                          "I vertex at (0.5, -0.5) and level 2"]

        expected_edges = [("E vertex at (-1, 1) and level 1", "E vertex at (0.0, 1.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "E vertex at (-1.0, 0.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (0.0, 1.0) and level 1", "E vertex at (1, 1) and level 1"),
                          ("E vertex at (1, 1) and level 1", "E vertex at (1.0, 0.0) and level 1"),
                          ("E vertex at (1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (1.0, 0.0) and level 1", "E vertex at (1, -1) and level 1"),
                          ("E vertex at (1, -1) and level 1", "E vertex at (0.0, -1.0) and level 1"),
                          ("E vertex at (1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (0.0, -1.0) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (-1.0, 0.0) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (-1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("i vertex at (0.0, 0.0) and level 1", "I vertex at (-0.5, 0.5) and level 2"),
                          ("i vertex at (0.0, 0.0) and level 1", "I vertex at (-0.5, -0.5) and level 2"),
                          ("i vertex at (0.0, 0.0) and level 1", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (-1, 1) and level 2", "E vertex at (-1.0, 0.0) and level 2"),
                          ("E vertex at (-1, 1) and level 2", "E vertex at (0.0, 1.0) and level 2"),
                          ("E vertex at (-1, 1) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2", "E vertex at (-1, -1) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2",
                           "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (-1, -1) and level 2", "E vertex at (0.0, -1.0) and level 2"),
                          ("E vertex at (-1, -1) and level 2", "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2", "E vertex at (1, -1) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2",
                           "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (1, -1) and level 2", "E vertex at (1.0, 0.0) and level 2"),
                          ("E vertex at (1, -1) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "E vertex at (1, 1) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (1, 1) and level 2", "E vertex at (0.0, 1.0) and level 2"),
                          ("E vertex at (1, 1) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (0.5, -0.5) and level 2")]
        P8RHS(self.graph)

        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))
        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        g = self.graph.P8(1)

        g.showLevel(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p8_new_vertex(self):
        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (-1, 1) and level 1, E vertex at (0.0, 1.0) and level 1, E vertex at (1, 1) and level 1, E vertex at (1.0, 0.0) and level 1, E vertex at (1, -1) and level 1, E vertex at (0.0, -1.0) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (-1, -1) and level 1, E vertex at (-1, 2) and level 1, i vertex at (0.0, 0.0) and level 1]",
            "[E vertex at (-1, 1) and level 2, E vertex at (-1.0, 0.0) and level 2, E vertex at (-1, -1) and level 2, E vertex at (1, 1) and level 2, E vertex at (0.0, 1.0) and level 2, E vertex at (1, -1) and level 2, E vertex at (0.0, 0.0) and level 2, E vertex at (0.0, -1.0) and level 2, E vertex at (1.0, 0.0) and level 2, I vertex at (-0.5, 0.5) and level 2, I vertex at (-0.5, -0.5) and level 2, I vertex at (0.5, 0.5) and level 2, I vertex at (0.5, -0.5) and level 2]"
        ]

        expected_nodes = ['e vertex at (0, 0) and level 0',
                          'E vertex at (-1, 1) and level 1',
                          'E vertex at (0.0, 1.0) and level 1',
                          'E vertex at (1, 1) and level 1',
                          'E vertex at (1.0, 0.0) and level 1',
                          'E vertex at (1, -1) and level 1',
                          'E vertex at (0.0, -1.0) and level 1',
                          'E vertex at (-1.0, 0.0) and level 1',
                          'E vertex at (-1, -1) and level 1',
                          'E vertex at (-1, 2) and level 1',
                          'i vertex at (0.0, 0.0) and level 1',
                          'E vertex at (-1, 1) and level 2',
                          'E vertex at (-1.0, 0.0) and level 2',
                          'E vertex at (-1, -1) and level 2',
                          'E vertex at (0.0, -1.0) and level 2',
                          'E vertex at (1, -1) and level 2',
                          'E vertex at (1.0, 0.0) and level 2',
                          'E vertex at (1, 1) and level 2',
                          'E vertex at (0.0, 1.0) and level 2',
                          'E vertex at (0.0, 0.0) and level 2',
                          'I vertex at (-0.5, 0.5) and level 2',
                          'I vertex at (-0.5, -0.5) and level 2',
                          'I vertex at (0.5, 0.5) and level 2',
                          'I vertex at (0.5, -0.5) and level 2']

        expected_edges = [("E vertex at (-1, 1) and level 1", "E vertex at (0.0, 1.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "E vertex at (-1.0, 0.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (0.0, 1.0) and level 1", "E vertex at (1, 1) and level 1"),
                          ("E vertex at (1, 1) and level 1", "E vertex at (1.0, 0.0) and level 1"),
                          ("E vertex at (1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (1.0, 0.0) and level 1", "E vertex at (1, -1) and level 1"),
                          ("E vertex at (1, -1) and level 1", "E vertex at (0.0, -1.0) and level 1"),
                          ("E vertex at (1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (0.0, -1.0) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (-1.0, 0.0) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (-1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("i vertex at (0.0, 0.0) and level 1", "I vertex at (-0.5, 0.5) and level 2"),
                          ("i vertex at (0.0, 0.0) and level 1", "I vertex at (-0.5, -0.5) and level 2"),
                          ("i vertex at (0.0, 0.0) and level 1", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (-1, 1) and level 2", "E vertex at (-1.0, 0.0) and level 2"),
                          ("E vertex at (-1, 1) and level 2", "E vertex at (0.0, 1.0) and level 2"),
                          ("E vertex at (-1, 1) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2", "E vertex at (-1, -1) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (-1.0, 0.0) and level 2",
                           "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (-1, -1) and level 2", "E vertex at (0.0, -1.0) and level 2"),
                          ("E vertex at (-1, -1) and level 2", "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2", "E vertex at (1, -1) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2",
                           "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, -1.0) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (1, -1) and level 2", "E vertex at (1.0, 0.0) and level 2"),
                          ("E vertex at (1, -1) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "E vertex at (1, 1) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (1.0, 0.0) and level 2", "I vertex at (0.5, -0.5) and level 2"),
                          ("E vertex at (1, 1) and level 2", "E vertex at (0.0, 1.0) and level 2"),
                          ("E vertex at (1, 1) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 1.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (-0.5, -0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
                          ("E vertex at (0.0, 0.0) and level 2", "I vertex at (0.5, -0.5) and level 2")]
        corners = self.graph.corners
        RHS = nx.Graph()

        RHS.add_node(v0 := Vertex((0, 0), "e", 0))
        RHS.add_node(v1 := Vertex(corners[0], "E", 1))
        RHS.add_node(v1_5 := Vertex(((corners[0][0] + corners[1][0]) / 2,
                                     (corners[0][1] + corners[1][1]) / 2), "E", 1))
        RHS.add_node(v2 := Vertex(corners[1], "E", 1))
        RHS.add_node(v2_5 := Vertex(((corners[1][0] + corners[2][0]) / 2,
                                     (corners[1][1] + corners[2][1]) / 2), "E", 1))
        RHS.add_node(v3 := Vertex(corners[2], "E", 1))
        RHS.add_node(v3_5 := Vertex(((corners[2][0] + corners[3][0]) / 2,
                                     (corners[2][1] + corners[3][1]) / 2), "E", 1))

        RHS.add_node(v4_5 := Vertex(((corners[0][0] + corners[3][0]) / 2,
                                     (corners[0][1] + corners[3][1]) / 2), "E", 1))
        RHS.add_node(v4 := Vertex(corners[3], "E", 1))
        RHS.add_node(v6 := Vertex((-1, 2), "E", 1))

        RHS.add_node(i := Vertex(((corners[0][0] + corners[2][0]) / 2,
                                  (corners[0][1] + corners[2][1]) / 2), "I", 1))
        RHS.add_edges_from(
            [(v1, v1_5), (v1_5, v2), (v2, v2_5), (v2_5, v3), (v3, v3_5), (v3_5, v4), (v1, v4_5), (v4, v4_5),
             (v1, i), (v2, i), (v3, i), (v4, i)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append([v1, v1_5, v2, v2_5, v3, v3_5, v4_5, v4, v6, i])  # appending RHS to first level
        self.graph.graph = RHS

        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))
        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        g = self.graph.P8(1)

        g.showLevel(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p8_new_edges(self):
        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (-1, 1) and level 1, E vertex at (0.0, 1.0) and level 1, E vertex at (1, 1) and level 1, E vertex at (1.0, 0.0) and level 1, E vertex at (1, -1) and level 1, E vertex at (0.0, -1.0) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (-1, -1) and level 1, E vertex at (-1, 2) and level 1, i vertex at (0.0, 0.0) and level 1]",
            "[E vertex at (-1, 1) and level 2, E vertex at (-1.0, 0.0) and level 2, E vertex at (-1, -1) and level 2, E vertex at (1, 1) and level 2, E vertex at (0.0, 1.0) and level 2, E vertex at (1, -1) and level 2, E vertex at (0.0, 0.0) and level 2, E vertex at (0.0, -1.0) and level 2, E vertex at (1.0, 0.0) and level 2, I vertex at (-0.5, 0.5) and level 2, I vertex at (-0.5, -0.5) and level 2, I vertex at (0.5, 0.5) and level 2, I vertex at (0.5, -0.5) and level 2]"
        ]

        expected_nodes = ['e vertex at (0, 0) and level 0',
                          'E vertex at (-1, 1) and level 1',
                          'E vertex at (0.0, 1.0) and level 1',
                          'E vertex at (1, 1) and level 1',
                          'E vertex at (1.0, 0.0) and level 1',
                          'E vertex at (1, -1) and level 1',
                          'E vertex at (0.0, -1.0) and level 1',
                          'E vertex at (-1.0, 0.0) and level 1',
                          'E vertex at (-1, -1) and level 1',
                          'E vertex at (-1, 2) and level 1',
                          'i vertex at (0.0, 0.0) and level 1',
                          'E vertex at (-1, 1) and level 2',
                          'E vertex at (-1.0, 0.0) and level 2',
                          'E vertex at (-1, -1) and level 2',
                          'E vertex at (0.0, -1.0) and level 2',
                          'E vertex at (1, -1) and level 2',
                          'E vertex at (1.0, 0.0) and level 2',
                          'E vertex at (1, 1) and level 2',
                          'E vertex at (0.0, 1.0) and level 2',
                          'E vertex at (0.0, 0.0) and level 2',
                          'I vertex at (-0.5, 0.5) and level 2',
                          'I vertex at (-0.5, -0.5) and level 2',
                          'I vertex at (0.5, 0.5) and level 2',
                          'I vertex at (0.5, -0.5) and level 2']

        expected_edges = [('E vertex at (-1, 1) and level 1', 'E vertex at (0.0, 1.0) and level 1'),
                          ('E vertex at (-1, 1) and level 1', 'E vertex at (-1.0, 0.0) and level 1'),
                          ('E vertex at (-1, 1) and level 1', 'E vertex at (-1, 2) and level 1'),
                          ('E vertex at (-1, 1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (0.0, 1.0) and level 1', 'E vertex at (1, 1) and level 1'),
                          ('E vertex at (0.0, 1.0) and level 1', 'E vertex at (-1, 2) and level 1'),
                          ('E vertex at (1, 1) and level 1', 'E vertex at (1.0, 0.0) and level 1'),
                          ('E vertex at (1, 1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (1.0, 0.0) and level 1', 'E vertex at (1, -1) and level 1'),
                          ('E vertex at (1, -1) and level 1', 'E vertex at (0.0, -1.0) and level 1'),
                          ('E vertex at (1, -1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (0.0, -1.0) and level 1', 'E vertex at (-1, -1) and level 1'),
                          ('E vertex at (-1.0, 0.0) and level 1', 'E vertex at (-1, -1) and level 1'),
                          ('E vertex at (-1, -1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
                          ('i vertex at (0.0, 0.0) and level 1', 'I vertex at (-0.5, 0.5) and level 2'),
                          ('i vertex at (0.0, 0.0) and level 1', 'I vertex at (-0.5, -0.5) and level 2'),
                          ('i vertex at (0.0, 0.0) and level 1', 'I vertex at (0.5, -0.5) and level 2'),
                          ('E vertex at (-1, 1) and level 2', 'E vertex at (-1.0, 0.0) and level 2'),
                          ('E vertex at (-1, 1) and level 2', 'E vertex at (0.0, 1.0) and level 2'),
                          ('E vertex at (-1, 1) and level 2', 'I vertex at (-0.5, 0.5) and level 2'),
                          ('E vertex at (-1.0, 0.0) and level 2', 'E vertex at (-1, -1) and level 2'),
                          ('E vertex at (-1.0, 0.0) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
                          ('E vertex at (-1.0, 0.0) and level 2', 'I vertex at (-0.5, 0.5) and level 2'),
                          ('E vertex at (-1.0, 0.0) and level 2',
                           'I vertex at (-0.5, -0.5) and level 2'),
                          ('E vertex at (-1, -1) and level 2', 'E vertex at (0.0, -1.0) and level 2'),
                          ('E vertex at (-1, -1) and level 2', 'I vertex at (-0.5, -0.5) and level 2'),
                          ('E vertex at (0.0, -1.0) and level 2', 'E vertex at (1, -1) and level 2'),
                          ('E vertex at (0.0, -1.0) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
                          ('E vertex at (0.0, -1.0) and level 2',
                           'I vertex at (-0.5, -0.5) and level 2'),
                          ('E vertex at (0.0, -1.0) and level 2', 'I vertex at (0.5, -0.5) and level 2'),
                          ('E vertex at (1, -1) and level 2', 'E vertex at (1.0, 0.0) and level 2'),
                          ('E vertex at (1, -1) and level 2', 'I vertex at (0.5, -0.5) and level 2'),
                          ('E vertex at (1.0, 0.0) and level 2', 'E vertex at (1, 1) and level 2'),
                          ('E vertex at (1.0, 0.0) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
                          ('E vertex at (1.0, 0.0) and level 2', 'I vertex at (0.5, 0.5) and level 2'),
                          ('E vertex at (1.0, 0.0) and level 2', 'I vertex at (0.5, -0.5) and level 2'),
                          ('E vertex at (1, 1) and level 2', 'E vertex at (0.0, 1.0) and level 2'),
                          ('E vertex at (1, 1) and level 2', 'I vertex at (0.5, 0.5) and level 2'),
                          ('E vertex at (0.0, 1.0) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
                          ('E vertex at (0.0, 1.0) and level 2', 'I vertex at (-0.5, 0.5) and level 2'),
                          ('E vertex at (0.0, 1.0) and level 2', 'I vertex at (0.5, 0.5) and level 2'),
                          ('E vertex at (0.0, 0.0) and level 2', 'I vertex at (-0.5, 0.5) and level 2'),
                          ('E vertex at (0.0, 0.0) and level 2', 'I vertex at (-0.5, -0.5) and level 2'),
                          ('E vertex at (0.0, 0.0) and level 2', 'I vertex at (0.5, 0.5) and level 2'),
                          ('E vertex at (0.0, 0.0) and level 2', 'I vertex at (0.5, -0.5) and level 2')]
        corners = self.graph.corners
        RHS = nx.Graph()

        RHS.add_node(v0 := Vertex((0, 0), "e", 0))
        RHS.add_node(v1 := Vertex(corners[0], "E", 1))
        RHS.add_node(v1_5 := Vertex(((corners[0][0] + corners[1][0]) / 2,
                                     (corners[0][1] + corners[1][1]) / 2), "E", 1))
        RHS.add_node(v2 := Vertex(corners[1], "E", 1))
        RHS.add_node(v2_5 := Vertex(((corners[1][0] + corners[2][0]) / 2,
                                     (corners[1][1] + corners[2][1]) / 2), "E", 1))
        RHS.add_node(v3 := Vertex(corners[2], "E", 1))
        RHS.add_node(v3_5 := Vertex(((corners[2][0] + corners[3][0]) / 2,
                                     (corners[2][1] + corners[3][1]) / 2), "E", 1))

        RHS.add_node(v4_5 := Vertex(((corners[0][0] + corners[3][0]) / 2,
                                     (corners[0][1] + corners[3][1]) / 2), "E", 1))
        RHS.add_node(v4 := Vertex(corners[3], "E", 1))
        RHS.add_node(v6 := Vertex((-1, 2), "E", 1))

        RHS.add_node(i := Vertex(((corners[0][0] + corners[2][0]) / 2,
                                  (corners[0][1] + corners[2][1]) / 2), "I", 1))
        RHS.add_edges_from(
            [(v1, v1_5), (v1_5, v2), (v2, v2_5), (v2_5, v3), (v3, v3_5), (v3_5, v4), (v1, v4_5), (v4, v4_5), (v1, v6),
             (v6, v1_5),
             (v1, i), (v2, i), (v3, i), (v4, i)])

        self.graph.tiers[0] = [v0]
        self.graph.tiers.append([v1, v1_5, v2, v2_5, v3, v3_5, v4_5, v4, v6, i])  # appending RHS to first level
        self.graph.graph = RHS

        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))
        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        g = self.graph.P8(1)

        g.showLevel(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p8_without_vertex(self):
        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (-1, 1) and level 1, E vertex at (0.0, 1.0) and level 1, E vertex at (1, 1) and level 1, E vertex at (1.0, 0.0) and level 1, E vertex at (1, -1) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (-1, -1) and level 1, I vertex at (0.0, 0.0) and level 1]",
        ]

        expected_nodes = ["e vertex at (0, 0) and level 0",
                          "E vertex at (-1, 1) and level 1",
                          "E vertex at (0.0, 1.0) and level 1",
                          "E vertex at (1, 1) and level 1",
                          "E vertex at (1.0, 0.0) and level 1",
                          "E vertex at (1, -1) and level 1",
                          "E vertex at (-1.0, 0.0) and level 1",
                          "E vertex at (-1, -1) and level 1",
                          "I vertex at (0.0, 0.0) and level 1",
                          ]

        expected_edges = [("E vertex at (-1, 1) and level 1", "E vertex at (0.0, 1.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "E vertex at (-1.0, 0.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "I vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (0.0, 1.0) and level 1", "E vertex at (1, 1) and level 1"),
                          ("E vertex at (1, 1) and level 1", "E vertex at (1.0, 0.0) and level 1"),
                          ("E vertex at (1, 1) and level 1", "I vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (1.0, 0.0) and level 1", "E vertex at (1, -1) and level 1"),
                          ("E vertex at (1, -1) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (1, -1) and level 1", "I vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (-1.0, 0.0) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (-1, -1) and level 1", "I vertex at (0.0, 0.0) and level 1"),
                          ]
        P7RHS(self.graph, rotation=0)

        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))
        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        g = self.graph.P8(1)

        self.graph.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p8_without_edge(self):
        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (-1, 1) and level 1, E vertex at (0.0, 1.0) and level 1, E vertex at (1, 1) and level 1, E vertex at (1.0, 0.0) and level 1, E vertex at (1, -1) and level 1, E vertex at (0.0, -1.0) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (-1, -1) and level 1, I vertex at (0.0, 0.0) and level 1]"
        ]
        expected_nodes = ['e vertex at (0, 0) and level 0',
                          'E vertex at (-1, 1) and level 1',
                          'E vertex at (0.0, 1.0) and level 1',
                          'E vertex at (1, 1) and level 1',
                          'E vertex at (1.0, 0.0) and level 1',
                          'E vertex at (1, -1) and level 1',
                          'E vertex at (0.0, -1.0) and level 1',
                          'E vertex at (-1.0, 0.0) and level 1',
                          'E vertex at (-1, -1) and level 1',
                          'I vertex at (0.0, 0.0) and level 1',
                          ]

        expected_edges = [("E vertex at (-1, 1) and level 1", "E vertex at (0.0, 1.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "E vertex at (-1.0, 0.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "I vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (0.0, 1.0) and level 1", "E vertex at (1, 1) and level 1"),
                          ("E vertex at (1, 1) and level 1", "E vertex at (1.0, 0.0) and level 1"),
                          ("E vertex at (1, 1) and level 1", "I vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (1.0, 0.0) and level 1", "E vertex at (1, -1) and level 1"),
                          ("E vertex at (1, -1) and level 1", "E vertex at (0.0, -1.0) and level 1"),
                          ("E vertex at (1, -1) and level 1", "I vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (0.0, -1.0) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (-1.0, 0.0) and level 1", "E vertex at (-1, -1) and level 1"),
                          ]
        corners = self.graph.corners
        RHS = nx.Graph()

        RHS.add_node(v0 := Vertex((0, 0), "e", 0))
        RHS.add_node(v1 := Vertex(corners[0], "E", 1))
        RHS.add_node(v1_5 := Vertex(((corners[0][0] + corners[1][0]) / 2,
                                     (corners[0][1] + corners[1][1]) / 2), "E", 1))
        RHS.add_node(v2 := Vertex(corners[1], "E", 1))
        RHS.add_node(v2_5 := Vertex(((corners[1][0] + corners[2][0]) / 2,
                                     (corners[1][1] + corners[2][1]) / 2), "E", 1))
        RHS.add_node(v3 := Vertex(corners[2], "E", 1))
        RHS.add_node(v3_5 := Vertex(((corners[2][0] + corners[3][0]) / 2,
                                     (corners[2][1] + corners[3][1]) / 2), "E", 1))

        RHS.add_node(v4_5 := Vertex(((corners[0][0] + corners[3][0]) / 2,
                                     (corners[0][1] + corners[3][1]) / 2), "E", 1))
        RHS.add_node(v4 := Vertex(corners[3], "E", 1))

        RHS.add_node(i := Vertex(((corners[0][0] + corners[2][0]) / 2,
                                  (corners[0][1] + corners[2][1]) / 2), "I", 1))
        RHS.add_edges_from(
            [(v1, v1_5), (v1_5, v2), (v2, v2_5), (v2_5, v3), (v3, v3_5), (v3_5, v4), (v1, v4_5), (v4, v4_5),
             (v1, i), (v2, i), (v3, i)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append([v1, v1_5, v2, v2_5, v3, v3_5, v4_5, v4, i])  # appending RHS to first level
        self.graph.graph = RHS

        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))
        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        g = self.graph.P8(1)

        self.graph.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p8_changed_label(self):
        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (-1, 1) and level 1, E vertex at (0.0, 1.0) and level 1, E vertex at (1, 1) and level 1, E vertex at (1.0, 0.0) and level 1, E vertex at (1, -1) and level 1, E vertex at (0.0, -1.0) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (-1, -1) and level 1, E vertex at (0.0, 0.0) and level 1]",
        ]

        expected_nodes = ["e vertex at (0, 0) and level 0",
                          "E vertex at (-1, 1) and level 1",
                          "E vertex at (0.0, 1.0) and level 1",
                          "E vertex at (1, 1) and level 1",
                          "E vertex at (1.0, 0.0) and level 1",
                          "E vertex at (1, -1) and level 1",
                          "E vertex at (0.0, -1.0) and level 1",
                          "E vertex at (-1.0, 0.0) and level 1",
                          "E vertex at (-1, -1) and level 1",
                          "E vertex at (0.0, 0.0) and level 1",
                          ]

        expected_edges = [("E vertex at (-1, 1) and level 1", "E vertex at (0.0, 1.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "E vertex at (-1.0, 0.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "E vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (0.0, 1.0) and level 1", "E vertex at (1, 1) and level 1"),
                          ("E vertex at (1, 1) and level 1", "E vertex at (1.0, 0.0) and level 1"),
                          ("E vertex at (1, 1) and level 1", "E vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (1.0, 0.0) and level 1", "E vertex at (1, -1) and level 1"),
                          ("E vertex at (1, -1) and level 1", "E vertex at (0.0, -1.0) and level 1"),
                          ("E vertex at (1, -1) and level 1", "E vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (0.0, -1.0) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (-1.0, 0.0) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (-1, -1) and level 1", "E vertex at (0.0, 0.0) and level 1"),
                          ]

        corners = self.graph.corners
        RHS = nx.Graph()

        RHS.add_node(v0 := Vertex((0, 0), "e", 0))
        RHS.add_node(v1 := Vertex(corners[0], "E", 1))

        RHS.add_node(v1_5 := Vertex(((corners[0][0] + corners[1][0]) / 2,
                                     (corners[0][1] + corners[1][1]) / 2), "E", 1))
        RHS.add_node(v2 := Vertex(corners[1], "E", 1))
        RHS.add_node(v2_5 := Vertex(((corners[1][0] + corners[2][0]) / 2,
                                     (corners[1][1] + corners[2][1]) / 2), "E", 1))
        RHS.add_node(v3 := Vertex(corners[2], "E", 1))
        RHS.add_node(v3_5 := Vertex(((corners[2][0] + corners[3][0]) / 2,
                                     (corners[2][1] + corners[3][1]) / 2), "E", 1))

        RHS.add_node(v4_5 := Vertex(((corners[0][0] + corners[3][0]) / 2,
                                     (corners[0][1] + corners[3][1]) / 2), "E", 1))
        RHS.add_node(v4 := Vertex(corners[3], "E", 1))

        RHS.add_node(i := Vertex(((corners[0][0] + corners[2][0]) / 2,
                                  (corners[0][1] + corners[2][1]) / 2), "E", 1))
        RHS.add_edges_from(
            [(v1, v1_5), (v1_5, v2), (v2, v2_5), (v2_5, v3), (v3, v3_5), (v3_5, v4), (v1, v4_5), (v4, v4_5),
             (v1, i), (v2, i), (v3, i), (v4, i)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append([v1, v1_5, v2, v2_5, v3, v3_5, v4_5, v4, i])  # appending RHS to first level
        self.graph.graph = RHS

        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))
        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        g = self.graph.P8(1)

        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)


    def test_p8_not_on_middle(self):
        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (-1, 1) and level 1, E vertex at (0.5, 1.0) and level 1, E vertex at (1, 1) and level 1, E vertex at (1.0, 0.0) and level 1, E vertex at (1, -1) and level 1, E vertex at (0.0, -1.0) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (-1, -1) and level 1, i vertex at (0.0, 0.0) and level 1]",
        ]

        expected_nodes = ["e vertex at (0, 0) and level 0",
                          "E vertex at (-1, 1) and level 1",
                          "E vertex at (0.5, 1.0) and level 1",
                          "E vertex at (1, 1) and level 1",
                          "E vertex at (1.0, 0.0) and level 1",
                          "E vertex at (1, -1) and level 1",
                          "E vertex at (0.0, -1.0) and level 1",
                          "E vertex at (-1.0, 0.0) and level 1",
                          "E vertex at (-1, -1) and level 1",
                          "i vertex at (0.0, 0.0) and level 1",
                          ]

        expected_edges = [("E vertex at (-1, 1) and level 1", "E vertex at (0.5, 1.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "E vertex at (-1.0, 0.0) and level 1"),
                          ("E vertex at (-1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (0.5, 1.0) and level 1", "E vertex at (1, 1) and level 1"),
                          ("E vertex at (1, 1) and level 1", "E vertex at (1.0, 0.0) and level 1"),
                          ("E vertex at (1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (1.0, 0.0) and level 1", "E vertex at (1, -1) and level 1"),
                          ("E vertex at (1, -1) and level 1", "E vertex at (0.0, -1.0) and level 1"),
                          ("E vertex at (1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ("E vertex at (0.0, -1.0) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (-1.0, 0.0) and level 1", "E vertex at (-1, -1) and level 1"),
                          ("E vertex at (-1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
                          ]

        corners = self.graph.corners

        RHS = nx.Graph()
        RHS.add_node(v0 := Vertex((0, 0), "e", 0))
        RHS.add_node(v1 := Vertex(corners[0], "E", 1))

        RHS.add_node(v1_5 := Vertex(((corners[0][0] + corners[1][0]) / 2 + 0.5,
                                     (corners[0][1] + corners[1][1]) / 2 ), "E", 1))
        RHS.add_node(v2 := Vertex(corners[1], "E", 1))
        RHS.add_node(v2_5 := Vertex(((corners[1][0] + corners[2][0]) / 2,
                                     (corners[1][1] + corners[2][1]) / 2), "E", 1))
        RHS.add_node(v3 := Vertex(corners[2], "E", 1))
        RHS.add_node(v3_5 := Vertex(((corners[2][0] + corners[3][0]) / 2,
                                     (corners[2][1] + corners[3][1]) / 2), "E", 1))

        RHS.add_node(v4_5 := Vertex(((corners[0][0] + corners[3][0]) / 2,
                                     (corners[0][1] + corners[3][1]) / 2), "E", 1))
        RHS.add_node(v4 := Vertex(corners[3], "E", 1))

        RHS.add_node(i := Vertex(((corners[0][0] + corners[2][0]) / 2,
                                  (corners[0][1] + corners[2][1]) / 2), "I", 1))
        RHS.add_edges_from(
            [(v1, v1_5), (v1_5, v2), (v2, v2_5), (v2_5, v3), (v3, v3_5), (v3_5, v4), (v1, v4_5), (v4, v4_5),
             (v1, i), (v2, i), (v3, i), (v4, i)])

        self.graph.tiers[0] = [v0]
        self.graph.tiers.append([v1, v1_5, v2, v2_5, v3, v3_5, v4_5, v4, i])  # appending RHS to first level
        self.graph.graph = RHS

        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))
        matches = GraphMatcherByLabel(self.graph.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

        g = self.graph.P8(1)

        g.showLevel(1)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)


if __name__ == "__main__":
    unittest.main()
