import unittest

from visualization import Direction, TieredGraph, Vertex


def double_key_sort(l):
    return sorted(sorted(l, key=lambda x: x[1]), key=lambda x: x[0])


def get_ith_vertex_from_graph(g, i):
    return list(g.graph.nodes.keys())[i]


class P1P2Test(unittest.TestCase):

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

    def test_p1(self):
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

        g = self.graph.P1()
        g.showLevel(1)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(g, expected_nodes, expected_edges)

    def test_p1_for_node_with_changed_label(self):
        expected_tiers = ['[U vertex at (0, 0) and level 0]']
        expected_nodes = ['U vertex at (0, 0) and level 0']
        expected_edges = []

        v0 = Vertex((0, 0), "U", 0)
        graph_with_one_node = TieredGraph((v0,))

        v0 = get_ith_vertex_from_graph(graph_with_one_node, 0)
        v0.label = "U"
        graph_with_one_node.graph.add_node(v0)
        graph_with_one_node.showLevel(0)
        graph_with_one_node.P1()
        graph_with_one_node.showLevel(0)

        self.validate_tiers(graph_with_one_node, expected_tiers)
        self.validate_graph(graph_with_one_node, expected_nodes, expected_edges)

    def test_p1_p2_vertical(self):
        expected_tiers = ['[e vertex at (0, 0) and level 0]',
                          '[E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex at (-1, -1) and level 1, E vertex at (1, -1) and level 1, i vertex at (0.0, 0.0) and level 1]',
                          '[E vertex at (-1, 1) and level 2, E vertex at (0.0, 1.0) and level 2, E vertex at (1, 1) and level 2, E vertex at (-1, -1) and level 2, E vertex at (0.0, -1.0) and level 2, E vertex at (1, -1) and level 2, I vertex at (-0.5, 0.0) and level 2, I vertex at (0.5, 0.0) and level 2]']

        expected_nodes = ['e vertex at (0, 0) and level 0',
                          'E vertex at (-1, 1) and level 1',
                          'E vertex at (1, 1) and level 1',
                          'E vertex at (-1, -1) and level 1',
                          'E vertex at (1, -1) and level 1',
                          'i vertex at (0.0, 0.0) and level 1',
                          'E vertex at (-1, 1) and level 2',
                          'E vertex at (0.0, 1.0) and level 2',
                          'E vertex at (1, 1) and level 2',
                          'E vertex at (-1, -1) and level 2',
                          'E vertex at (0.0, -1.0) and level 2',
                          'E vertex at (1, -1) and level 2',
                          'I vertex at (-0.5, 0.0) and level 2',
                          'I vertex at (0.5, 0.0) and level 2']

        expected_edges = [('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
                          ('E vertex at (-1, 1) and level 1',
                           'E vertex at (-1, -1) and level 1'),
                          ('E vertex at (-1, 1) and level 1',
                           'i vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (1, 1) and level 1',
                           'E vertex at (1, -1) and level 1'),
                          ('E vertex at (1, 1) and level 1',
                           'i vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (-1, -1) and level 1',
                           'E vertex at (1, -1) and level 1'),
                          ('E vertex at (-1, -1) and level 1',
                           'i vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (1, -1) and level 1',
                           'i vertex at (0.0, 0.0) and level 1'),
                          ('i vertex at (0.0, 0.0) and level 1',
                           'I vertex at (-0.5, 0.0) and level 2'),
                          ('i vertex at (0.0, 0.0) and level 1',
                           'I vertex at (0.5, 0.0) and level 2'),
                          ('E vertex at (-1, 1) and level 2',
                           'E vertex at (0.0, 1.0) and level 2'),
                          ('E vertex at (-1, 1) and level 2',
                           'E vertex at (-1, -1) and level 2'),
                          ('E vertex at (-1, 1) and level 2',
                           'I vertex at (-0.5, 0.0) and level 2'),
                          ('E vertex at (0.0, 1.0) and level 2',
                           'E vertex at (1, 1) and level 2'),
                          ('E vertex at (0.0, 1.0) and level 2',
                           'E vertex at (0.0, -1.0) and level 2'),
                          ('E vertex at (0.0, 1.0) and level 2',
                           'I vertex at (-0.5, 0.0) and level 2'),
                          ('E vertex at (0.0, 1.0) and level 2',
                           'I vertex at (0.5, 0.0) and level 2'),
                          ('E vertex at (1, 1) and level 2',
                           'E vertex at (1, -1) and level 2'),
                          ('E vertex at (1, 1) and level 2',
                           'I vertex at (0.5, 0.0) and level 2'),
                          ('E vertex at (-1, -1) and level 2',
                           'E vertex at (0.0, -1.0) and level 2'),
                          ('E vertex at (-1, -1) and level 2',
                           'I vertex at (-0.5, 0.0) and level 2'),
                          ('E vertex at (0.0, -1.0) and level 2',
                           'E vertex at (1, -1) and level 2'),
                          ('E vertex at (0.0, -1.0) and level 2',
                           'I vertex at (-0.5, 0.0) and level 2'),
                          ('E vertex at (0.0, -1.0) and level 2',
                           'I vertex at (0.5, 0.0) and level 2'),
                          ('E vertex at (1, -1) and level 2', 'I vertex at (0.5, 0.0) and level 2')]

        self.graph.P1()
        g = self.graph.P2(1)
        g.showLevel(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(g, expected_nodes, expected_edges)

    def test_p1_p2_horizontal(self):
        expected_tiers = ['[e vertex at (0, 0) and level 0]',
                          '[E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex at (-1, -1) and level 1, E vertex at (1, -1) and level 1, i vertex at (0.0, 0.0) and level 1]',
                          '[E vertex at (-1, 1) and level 2, E vertex at (-1.0, 0.0) and level 2, E vertex at (-1, -1) and level 2, E vertex at (1, 1) and level 2, E vertex at (1.0, 0.0) and level 2, E vertex at (1, -1) and level 2, I vertex at (0.0, 0.5) and level 2, I vertex at (0.0, -0.5) and level 2]']

        expected_nodes = ['e vertex at (0, 0) and level 0',
                          'E vertex at (-1, 1) and level 1',
                          'E vertex at (1, 1) and level 1',
                          'E vertex at (-1, -1) and level 1',
                          'E vertex at (1, -1) and level 1',
                          'i vertex at (0.0, 0.0) and level 1',
                          'E vertex at (-1, 1) and level 2',
                          'E vertex at (1.0, 0.0) and level 2',
                          'E vertex at (1, 1) and level 2',
                          'E vertex at (-1, -1) and level 2',
                          'E vertex at (-1.0, 0.0) and level 2',
                          'E vertex at (1, -1) and level 2',
                          'I vertex at (0.0, -0.5) and level 2',
                          'I vertex at (0.0, 0.5) and level 2']

        expected_edges = [('E vertex at (-1, -1) and level 1', 'E vertex at (1, -1) and level 1'),
                          ('E vertex at (-1, -1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (-1, -1) and level 2', 'E vertex at (1, -1) and level 2'),
                          ('E vertex at (-1, -1) and level 2', 'I vertex at (0.0, -0.5) and level 2'),
                          ('E vertex at (-1, 1) and level 1', 'E vertex at (-1, -1) and level 1'),
                          ('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
                          ('E vertex at (-1, 1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (-1, 1) and level 2', 'E vertex at (-1.0, 0.0) and level 2'),
                          ('E vertex at (-1, 1) and level 2', 'E vertex at (1, 1) and level 2'),
                          ('E vertex at (-1, 1) and level 2', 'I vertex at (0.0, 0.5) and level 2'),
                          ('E vertex at (-1.0, 0.0) and level 2', 'E vertex at (-1, -1) and level 2'),
                          ('E vertex at (-1.0, 0.0) and level 2', 'E vertex at (1.0, 0.0) and level 2'),
                          ('E vertex at (-1.0, 0.0) and level 2', 'I vertex at (0.0, -0.5) and level 2'),
                          ('E vertex at (-1.0, 0.0) and level 2', 'I vertex at (0.0, 0.5) and level 2'),
                          ('E vertex at (1, -1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (1, -1) and level 2', 'I vertex at (0.0, -0.5) and level 2'),
                          ('E vertex at (1, 1) and level 1', 'E vertex at (1, -1) and level 1'),
                          ('E vertex at (1, 1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (1, 1) and level 2', 'E vertex at (1.0, 0.0) and level 2'),
                          ('E vertex at (1, 1) and level 2', 'I vertex at (0.0, 0.5) and level 2'),
                          ('E vertex at (1.0, 0.0) and level 2', 'E vertex at (1, -1) and level 2'),
                          ('E vertex at (1.0, 0.0) and level 2', 'I vertex at (0.0, -0.5) and level 2'),
                          ('E vertex at (1.0, 0.0) and level 2', 'I vertex at (0.0, 0.5) and level 2'),
                          ('i vertex at (0.0, 0.0) and level 1', 'I vertex at (0.0, -0.5) and level 2'),
                          ('i vertex at (0.0, 0.0) and level 1', 'I vertex at (0.0, 0.5) and level 2')]

        self.graph.P1()
        g = self.graph.P2(1, direction=Direction.HORIZONTAL)
        g.showLevel(1)
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(g, expected_nodes, expected_edges)

    def test_p1_p2_p2_all_vertical(self):
        expected_tiers = ['[E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex '
                          'at (-1, -1) and level 1, E vertex at (1, -1) and level 1, i vertex at (0.0, '
                          '0.0) and level 1]',
                          '[E vertex at (-1, 1) and level 2, E vertex at (0.0, 1.0) and level 2, E '
                          'vertex at (1, 1) and level 2, E vertex at (-1, -1) and level 2, E vertex at '
                          '(0.0, -1.0) and level 2, E vertex at (1, -1) and level 2, i vertex at (-0.5, '
                          '0.0) and level 2, I vertex at (0.5, 0.0) and level 2]',
                          '[E vertex at (-1, 1) and level 3, E vertex at (-0.5, 1.0) and level 3, E '
                          'vertex at (0.0, 1.0) and level 3, E vertex at (-1, -1) and level 3, E vertex '
                          'at (-0.5, -1.0) and level 3, E vertex at (0.0, -1.0) and level 3, I vertex '
                          'at (-0.75, 0.0) and level 3, I vertex at (-0.25, 0.0) and level 3]',
                          '[e vertex at (0, 0) and level 0]']

        expected_nodes = ['E vertex at (-0.5, -1.0) and level 3',
                          'E vertex at (-0.5, 1.0) and level 3',
                          'E vertex at (-1, -1) and level 1',
                          'E vertex at (-1, -1) and level 2',
                          'E vertex at (-1, -1) and level 3',
                          'E vertex at (-1, 1) and level 1',
                          'E vertex at (-1, 1) and level 2',
                          'E vertex at (-1, 1) and level 3',
                          'E vertex at (0.0, -1.0) and level 2',
                          'E vertex at (0.0, -1.0) and level 3',
                          'E vertex at (0.0, 1.0) and level 2',
                          'E vertex at (0.0, 1.0) and level 3',
                          'E vertex at (1, -1) and level 1',
                          'E vertex at (1, -1) and level 2',
                          'E vertex at (1, 1) and level 1',
                          'E vertex at (1, 1) and level 2',
                          'I vertex at (-0.25, 0.0) and level 3',
                          'I vertex at (-0.75, 0.0) and level 3',
                          'I vertex at (0.5, 0.0) and level 2',
                          'e vertex at (0, 0) and level 0',
                          'i vertex at (-0.5, 0.0) and level 2',
                          'i vertex at (0.0, 0.0) and level 1']

        expected_edges = [('E vertex at (-0.5, -1.0) and level 3',
                           'E vertex at (0.0, -1.0) and level 3'),
                          ('E vertex at (-0.5, -1.0) and level 3',
                           'I vertex at (-0.25, 0.0) and level 3'),
                          ('E vertex at (-0.5, -1.0) and level 3',
                           'I vertex at (-0.75, 0.0) and level 3'),
                          ('E vertex at (-0.5, 1.0) and level 3',
                           'E vertex at (-0.5, -1.0) and level 3'),
                          ('E vertex at (-0.5, 1.0) and level 3', 'E vertex at (0.0, 1.0) and level 3'),
                          ('E vertex at (-0.5, 1.0) and level 3',
                           'I vertex at (-0.25, 0.0) and level 3'),
                          ('E vertex at (-0.5, 1.0) and level 3',
                           'I vertex at (-0.75, 0.0) and level 3'),
                          ('E vertex at (-1, -1) and level 1', 'E vertex at (1, -1) and level 1'),
                          ('E vertex at (-1, -1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (-1, -1) and level 2', 'E vertex at (0.0, -1.0) and level 2'),
                          ('E vertex at (-1, -1) and level 2', 'i vertex at (-0.5, 0.0) and level 2'),
                          ('E vertex at (-1, -1) and level 3', 'E vertex at (-0.5, -1.0) and level 3'),
                          ('E vertex at (-1, -1) and level 3', 'I vertex at (-0.75, 0.0) and level 3'),
                          ('E vertex at (-1, 1) and level 1', 'E vertex at (-1, -1) and level 1'),
                          ('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
                          ('E vertex at (-1, 1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (-1, 1) and level 2', 'E vertex at (-1, -1) and level 2'),
                          ('E vertex at (-1, 1) and level 2', 'E vertex at (0.0, 1.0) and level 2'),
                          ('E vertex at (-1, 1) and level 2', 'i vertex at (-0.5, 0.0) and level 2'),
                          ('E vertex at (-1, 1) and level 3', 'E vertex at (-0.5, 1.0) and level 3'),
                          ('E vertex at (-1, 1) and level 3', 'E vertex at (-1, -1) and level 3'),
                          ('E vertex at (-1, 1) and level 3', 'I vertex at (-0.75, 0.0) and level 3'),
                          ('E vertex at (0.0, -1.0) and level 2', 'E vertex at (1, -1) and level 2'),
                          ('E vertex at (0.0, -1.0) and level 2', 'I vertex at (0.5, 0.0) and level 2'),
                          ('E vertex at (0.0, -1.0) and level 2', 'i vertex at (-0.5, 0.0) and level 2'),
                          ('E vertex at (0.0, -1.0) and level 3',
                           'I vertex at (-0.25, 0.0) and level 3'),
                          ('E vertex at (0.0, 1.0) and level 2', 'E vertex at (0.0, -1.0) and level 2'),
                          ('E vertex at (0.0, 1.0) and level 2', 'E vertex at (1, 1) and level 2'),
                          ('E vertex at (0.0, 1.0) and level 2', 'I vertex at (0.5, 0.0) and level 2'),
                          ('E vertex at (0.0, 1.0) and level 2', 'i vertex at (-0.5, 0.0) and level 2'),
                          ('E vertex at (0.0, 1.0) and level 3', 'E vertex at (0.0, -1.0) and level 3'),
                          ('E vertex at (0.0, 1.0) and level 3', 'I vertex at (-0.25, 0.0) and level 3'),
                          ('E vertex at (1, -1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (1, -1) and level 2', 'I vertex at (0.5, 0.0) and level 2'),
                          ('E vertex at (1, 1) and level 1', 'E vertex at (1, -1) and level 1'),
                          ('E vertex at (1, 1) and level 1', 'i vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (1, 1) and level 2', 'E vertex at (1, -1) and level 2'),
                          ('E vertex at (1, 1) and level 2', 'I vertex at (0.5, 0.0) and level 2'),
                          ('i vertex at (-0.5, 0.0) and level 2',
                           'I vertex at (-0.25, 0.0) and level 3'),
                          ('i vertex at (-0.5, 0.0) and level 2',
                           'I vertex at (-0.75, 0.0) and level 3'),
                          ('i vertex at (0.0, 0.0) and level 1', 'I vertex at (0.5, 0.0) and level 2'),
                          ('i vertex at (0.0, 0.0) and level 1', 'i vertex at (-0.5, 0.0) and level 2')]

        g = self.graph.P1().P2(1).P2(2)
        g.showLevel(2)
        g.showLevel(3)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(g, expected_nodes, expected_edges)

    def test_p1_p2_horizontal_for_incomplete_graph_with_removed_vertex(self):
        expected_tiers = ['[e vertex at (0, 0) and level 0]',
                          '[E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex at (-1, -1) and level 1, E vertex at (1, -1) and level 1, I vertex at (0.0, 0.0) and level 1]']

        expected_nodes = ['e vertex at (0, 0) and level 0',
                          'E vertex at (-1, 1) and level 1',
                          'E vertex at (1, 1) and level 1',
                          'E vertex at (-1, -1) and level 1',
                          'I vertex at (0.0, 0.0) and level 1']

        expected_edges = [('E vertex at (-1, -1) and level 1', 'I vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (-1, 1) and level 1', 'E vertex at (-1, -1) and level 1'),
                          ('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
                          ('E vertex at (-1, 1) and level 1', 'I vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (1, 1) and level 1', 'I vertex at (0.0, 0.0) and level 1')]

        g = self.graph.P1()
        g.showLevel(1)

        v4 = get_ith_vertex_from_graph(g, 4)
        g.graph.remove_node(v4)
        g.showLevel(1)
        g.P2(1, direction=Direction.HORIZONTAL)
        g.showLevel(1)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(g, expected_nodes, expected_edges)

    def test_p1_p2_vertical_for_incomplete_graph_with_removed_edge(self):
        expected_tiers = ['[e vertex at (0, 0) and level 0]',
                          '[E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex at (-1, -1) and level 1, E vertex at (1, -1) and level 1, I vertex at (0.0, 0.0) and level 1]']

        expected_nodes = ['e vertex at (0, 0) and level 0',
                          'E vertex at (-1, 1) and level 1',
                          'E vertex at (1, 1) and level 1',
                          'E vertex at (-1, -1) and level 1',
                          'E vertex at (1, -1) and level 1',
                          'I vertex at (0.0, 0.0) and level 1']

        expected_edges = [('E vertex at (-1, -1) and level 1', 'I vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (-1, 1) and level 1', 'E vertex at (-1, -1) and level 1'),
                          ('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
                          ('E vertex at (-1, 1) and level 1', 'I vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (1, -1) and level 1', 'I vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (1, 1) and level 1', 'E vertex at (1, -1) and level 1'),
                          ('E vertex at (1, 1) and level 1', 'I vertex at (0.0, 0.0) and level 1')]

        g = self.graph.P1()
        g.showLevel(1)

        v3 = get_ith_vertex_from_graph(g, 3)
        v4 = get_ith_vertex_from_graph(g, 4)
        g.graph.remove_edge(v3, v4)
        g.showLevel(1)
        g.P2(1)
        g.showLevel(1)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(g, expected_nodes, expected_edges)

    def test_p1_p2_horizontal_for_incomplete_graph_with_changed_label(self):
        expected_tiers = ['[e vertex at (0, 0) and level 0]',
                          '[E vertex at (-1, 1) and level 1, E vertex at (1, 1) and level 1, E vertex at (-1, -1) and level 1, U vertex at (1, -1) and level 1, I vertex at (0.0, 0.0) and level 1]']

        expected_nodes = ['e vertex at (0, 0) and level 0',
                          'E vertex at (-1, 1) and level 1',
                          'E vertex at (1, 1) and level 1',
                          'E vertex at (-1, -1) and level 1',
                          'U vertex at (1, -1) and level 1',
                          'I vertex at (0.0, 0.0) and level 1']

        expected_edges = [('E vertex at (-1, -1) and level 1', 'I vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (-1, -1) and level 1', 'U vertex at (1, -1) and level 1'),
                          ('E vertex at (-1, 1) and level 1', 'E vertex at (-1, -1) and level 1'),
                          ('E vertex at (-1, 1) and level 1', 'E vertex at (1, 1) and level 1'),
                          ('E vertex at (-1, 1) and level 1', 'I vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (1, 1) and level 1', 'I vertex at (0.0, 0.0) and level 1'),
                          ('E vertex at (1, 1) and level 1', 'U vertex at (1, -1) and level 1'),
                          ('U vertex at (1, -1) and level 1', 'I vertex at (0.0, 0.0) and level 1')]

        g = self.graph.P1()

        v4 = get_ith_vertex_from_graph(g, 4)
        v4.label = "U"
        g.graph.add_node(v4)
        g.showLevel(1)

        g = self.graph.P2(1, direction=Direction.HORIZONTAL)
        g.showLevel(1)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(g, expected_nodes, expected_edges)


if __name__ == '__main__':
    unittest.main()

    # TODO:
    #  - ZAD.2: ogarnąć znajdowanie grafów izomorficznych - żeby się dało wybrać, na którym poziomie i w którym miejscu wykonujemy produkcję
    #  - produkcja nr 9?
