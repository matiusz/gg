import unittest

from collections import deque
from visualization import TieredGraph, Vertex
import networkx as nx


def P3RHS(graph):
    RHS = nx.Graph()
    RHS.add_node(v0 := Vertex((0, 0), "e", 0))
    RHS.add_node(v1 := Vertex(graph.corners[0], "E", 1))
    RHS.add_node(v2 := Vertex(graph.corners[1], "E", 1))
    RHS.add_node(v3 := Vertex(graph.corners[2], "E", 1))
    RHS.add_node(v4 := Vertex(graph.corners[3], "E", 1))

    RHS.add_node(i := Vertex(((graph.corners[0][0] + graph.corners[2][0]) / 2, (graph.corners[0][1] + graph.corners[2][1]) / 2), "I", 1))
    RHS.add_edges_from([(v1, v2), (v2, v3), (v3, v4), (v4, v1), (v1, i), (v2, i), (v3, i), (v4, i)])
    graph.tiers[0] = [v0]
    graph.tiers.append([v1, v2, v3, v4, i])  # appending RHS to first level

    graph.graph = RHS


def P4RHS(graph, rotation):
    corners = deque(graph.corners)
    corners.rotate(rotation)

    RHS = nx.Graph()
    RHS.add_node(v0 := Vertex((0, 0), "e", 0))
    RHS.add_node(v1 := Vertex(corners[0], "E", 1))
    RHS.add_node(v1_5 := Vertex(((corners[0][0] + corners[1][0]) / 2, (corners[0][1] + corners[1][1]) / 2), "E", 1))
    RHS.add_node(v2 := Vertex(corners[1], "E", 1))
    RHS.add_node(v3 := Vertex(corners[2], "E", 1))
    RHS.add_node(v4 := Vertex(corners[3], "E", 1))

    RHS.add_node(i := Vertex(((corners[0][0] + corners[2][0]) / 2, (corners[0][1] + corners[2][1]) / 2), "I", 1))
    RHS.add_edges_from([(v1, v1_5), (v1_5, v2), (v2, v3), (v3, v4), (v4, v1), (v1, i), (v2, i), (v3, i), (v4, i)])
    graph.tiers[0] = [v0]
    graph.tiers.append([v1, v1_5, v2, v3, v4, i])  # appending RHS to first level

    graph.graph = RHS


class P3P4Test(unittest.TestCase):
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
        self.assertEqual(expected_edges, [(pair[0].__repr__(), pair[1].__repr__()) for pair in list(self.graph.graph.edges)])

    def test_p3(self):
        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex at (1, -1) and level 1, E vertex at (-1, -1) and level 1, i vertex at (0.0, 0.0) and level 1]",
            "[E vertex at (-1, 1) and level 2, E vertex at (0.0, 1.0) and level 2, E vertex at (1, 1) and level 2, E vertex at (-1, -1) and level 2, E vertex at (0.0, -1.0) and level 2, E vertex at (1, -1) and level 2, E vertex at (-1.0, 0.0) and level 2, E vertex at (0.0, 0.0) and level 2, E vertex at (1.0, 0.0) and level 2, I vertex at (-0.5, 0.5) and level 2, I vertex at (0.5, 0.5) and level 2, I vertex at (-0.5, -0.5) and level 2, I vertex at (0.5, -0.5) and level 2]",
        ]

        expected_nodes = [
            'e vertex at (0, 0) and level 0',
            'E vertex at (-1, 1) and level 1',
            'E vertex at (1, 1) and level 1',
            'E vertex at (1, -1) and level 1',
            'E vertex at (-1, -1) and level 1',
            'i vertex at (0.0, 0.0) and level 1',
            'E vertex at (-1, 1) and level 2',
            'E vertex at (0.0, 1.0) and level 2',
            'E vertex at (1, 1) and level 2',
            'E vertex at (1.0, 0.0) and level 2',
            'E vertex at (1, -1) and level 2',
            'E vertex at (0.0, -1.0) and level 2',
            'E vertex at (-1, -1) and level 2',
            'E vertex at (-1.0, 0.0) and level 2',
            'E vertex at (0.0, 0.0) and level 2',
            'I vertex at (-0.5, 0.5) and level 2',
            'I vertex at (0.5, 0.5) and level 2',
            'I vertex at (-0.5, -0.5) and level 2',
            'I vertex at (0.5, -0.5) and level 2'
        ]

        expected_edges = [
            ('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
            ('E vertex at (-1, 1) and level 1', 'E vertex at (-1, -1) and level 1'),
            ('E vertex at (-1, 1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('E vertex at (1, 1) and level 1', 'E vertex at (1, -1) and level 1'),
            ('E vertex at (1, 1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('E vertex at (1, -1) and level 1', 'E vertex at (-1, -1) and level 1'),
            ('E vertex at (1, -1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('E vertex at (-1, -1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('i vertex at (0.0, 0.0) and level 1', 'I vertex at (-0.5, 0.5) and level 2'),
            ('i vertex at (0.0, 0.0) and level 1', 'I vertex at (0.5, 0.5) and level 2'),
            ('E vertex at (-1, 1) and level 2', 'E vertex at (0.0, 1.0) and level 2'),
            ('E vertex at (-1, 1) and level 2', 'E vertex at (-1.0, 0.0) and level 2'),
            ('E vertex at (-1, 1) and level 2', 'I vertex at (-0.5, 0.5) and level 2'),
            ('E vertex at (0.0, 1.0) and level 2', 'E vertex at (1, 1) and level 2'),
            ('E vertex at (0.0, 1.0) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
            ('E vertex at (0.0, 1.0) and level 2', 'I vertex at (-0.5, 0.5) and level 2'),
            ('E vertex at (0.0, 1.0) and level 2', 'I vertex at (0.5, 0.5) and level 2'),
            ('E vertex at (1, 1) and level 2', 'E vertex at (1.0, 0.0) and level 2'),
            ('E vertex at (1, 1) and level 2', 'I vertex at (0.5, 0.5) and level 2'),
            ('E vertex at (1.0, 0.0) and level 2', 'E vertex at (1, -1) and level 2'),
            ('E vertex at (1.0, 0.0) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
            ('E vertex at (1.0, 0.0) and level 2', 'I vertex at (0.5, 0.5) and level 2'),
            ('E vertex at (1.0, 0.0) and level 2', 'I vertex at (0.5, -0.5) and level 2'),
            ('E vertex at (1, -1) and level 2', 'E vertex at (0.0, -1.0) and level 2'),
            ('E vertex at (1, -1) and level 2', 'I vertex at (0.5, -0.5) and level 2'),
            ('E vertex at (0.0, -1.0) and level 2', 'E vertex at (-1, -1) and level 2'),
            ('E vertex at (0.0, -1.0) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
            ('E vertex at (0.0, -1.0) and level 2', 'I vertex at (-0.5, -0.5) and level 2'),
            ('E vertex at (0.0, -1.0) and level 2', 'I vertex at (0.5, -0.5) and level 2'),
            ('E vertex at (-1, -1) and level 2', 'E vertex at (-1.0, 0.0) and level 2'),
            ('E vertex at (-1, -1) and level 2', 'I vertex at (-0.5, -0.5) and level 2'),
            ('E vertex at (-1.0, 0.0) and level 2', 'E vertex at (0.0, 0.0) and level 2'),
            ('E vertex at (-1.0, 0.0) and level 2', 'I vertex at (-0.5, 0.5) and level 2'),
            ('E vertex at (-1.0, 0.0) and level 2', 'I vertex at (-0.5, -0.5) and level 2'),
            ('E vertex at (0.0, 0.0) and level 2', 'I vertex at (-0.5, 0.5) and level 2'),
            ('E vertex at (0.0, 0.0) and level 2', 'I vertex at (0.5, 0.5) and level 2'),
            ('E vertex at (0.0, 0.0) and level 2', 'I vertex at (-0.5, -0.5) and level 2'),
            ('E vertex at (0.0, 0.0) and level 2', 'I vertex at (0.5, -0.5) and level 2')
        ]

        P3RHS(self.graph)

        g = self.graph.P3(1)
        g.showLevel(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p4_rotation_0(self):
        P4RHS(self.graph, 0)

        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (-1, 1) and level 1, E vertex at (0.0, 1.0) and level 1, E vertex at (1, 1) and level 1, E vertex at (1, -1) and level 1, E vertex at (-1, -1) and level 1, i vertex at (0.0, 0.0) and level 1]",
            "[E vertex at (-1, 1) and level 2, E vertex at (0.0, 1.0) and level 2, E vertex at (1, 1) and level 2, E vertex at (-1, -1) and level 2, E vertex at (0.0, -1.0) and level 2, E vertex at (1, -1) and level 2, I vertex at (-0.5, 0.0) and level 2, I vertex at (0.5, 0.0) and level 2]",
        ]

        expected_nodes = [
            "e vertex at (0, 0) and level 0",
            "E vertex at (-1, 1) and level 1",
            "E vertex at (0.0, 1.0) and level 1",
            "E vertex at (1, 1) and level 1",
            "E vertex at (1, -1) and level 1",
            "E vertex at (-1, -1) and level 1",
            "i vertex at (0.0, 0.0) and level 1",
            "E vertex at (-1, 1) and level 2",
            "E vertex at (0.0, 1.0) and level 2",
            "E vertex at (1, 1) and level 2",
            "E vertex at (-1, -1) and level 2",
            "E vertex at (0.0, -1.0) and level 2",
            "E vertex at (1, -1) and level 2",
            "I vertex at (-0.5, 0.0) and level 2",
            "I vertex at (0.5, 0.0) and level 2",
        ]

        expected_edges = [
            ('E vertex at (-1, 1) and level 1', 'E vertex at (0.0, 1.0) and level 1'),
            ('E vertex at (-1, 1) and level 1', 'E vertex at (-1, -1) and level 1'),
            ('E vertex at (-1, 1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('E vertex at (0.0, 1.0) and level 1', 'E vertex at (1, 1) and level 1'),
            ('E vertex at (1, 1) and level 1', 'E vertex at (1, -1) and level 1'),
            ('E vertex at (1, 1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('E vertex at (1, -1) and level 1', 'E vertex at (-1, -1) and level 1'),
            ('E vertex at (1, -1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('E vertex at (-1, -1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('i vertex at (0.0, 0.0) and level 1', 'I vertex at (-0.5, 0.0) and level 2'),
            ('i vertex at (0.0, 0.0) and level 1', 'I vertex at (0.5, 0.0) and level 2'),
            ('E vertex at (-1, 1) and level 2', 'E vertex at (0.0, 1.0) and level 2'),
            ('E vertex at (-1, 1) and level 2', 'E vertex at (-1, -1) and level 2'),
            ('E vertex at (-1, 1) and level 2', 'I vertex at (-0.5, 0.0) and level 2'),
            ('E vertex at (0.0, 1.0) and level 2', 'E vertex at (1, 1) and level 2'),
            ('E vertex at (0.0, 1.0) and level 2', 'E vertex at (0.0, -1.0) and level 2'),
            ('E vertex at (0.0, 1.0) and level 2', 'I vertex at (-0.5, 0.0) and level 2'),
            ('E vertex at (0.0, 1.0) and level 2', 'I vertex at (0.5, 0.0) and level 2'),
            ('E vertex at (1, 1) and level 2', 'E vertex at (1, -1) and level 2'),
            ('E vertex at (1, 1) and level 2', 'I vertex at (0.5, 0.0) and level 2'),
            ('E vertex at (-1, -1) and level 2', 'E vertex at (0.0, -1.0) and level 2'),
            ('E vertex at (-1, -1) and level 2', 'I vertex at (-0.5, 0.0) and level 2'),
            ('E vertex at (0.0, -1.0) and level 2', 'E vertex at (1, -1) and level 2'),
            ('E vertex at (0.0, -1.0) and level 2', 'I vertex at (-0.5, 0.0) and level 2'),
            ('E vertex at (0.0, -1.0) and level 2', 'I vertex at (0.5, 0.0) and level 2'),
            ('E vertex at (1, -1) and level 2', 'I vertex at (0.5, 0.0) and level 2')
        ]

        g = self.graph.P4(1)

        g.showLevel(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p4_rotation_1(self):
        P4RHS(self.graph, 1)

        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (-1, -1) and level 1, E vertex at (-1.0, 0.0) and level 1, E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex at (1, -1) and level 1, i vertex at (0.0, 0.0) and level 1]",
            "[E vertex at (-1, -1) and level 2, E vertex at (-1.0, 0.0) and level 2, E vertex at (-1, 1) and level 2, E vertex at (1, -1) and level 2, E vertex at (1.0, 0.0) and level 2, E vertex at (1, 1) and level 2, I vertex at (0.0, -0.5) and level 2, I vertex at (0.0, 0.5) and level 2]",
        ]

        expected_nodes = [
            'e vertex at (0, 0) and level 0',
            'E vertex at (-1, -1) and level 1',
            'E vertex at (-1.0, 0.0) and level 1',
            'E vertex at (-1, 1) and level 1',
            'E vertex at (1, 1) and level 1',
            'E vertex at (1, -1) and level 1',
            'i vertex at (0.0, 0.0) and level 1',
            'E vertex at (-1, -1) and level 2',
            'E vertex at (-1.0, 0.0) and level 2',
            'E vertex at (-1, 1) and level 2',
            'E vertex at (1, -1) and level 2',
            'E vertex at (1.0, 0.0) and level 2',
            'E vertex at (1, 1) and level 2',
            'I vertex at (0.0, -0.5) and level 2',
            'I vertex at (0.0, 0.5) and level 2'
        ]

        expected_edges = [
            ('E vertex at (-1, -1) and level 1', 'E vertex at (-1.0, 0.0) and level 1'),
            ('E vertex at (-1, -1) and level 1', 'E vertex at (1, -1) and level 1'),
            ('E vertex at (-1, -1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('E vertex at (-1.0, 0.0) and level 1', 'E vertex at (-1, 1) and level 1'),
            ('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
            ('E vertex at (-1, 1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('E vertex at (1, 1) and level 1', 'E vertex at (1, -1) and level 1'),
            ('E vertex at (1, 1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('E vertex at (1, -1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('i vertex at (0.0, 0.0) and level 1', 'I vertex at (0.0, -0.5) and level 2'),
            ('i vertex at (0.0, 0.0) and level 1', 'I vertex at (0.0, 0.5) and level 2'),
            ('E vertex at (-1, -1) and level 2', 'E vertex at (-1.0, 0.0) and level 2'),
            ('E vertex at (-1, -1) and level 2', 'E vertex at (1, -1) and level 2'),
            ('E vertex at (-1, -1) and level 2', 'I vertex at (0.0, -0.5) and level 2'),
            ('E vertex at (-1.0, 0.0) and level 2', 'E vertex at (-1, 1) and level 2'),
            ('E vertex at (-1.0, 0.0) and level 2', 'E vertex at (1.0, 0.0) and level 2'),
            ('E vertex at (-1.0, 0.0) and level 2', 'I vertex at (0.0, -0.5) and level 2'),
            ('E vertex at (-1.0, 0.0) and level 2', 'I vertex at (0.0, 0.5) and level 2'),
            ('E vertex at (-1, 1) and level 2', 'E vertex at (1, 1) and level 2'),
            ('E vertex at (-1, 1) and level 2', 'I vertex at (0.0, 0.5) and level 2'),
            ('E vertex at (1, -1) and level 2', 'E vertex at (1.0, 0.0) and level 2'),
            ('E vertex at (1, -1) and level 2', 'I vertex at (0.0, -0.5) and level 2'),
            ('E vertex at (1.0, 0.0) and level 2', 'E vertex at (1, 1) and level 2'),
            ('E vertex at (1.0, 0.0) and level 2', 'I vertex at (0.0, -0.5) and level 2'),
            ('E vertex at (1.0, 0.0) and level 2', 'I vertex at (0.0, 0.5) and level 2'),
            ('E vertex at (1, 1) and level 2', 'I vertex at (0.0, 0.5) and level 2')
        ]

        g = self.graph.P4(1)

        g.showLevel(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p4_rotation_2(self):
        P4RHS(self.graph, 2)

        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (1, -1) and level 1, E vertex at (0.0, -1.0) and level 1, E vertex at (-1, -1) and level 1, E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, i vertex at (0.0, 0.0) and level 1]",
            "[E vertex at (1, -1) and level 2, E vertex at (0.0, -1.0) and level 2, E vertex at (-1, -1) and level 2, E vertex at (1, 1) and level 2, E vertex at (0.0, 1.0) and level 2, E vertex at (-1, 1) and level 2, I vertex at (0.5, 0.0) and level 2, I vertex at (-0.5, 0.0) and level 2]",
        ]

        expected_nodes = [
            'e vertex at (0, 0) and level 0',
            'E vertex at (1, -1) and level 1',
            'E vertex at (0.0, -1.0) and level 1',
            'E vertex at (-1, -1) and level 1',
            'E vertex at (-1, 1) and level 1',
            'E vertex at (1, 1) and level 1',
            'i vertex at (0.0, 0.0) and level 1',
            'E vertex at (1, -1) and level 2',
            'E vertex at (0.0, -1.0) and level 2',
            'E vertex at (-1, -1) and level 2',
            'E vertex at (1, 1) and level 2',
            'E vertex at (0.0, 1.0) and level 2',
            'E vertex at (-1, 1) and level 2',
            'I vertex at (0.5, 0.0) and level 2',
            'I vertex at (-0.5, 0.0) and level 2'
        ]

        expected_edges = [
            ('E vertex at (1, -1) and level 1', 'E vertex at (0.0, -1.0) and level 1'),
            ('E vertex at (1, -1) and level 1', 'E vertex at (1, 1) and level 1'),
            ('E vertex at (1, -1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('E vertex at (0.0, -1.0) and level 1', 'E vertex at (-1, -1) and level 1'),
            ('E vertex at (-1, -1) and level 1', 'E vertex at (-1, 1) and level 1'),
            ('E vertex at (-1, -1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
            ('E vertex at (-1, 1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('E vertex at (1, 1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('i vertex at (0.0, 0.0) and level 1', 'I vertex at (0.5, 0.0) and level 2'),
            ('i vertex at (0.0, 0.0) and level 1', 'I vertex at (-0.5, 0.0) and level 2'),
            ('E vertex at (1, -1) and level 2', 'E vertex at (0.0, -1.0) and level 2'),
            ('E vertex at (1, -1) and level 2', 'E vertex at (1, 1) and level 2'),
            ('E vertex at (1, -1) and level 2', 'I vertex at (0.5, 0.0) and level 2'),
            ('E vertex at (0.0, -1.0) and level 2', 'E vertex at (-1, -1) and level 2'),
            ('E vertex at (0.0, -1.0) and level 2', 'E vertex at (0.0, 1.0) and level 2'),
            ('E vertex at (0.0, -1.0) and level 2', 'I vertex at (0.5, 0.0) and level 2'),
            ('E vertex at (0.0, -1.0) and level 2', 'I vertex at (-0.5, 0.0) and level 2'),
            ('E vertex at (-1, -1) and level 2', 'E vertex at (-1, 1) and level 2'),
            ('E vertex at (-1, -1) and level 2', 'I vertex at (-0.5, 0.0) and level 2'),
            ('E vertex at (1, 1) and level 2', 'E vertex at (0.0, 1.0) and level 2'),
            ('E vertex at (1, 1) and level 2', 'I vertex at (0.5, 0.0) and level 2'),
            ('E vertex at (0.0, 1.0) and level 2', 'E vertex at (-1, 1) and level 2'),
            ('E vertex at (0.0, 1.0) and level 2', 'I vertex at (0.5, 0.0) and level 2'),
            ('E vertex at (0.0, 1.0) and level 2', 'I vertex at (-0.5, 0.0) and level 2'),
            ('E vertex at (-1, 1) and level 2', 'I vertex at (-0.5, 0.0) and level 2')
        ]

        g = self.graph.P4(1)

        g.showLevel(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p4_rotation_3(self):
        P4RHS(self.graph, 3)

        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (1, 1) and level 1, E vertex at (1.0, 0.0) and level 1, E vertex at (1, -1) and level 1, E vertex at (-1, -1) and level 1, E vertex at (-1, 1) and level 1, i vertex at (0.0, 0.0) and level 1]",
            "[E vertex at (1, 1) and level 2, E vertex at (1.0, 0.0) and level 2, E vertex at (1, -1) and level 2, E vertex at (-1, 1) and level 2, E vertex at (-1.0, 0.0) and level 2, E vertex at (-1, -1) and level 2, I vertex at (0.0, 0.5) and level 2, I vertex at (0.0, -0.5) and level 2]",
        ]

        expected_nodes = [
            'e vertex at (0, 0) and level 0',
            'E vertex at (1, 1) and level 1',
            'E vertex at (1.0, 0.0) and level 1',
            'E vertex at (1, -1) and level 1',
            'E vertex at (-1, -1) and level 1',
            'E vertex at (-1, 1) and level 1',
            'i vertex at (0.0, 0.0) and level 1',
            'E vertex at (1, 1) and level 2',
            'E vertex at (1.0, 0.0) and level 2',
            'E vertex at (1, -1) and level 2',
            'E vertex at (-1, 1) and level 2',
            'E vertex at (-1.0, 0.0) and level 2',
            'E vertex at (-1, -1) and level 2',
            'I vertex at (0.0, 0.5) and level 2',
            'I vertex at (0.0, -0.5) and level 2'
        ]

        expected_edges = [
            ('E vertex at (1, 1) and level 1', 'E vertex at (1.0, 0.0) and level 1'),
            ('E vertex at (1, 1) and level 1', 'E vertex at (-1, 1) and level 1'),
            ('E vertex at (1, 1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('E vertex at (1.0, 0.0) and level 1', 'E vertex at (1, -1) and level 1'),
            ('E vertex at (1, -1) and level 1', 'E vertex at (-1, -1) and level 1'),
            ('E vertex at (1, -1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('E vertex at (-1, -1) and level 1', 'E vertex at (-1, 1) and level 1'),
            ('E vertex at (-1, -1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('E vertex at (-1, 1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
            ('i vertex at (0.0, 0.0) and level 1', 'I vertex at (0.0, 0.5) and level 2'),
            ('i vertex at (0.0, 0.0) and level 1', 'I vertex at (0.0, -0.5) and level 2'),
            ('E vertex at (1, 1) and level 2', 'E vertex at (1.0, 0.0) and level 2'),
            ('E vertex at (1, 1) and level 2', 'E vertex at (-1, 1) and level 2'),
            ('E vertex at (1, 1) and level 2', 'I vertex at (0.0, 0.5) and level 2'),
            ('E vertex at (1.0, 0.0) and level 2', 'E vertex at (1, -1) and level 2'),
            ('E vertex at (1.0, 0.0) and level 2', 'E vertex at (-1.0, 0.0) and level 2'),
            ('E vertex at (1.0, 0.0) and level 2', 'I vertex at (0.0, 0.5) and level 2'),
            ('E vertex at (1.0, 0.0) and level 2', 'I vertex at (0.0, -0.5) and level 2'),
            ('E vertex at (1, -1) and level 2', 'E vertex at (-1, -1) and level 2'),
            ('E vertex at (1, -1) and level 2', 'I vertex at (0.0, -0.5) and level 2'),
            ('E vertex at (-1, 1) and level 2', 'E vertex at (-1.0, 0.0) and level 2'),
            ('E vertex at (-1, 1) and level 2', 'I vertex at (0.0, 0.5) and level 2'),
            ('E vertex at (-1.0, 0.0) and level 2', 'E vertex at (-1, -1) and level 2'),
            ('E vertex at (-1.0, 0.0) and level 2', 'I vertex at (0.0, 0.5) and level 2'),
            ('E vertex at (-1.0, 0.0) and level 2', 'I vertex at (0.0, -0.5) and level 2'),
            ('E vertex at (-1, -1) and level 2', 'I vertex at (0.0, -0.5) and level 2')
        ]

        g = self.graph.P4(1)

        g.showLevel(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p4_invalid_v1_5(self):
        RHS = nx.Graph()
        RHS.add_node(v0 := Vertex((0, 0), "e", 0))
        RHS.add_node(v1 := Vertex(self.graph.corners[0], "E", 1))
        RHS.add_node(v1_5 := Vertex(((self.graph.corners[0][0] + self.graph.corners[1][0]) / 2 + 0.25, (self.graph.corners[0][1] + self.graph.corners[1][1]) / 2), "E", 1))
        RHS.add_node(v2 := Vertex(self.graph.corners[1], "E", 1))
        RHS.add_node(v3 := Vertex(self.graph.corners[2], "E", 1))
        RHS.add_node(v4 := Vertex(self.graph.corners[3], "E", 1))

        RHS.add_node(i := Vertex(((self.graph.corners[0][0] + self.graph.corners[2][0]) / 2, (self.graph.corners[0][1] + self.graph.corners[2][1]) / 2), "I", 1))
        RHS.add_edges_from([(v1, v1_5), (v1_5, v2), (v2, v3), (v3, v4), (v4, v1), (v1, i), (v2, i), (v3, i), (v4, i)])
        self.graph.tiers[0] = [v0]
        self.graph.tiers.append([v1, v1_5, v2, v3, v4, i])  # appending RHS to first level

        self.graph.graph = RHS

        with self.assertRaises(AssertionError):
            g = self.graph.P4(1)


if __name__ == "__main__":
    unittest.main()
