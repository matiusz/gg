import unittest

from visualization import TieredGraph


class P3P4Test(unittest.TestCase):
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
        self.assertEqual(expected_edges, [(pair[0].__repr__(), pair[1].__repr__()) for pair in list(self.graph.graph.edges)])

    def test_p3(self):
        expected_tiers = [
            "[e vertex at (0, 0) and level 0]",
            "[E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex at (-1, -1) and level 1, E vertex at (1, -1) and level 1, i vertex at (0.0, 0.0) and level 1]",
            "[E vertex at (-1, 1) and level 2, E vertex at (0.0, 1.0) and level 2, E vertex at (1, 1) and level 2, E vertex at (-1, -1) and level 2, E vertex at (0.0, -1.0) and level 2, E vertex at (1, -1) and level 2, E vertex at (-1.0, 0.0) and level 2, E vertex at (0.0, 0.0) and level 2, E vertex at (1.0, 0.0) and level 2, I vertex at (-0.5, 0.5) and level 2, I vertex at (0.5, 0.5) and level 2, I vertex at (-0.5, -0.5) and level 2, I vertex at (0.5, -0.5) and level 2]",
        ]

        expected_nodes = [
            "e vertex at (0, 0) and level 0",
            "E vertex at (-1, 1) and level 1",
            "E vertex at (1, 1) and level 1",
            "E vertex at (-1, -1) and level 1",
            "E vertex at (1, -1) and level 1",
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
            "I vertex at (0.5, -0.5) and level 2",
        ]

        expected_edges = [
            ("E vertex at (-1, 1) and level 1", "E vertex at (1, 1) and level 1"),
            ("E vertex at (-1, 1) and level 1", "E vertex at (-1, -1) and level 1"),
            ("E vertex at (-1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
            ("E vertex at (1, 1) and level 1", "E vertex at (1, -1) and level 1"),
            ("E vertex at (1, 1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
            ("E vertex at (-1, -1) and level 1", "E vertex at (1, -1) and level 1"),
            ("E vertex at (-1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
            ("E vertex at (1, -1) and level 1", "i vertex at (0.0, 0.0) and level 1"),
            ("i vertex at (0.0, 0.0) and level 1", "I vertex at (-0.5, 0.5) and level 2"),
            ("i vertex at (0.0, 0.0) and level 1", "I vertex at (0.5, 0.5) and level 2"),
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
            ("E vertex at (0.0, -1.0) and level 2", "I vertex at (-0.5, -0.5) and level 2"),
            ("E vertex at (0.0, -1.0) and level 2", "I vertex at (0.5, -0.5) and level 2"),
            ("E vertex at (-1, -1) and level 2", "E vertex at (-1.0, 0.0) and level 2"),
            ("E vertex at (-1, -1) and level 2", "I vertex at (-0.5, -0.5) and level 2"),
            ("E vertex at (-1.0, 0.0) and level 2", "E vertex at (0.0, 0.0) and level 2"),
            ("E vertex at (-1.0, 0.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
            ("E vertex at (-1.0, 0.0) and level 2", "I vertex at (-0.5, -0.5) and level 2"),
            ("E vertex at (0.0, 0.0) and level 2", "I vertex at (-0.5, 0.5) and level 2"),
            ("E vertex at (0.0, 0.0) and level 2", "I vertex at (0.5, 0.5) and level 2"),
            ("E vertex at (0.0, 0.0) and level 2", "I vertex at (-0.5, -0.5) and level 2"),
            ("E vertex at (0.0, 0.0) and level 2", "I vertex at (0.5, -0.5) and level 2"),
        ]

        self.graph.P1()
        g = self.graph.P3(1)
        g.showLevel(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

if __name__ == "__main__":
    unittest.main()
