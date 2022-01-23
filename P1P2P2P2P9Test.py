import unittest

from visualization import TieredGraph, Direction


def double_key_sort(l):
    return sorted(sorted(l, key=lambda x: x[1]), key=lambda x: x[0])


def get_ith_vertex_from_graph(g, i):
    return list(g.graph.nodes.keys())[i]


class P1P2P2P2P9Test(unittest.TestCase):

    def setUp(self):
        v1 = (-1, 1)
        v2 = (1, 1)
        v3 = (-1, -1)
        v4 = (1, -1)
        self.graph = TieredGraph((v1, v2, v3, v4))

    def validate_tiers(self, graph, expectedTiers):
        self.assertEqual(sorted(expectedTiers), sorted(
            list(map(lambda vertex: vertex.__repr__(), graph.tiers))))

    def validate_graph(self, graph, expected_nodes, expected_edges):
        self.validate_nodes(graph, expected_nodes)
        self.validate_edges(graph, expected_edges)

    def validate_nodes(self, graph, expected_nodes):
        self.assertEqual(sorted(expected_nodes),
                         sorted([node.__repr__() for node in dict(graph.graph.nodes).keys()]))

    def validate_edges(self, graph, expected_edges):
        self.assertEqual(double_key_sort(expected_edges),
                         double_key_sort(
                             [(pair[0].__repr__(), pair[1].__repr__()) for pair in list(graph.graph.edges)]))

    def test_p1_p2_p2_p2_p9(self):
        expected_tiers = ['[E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex '
                          'at (-1, -1) and level 1, E vertex at (1, -1) and level 1, i vertex at (0.0, '
                          '0.0) and level 1]',
                          '[E vertex at (-1, 1) and level 2, E vertex at (0.0, 1.0) and level 2, E '
                          'vertex at (1, 1) and level 2, E vertex at (-1, -1) and level 2, E vertex at '
                          '(0.0, -1.0) and level 2, E vertex at (1, -1) and level 2, i vertex at (-0.5, '
                          '0.0) and level 2, i vertex at (0.5, 0.0) and level 2]',
                          '[E vertex at (-1, 1) and level 3, E vertex at (-1.0, 0.0) and level 3, E '
                          'vertex at (-1, -1) and level 3, E vertex at (0.0, 1.0) and level 3, E vertex '
                          'at (0.0, 0.0) and level 3, E vertex at (0.0, -1.0) and level 3, I vertex at '
                          '(-0.5, 0.5) and level 3, I vertex at (-0.5, -0.5) and level 3, E vertex at '
                          '(1, 1) and level 3, E vertex at (1.0, 0.0) and level 3, E vertex at (1, -1) '
                          'and level 3, I vertex at (0.5, 0.5) and level 3, I vertex at (0.5, -0.5) and '
                          'level 3]',
                          '[e vertex at (0, 0) and level 0]']

        expected_nodes = ['E vertex at (-1, -1) and level 1',
                          'E vertex at (-1, -1) and level 2',
                          'E vertex at (-1, -1) and level 3',
                          'E vertex at (-1, 1) and level 1',
                          'E vertex at (-1, 1) and level 2',
                          'E vertex at (-1, 1) and level 3',
                          'E vertex at (-1.0, 0.0) and level 3',
                          'E vertex at (0.0, -1.0) and level 2',
                          'E vertex at (0.0, -1.0) and level 3',
                          'E vertex at (0.0, 0.0) and level 3',
                          'E vertex at (0.0, 1.0) and level 2',
                          'E vertex at (0.0, 1.0) and level 3',
                          'E vertex at (1, -1) and level 1',
                          'E vertex at (1, -1) and level 2',
                          'E vertex at (1, -1) and level 3',
                          'E vertex at (1, 1) and level 1',
                          'E vertex at (1, 1) and level 2',
                          'E vertex at (1, 1) and level 3',
                          'E vertex at (1.0, 0.0) and level 3',
                          'I vertex at (-0.5, -0.5) and level 3',
                          'I vertex at (-0.5, 0.5) and level 3',
                          'I vertex at (0.5, -0.5) and level 3',
                          'I vertex at (0.5, 0.5) and level 3',
                          'e vertex at (0, 0) and level 0',
                          'i vertex at (-0.5, 0.0) and level 2',
                          'i vertex at (0.0, 0.0) and level 1',
                          'i vertex at (0.5, 0.0) and level 2']

        expected_edges = [('E vertex at (-1, -1) and level 1', 'E vertex at (1, -1) and level 1'),
                          ('E vertex at (-1, -1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (-1, -1) and level 2', 'E vertex at (0.0, -1.0) and level 2'),
                          ('E vertex at (-1, -1) and level 2', 'i vertex at (-0.5, 0.0) and level 2'),
                          ('E vertex at (-1, -1) and level 3', 'E vertex at (0.0, -1.0) and level 3'),
                          ('E vertex at (-1, -1) and level 3', 'I vertex at (-0.5, -0.5) and level 3'),
                          ('E vertex at (-1, 1) and level 1', 'E vertex at (-1, -1) and level 1'),
                          ('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
                          ('E vertex at (-1, 1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (-1, 1) and level 2', 'E vertex at (-1, -1) and level 2'),
                          ('E vertex at (-1, 1) and level 2', 'E vertex at (0.0, 1.0) and level 2'),
                          ('E vertex at (-1, 1) and level 2', 'i vertex at (-0.5, 0.0) and level 2'),
                          ('E vertex at (-1, 1) and level 3', 'E vertex at (-1.0, 0.0) and level 3'),
                          ('E vertex at (-1, 1) and level 3', 'E vertex at (0.0, 1.0) and level 3'),
                          ('E vertex at (-1, 1) and level 3', 'I vertex at (-0.5, 0.5) and level 3'),
                          ('E vertex at (-1.0, 0.0) and level 3', 'E vertex at (-1, -1) and level 3'),
                          ('E vertex at (-1.0, 0.0) and level 3', 'E vertex at (0.0, 0.0) and level 3'),
                          ('E vertex at (-1.0, 0.0) and level 3',
                           'I vertex at (-0.5, -0.5) and level 3'),
                          ('E vertex at (-1.0, 0.0) and level 3', 'I vertex at (-0.5, 0.5) and level 3'),
                          ('E vertex at (0.0, -1.0) and level 2', 'E vertex at (1, -1) and level 2'),
                          ('E vertex at (0.0, -1.0) and level 2', 'i vertex at (-0.5, 0.0) and level 2'),
                          ('E vertex at (0.0, -1.0) and level 2', 'i vertex at (0.5, 0.0) and level 2'),
                          ('E vertex at (0.0, -1.0) and level 3', 'E vertex at (1, -1) and level 3'),
                          ('E vertex at (0.0, -1.0) and level 3',
                           'I vertex at (-0.5, -0.5) and level 3'),
                          ('E vertex at (0.0, -1.0) and level 3', 'I vertex at (0.5, -0.5) and level 3'),
                          ('E vertex at (0.0, 0.0) and level 3', 'E vertex at (0.0, -1.0) and level 3'),
                          ('E vertex at (0.0, 0.0) and level 3', 'E vertex at (1.0, 0.0) and level 3'),
                          ('E vertex at (0.0, 0.0) and level 3', 'I vertex at (-0.5, -0.5) and level 3'),
                          ('E vertex at (0.0, 0.0) and level 3', 'I vertex at (-0.5, 0.5) and level 3'),
                          ('E vertex at (0.0, 0.0) and level 3', 'I vertex at (0.5, -0.5) and level 3'),
                          ('E vertex at (0.0, 0.0) and level 3', 'I vertex at (0.5, 0.5) and level 3'),
                          ('E vertex at (0.0, 1.0) and level 2', 'E vertex at (0.0, -1.0) and level 2'),
                          ('E vertex at (0.0, 1.0) and level 2', 'E vertex at (1, 1) and level 2'),
                          ('E vertex at (0.0, 1.0) and level 2', 'i vertex at (-0.5, 0.0) and level 2'),
                          ('E vertex at (0.0, 1.0) and level 2', 'i vertex at (0.5, 0.0) and level 2'),
                          ('E vertex at (0.0, 1.0) and level 3', 'E vertex at (0.0, 0.0) and level 3'),
                          ('E vertex at (0.0, 1.0) and level 3', 'E vertex at (1, 1) and level 3'),
                          ('E vertex at (0.0, 1.0) and level 3', 'I vertex at (-0.5, 0.5) and level 3'),
                          ('E vertex at (0.0, 1.0) and level 3', 'I vertex at (0.5, 0.5) and level 3'),
                          ('E vertex at (1, -1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (1, -1) and level 2', 'i vertex at (0.5, 0.0) and level 2'),
                          ('E vertex at (1, -1) and level 3', 'I vertex at (0.5, -0.5) and level 3'),
                          ('E vertex at (1, 1) and level 1', 'E vertex at (1, -1) and level 1'),
                          ('E vertex at (1, 1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (1, 1) and level 2', 'E vertex at (1, -1) and level 2'),
                          ('E vertex at (1, 1) and level 2', 'i vertex at (0.5, 0.0) and level 2'),
                          ('E vertex at (1, 1) and level 3', 'E vertex at (1.0, 0.0) and level 3'),
                          ('E vertex at (1, 1) and level 3', 'I vertex at (0.5, 0.5) and level 3'),
                          ('E vertex at (1.0, 0.0) and level 3', 'E vertex at (1, -1) and level 3'),
                          ('E vertex at (1.0, 0.0) and level 3', 'I vertex at (0.5, -0.5) and level 3'),
                          ('E vertex at (1.0, 0.0) and level 3', 'I vertex at (0.5, 0.5) and level 3'),
                          ('e vertex at (0, 0) and level 0', 'i vertex at (0.0, 0.0) and level 1'),
                          ('i vertex at (-0.5, 0.0) and level 2',
                           'I vertex at (-0.5, -0.5) and level 3'),
                          ('i vertex at (-0.5, 0.0) and level 2', 'I vertex at (-0.5, 0.5) and level 3'),
                          ('i vertex at (0.0, 0.0) and level 1', 'i vertex at (-0.5, 0.0) and level 2'),
                          ('i vertex at (0.0, 0.0) and level 1', 'i vertex at (0.5, 0.0) and level 2'),
                          ('i vertex at (0.5, 0.0) and level 2', 'I vertex at (0.5, -0.5) and level 3'),
                          ('i vertex at (0.5, 0.0) and level 2', 'I vertex at (0.5, 0.5) and level 3')]

        g = self.graph
        g.P1()
        g.P2(1)
        g.P2(2, Direction.HORIZONTAL)
        g.P2(2, Direction.HORIZONTAL)
        g.P9(3)

        g.showLevel(3)
        g.show3d()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(g, expected_nodes, expected_edges)


if __name__ == "__main__":
    unittest.main()
