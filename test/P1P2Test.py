import unittest

from visualization import TieredGraph


class P1P2Test(unittest.TestCase):

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

    def test_p1(self):
        expected_tiers = ['[red e vertex at (0, 0)]',
                          '[blue E vertex at (-1, 1), blue E vertex at (1, 1), blue E vertex at (-1, -1), blue E vertex at (1, -1), red I vertex at (0.0, 0.0)]']

        expected_nodes = ['red e vertex at (0, 0)', 'blue E vertex at (-1, 1)', 'blue E vertex at (1, 1)',
                          'blue E vertex at (-1, -1)', 'blue E vertex at (1, -1)',
                          'red I vertex at (0.0, 0.0)']

        expected_edges = [('blue E vertex at (-1, 1)', 'blue E vertex at (1, 1)'),
                          ('blue E vertex at (-1, 1)', 'blue E vertex at (-1, -1)'),
                          ('blue E vertex at (-1, 1)', 'red I vertex at (0.0, 0.0)'),
                          ('blue E vertex at (1, 1)', 'blue E vertex at (1, -1)'),
                          ('blue E vertex at (1, 1)', 'red I vertex at (0.0, 0.0)'),
                          ('blue E vertex at (-1, -1)', 'blue E vertex at (1, -1)'),
                          ('blue E vertex at (-1, -1)', 'red I vertex at (0.0, 0.0)'),
                          ('blue E vertex at (1, -1)', 'red I vertex at (0.0, 0.0)')]

        g = self.graph.P1()
        g.showLevel(1)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)

    def test_p1_p2(self):
        expected_tiers = ['[red e vertex at (0, 0)]',
                          '[blue E vertex at (-1, 1), blue E vertex at (1, 1), blue E vertex at (-1, -1), blue E vertex at (1, -1), red i vertex at (0.0, 0.0)]',
                          '[blue E vertex at (-1, 1), blue E vertex at (0.0, 1.0), blue E vertex at (1, 1), blue E vertex at (-1, -1), blue E vertex at (0.0, -1.0), blue E vertex at (1, -1), red I vertex at (-0.5, 0.0), red I vertex at (0.5, 0.0)]']

        expected_nodes = ['red e vertex at (0, 0)', 'blue E vertex at (-1, 1)', 'blue E vertex at (1, 1)',
                          'blue E vertex at (-1, -1)', 'blue E vertex at (1, -1)', 'red i vertex at (0.0, 0.0)',
                          'blue E vertex at (-1, 1)', 'blue E vertex at (0.0, 1.0)', 'blue E vertex at (1, 1)',
                          'blue E vertex at (-1, -1)', 'blue E vertex at (0.0, -1.0)', 'blue E vertex at (1, -1)',
                          'red I vertex at (-0.5, 0.0)', 'red I vertex at (0.5, 0.0)']

        expected_edges = [('blue E vertex at (-1, 1)', 'blue E vertex at (1, 1)'),
                          ('blue E vertex at (-1, 1)', 'blue E vertex at (-1, -1)'),
                          ('blue E vertex at (-1, 1)', 'red i vertex at (0.0, 0.0)'),
                          ('blue E vertex at (1, 1)', 'blue E vertex at (1, -1)'),
                          ('blue E vertex at (1, 1)', 'red i vertex at (0.0, 0.0)'),
                          ('blue E vertex at (-1, -1)', 'blue E vertex at (1, -1)'),
                          ('blue E vertex at (-1, -1)', 'red i vertex at (0.0, 0.0)'),
                          ('blue E vertex at (1, -1)', 'red i vertex at (0.0, 0.0)'),
                          # ('red i vertex at (0.0, 0.0)', 'red I vertex at (-0.5, 0.0)'), fixme
                          # ('red i vertex at (0.0, 0.0)', 'red I vertex at (0.5, 0.0)'),
                          ('blue E vertex at (-1, 1)', 'blue E vertex at (0.0, 1.0)'),
                          ('blue E vertex at (-1, 1)', 'blue E vertex at (-1, -1)'),
                          ('blue E vertex at (-1, 1)', 'red I vertex at (-0.5, 0.0)'),
                          ('blue E vertex at (0.0, 1.0)', 'blue E vertex at (1, 1)'),
                          ('blue E vertex at (0.0, 1.0)', 'blue E vertex at (0.0, -1.0)'),
                          ('blue E vertex at (0.0, 1.0)', 'red I vertex at (-0.5, 0.0)'),
                          ('blue E vertex at (0.0, 1.0)', 'red I vertex at (0.5, 0.0)'),
                          ('blue E vertex at (1, 1)', 'blue E vertex at (1, -1)'),
                          ('blue E vertex at (1, 1)', 'red I vertex at (0.5, 0.0)'),
                          ('blue E vertex at (-1, -1)', 'blue E vertex at (0.0, -1.0)'),
                          ('blue E vertex at (-1, -1)', 'red I vertex at (-0.5, 0.0)'),
                          ('blue E vertex at (0.0, -1.0)', 'blue E vertex at (1, -1)'),
                          ('blue E vertex at (0.0, -1.0)', 'red I vertex at (-0.5, 0.0)'),
                          ('blue E vertex at (0.0, -1.0)', 'red I vertex at (0.5, 0.0)'),
                          ('blue E vertex at (1, -1)', 'red I vertex at (0.5, 0.0)')]
        self.graph.P1()
        g = self.graph.P2()
        g.showLevel(2)
        g.show()

        self.validate_tiers(g, expected_tiers)
        self.validate_graph(expected_nodes, expected_edges)


if __name__ == '__main__':
    unittest.main()

    # TODO:
    #  - naprawić walidację krawędzi
    #  - ogarnąć znajdowanie grafów izomorficznych
    #  - ogarnąc łamania w pionie i poziomie w P2
    #  - test do P1 P2 P2 P2
    #  - lepsze testy: z grafami, do których nie da się podgrafów dodać, ogólnie dla większego grafu ma działać, zmienić etykietę jednego wierzchołka, brak jakiejś krawędzi
    #  - czy __eq__ jest ok??
