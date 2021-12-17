import unittest

from visualization import TieredGraph


class P1P2Test(unittest.TestCase):

    def setUp(self):
        v1 = (-1, 1)
        v2 = (1, 1)
        v3 = (-1, -1)
        v4 = (1, -1)
        self.graph = TieredGraph((v1, v2, v3, v4))

    def test_p1(self):
        g = self.graph.P1()
        g.showLevel(1)

        self.assertEqual(dict(g.graph.nodes),
                         {"red e vertex at (0, 0)": {}, "blue E vertex at (-1, 1)": {}, "blue E vertex at (1, 1)": {},
                          "blue E vertex at (-1, -1)": {}, "blue E vertex at (1, -1)": {},
                          "red I vertex at (0.0, 0.0)": {}})

    def test_p1_p2(self):
        self.graph.P1()
        g = self.graph.P2()
        g.showLevel(2)
        self.assertEqual(['[red e vertex at (0, 0)]',
                          '[blue E vertex at (-1, 1), blue E vertex at (1, 1), blue E vertex at (-1, -1), blue E vertex at (1, -1), red i vertex at (0.0, 0.0)]',
                          '[green E vertex at (-1, 1), green FFF vertex at (0.0, 1.0), green E vertex at (1, 1), green E vertex at (-1, -1), green GGG vertex at (0.0, -1.0), green E vertex at (1, -1), orange I vertex at (-0.5, 0.0), orange I vertex at (0.5, 0.0)]'],
                         list(map(lambda vertex: vertex.__repr__(), g.tiers)))


if __name__ == '__main__':
    unittest.main()
