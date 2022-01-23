from enum import Enum

import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D




class Direction(Enum):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'


class Production(Enum):
    P1 = 'P1'
    P2 = 'P2'
    P3 = 'P3'
    P4 = 'P4'
    P9 = 'P9'
    P10 = 'P10'

    def __repr__(self):
        return self.name


class Vertex:
    def __init__(self, position: tuple((int, int)), label: str, level: int, id=[0]):
        self.label = label
        self.position = position
        self.level = level
        self.id = id[0]
        id[0] += 1

    @property
    def levelPosTuple(self):
        return (self.position[0], self.position[1], -self.level)


    def __hash__(self) -> int:
        # NetworkX identifies vertices by hash
        return hash(self.id)

    def __eq__(self, G2_node):
        # TODO: porównywać po odległościach między wierzchołkami??? bo trzeba chyba sprawdzić, czy w środku grafu jest I czy i?
        return self.label == G2_node.label and self.level == G2_node.level

    def __repr__(self):
        return f"{self.label} vertex at {self.position} and level {self.level}"




class GraphMatcherByLabel(nx.isomorphism.GraphMatcher):
    def __init__(self, graph1, graph2):
        super().__init__(graph1, graph2)

    def semantic_feasibility(self, G1_node, G2_node):
        return G1_node.label == G2_node.label and G2_node.level == G2_node.level


class TieredGraph:
    def __init__(self, corners: tuple):
        self.graph = nx.Graph()
        starting_vertex = Vertex((0, 0), "E", 0)
        self.graph.add_node(starting_vertex)
        self.corners = corners
        self.tiers = []
        self.tiers.append([starting_vertex])
        self.productions = []

    def show3d(self):
        # The graph to visualize
        G = self.graph

        # 3d spring layout
        pos = nx.spring_layout(G, dim=3, seed=779)
        # Extract node and edge positions from the layout
        node_xyz = np.array([v.levelPosTuple for v in G.nodes()])
        edge_xyz = np.array([(u.levelPosTuple, v.levelPosTuple) for u, v in G.edges()])
        colors = [self.color_mapping[(node.level, node.label)] for node in G.nodes()]

        # Create the 3D figure
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        # Plot the nodes - alpha is scaled by "depth" automatically
        ax.scatter(*node_xyz.T, s=100, ec="w", c = colors)

        # Plot the edges
        for vizedge in edge_xyz:
            ax.plot(*vizedge.T, color="tab:gray")

        self._format_axes(ax)
        fig.tight_layout()
        plt.show()

    def _format_axes(self, ax):
        """Visualization options for the 3D axes."""
        # Turn gridlines off
        ax.grid(False)
        # Suppress tick labels
        for dim in (ax.xaxis, ax.yaxis, ax.zaxis):
            dim.set_ticks([])
        # Set axes labels
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

    @property
    def color_mapping(self):
        return {
            (0, "E"): "red",
            (0, "e"): "red",
            (1, "E"): "blue",
            (1, "I"): "red",
            (1, "i"): "red",
            (2, "E"): "green",
            (2, "I"): "orange",
            (2, "i"): "orange",
            (3, "E"): "red",
            (3, "I"): "blue",
            (3, "i"): "blue",
            # vertices labelled incorrectly:
            (0, "U"): "yellow",
            (1, "U"): "yellow"
        }

    def show(self):
        fig, ax = plt.subplots()
        xs, ys = zip(*[node.position for node in self.graph.nodes])
        colors = [self.color_mapping[(node.level, node.label)] for node in self.graph.nodes]
        labels = [node.label for node in self.graph.nodes]
        xs = list(xs)
        ys = list(ys)

        for edge in self.graph.edges:
            ax.plot([edge[0].position[0], edge[1].position[0]], [edge[0].position[1], edge[1].position[1]],
                    color="black", zorder=1)

        ax.scatter(xs, ys, c=colors, s=200, zorder=2)

        for i, label in enumerate(labels):
            ax.annotate(label, (xs[i], ys[i]))

        plt.title(f"Whole graph after productions {self.productions}")
        plt.show()

    def showLevel(self, level: int):
        levelNodes = [node for node in self.graph.nodes if node in self.tiers[level]]
        graph = self.graph.subgraph(levelNodes)

        fig, ax = plt.subplots()
        xs, ys = zip(*[node.position for node in graph.nodes])
        colors = [self.color_mapping[(node.level, node.label)] for node in graph.nodes]
        labels = [node.label for node in graph.nodes]
        xs = list(xs)
        ys = list(ys)

        edges = [edge for edge in graph.edges if edge[0] in levelNodes and edge[1] in levelNodes]
        for edge in edges:
            ax.plot([edge[0].position[0], edge[1].position[0]], [edge[0].position[1], edge[1].position[1]],
                    color="black", zorder=1)

        ax.scatter(xs, ys, c=colors, s=200, zorder=2)

        for i, label in enumerate(labels):
            ax.annotate(label, (xs[i], ys[i]))

        plt.title(f"Graph at level {level} after productions {self.productions}")
        plt.show()

    def P1(self):
        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))

        matches = GraphMatcherByLabel(self.graph, LHS).subgraph_isomorphisms_iter()

        try:
            match = next(matches)
        except StopIteration:
            print(f"P1: No match for {v0} found!")
            return self

        RHS = nx.Graph()
        RHS.add_node(v0 := Vertex(list(match.keys())[0].position, "e", 0))
        RHS.add_node(v1 := Vertex(self.corners[0], "E", 1))
        RHS.add_node(v2 := Vertex(self.corners[1], "E", 1))
        RHS.add_node(v3 := Vertex(self.corners[2], "E", 1))
        RHS.add_node(v4 := Vertex(self.corners[3], "E", 1))

        RHS.add_node(
            i := Vertex(((self.corners[0][0] + self.corners[1][0]) / 2, (self.corners[0][1] + self.corners[2][1]) / 2),
                        "I", 1))
        RHS.add_edges_from([(v1, v2), (v2, v4), (v4, v3), (v3, v1),
                            (v1, i), (v2, i), (v3, i), (v4, i), (v0, i)])
        self.tiers[0] = [v0]
        self.tiers.append([v1, v2, v3, v4, i])  # appending RHS to first level

        self.graph = RHS
        self.productions.append(Production.P1)

        return self

    def P2(self, level, direction=Direction.VERTICAL):  # TODO: uwzględnić poziom, na którym ma się wykonać produkcja

        LHS = nx.Graph()
        LHS.add_node(v1 := Vertex(None, "E", level))
        LHS.add_node(v2 := Vertex(None, "E", level))
        LHS.add_node(v3 := Vertex(None, "E", level))
        LHS.add_node(v4 := Vertex(None, "E", level))
        LHS.add_node(i := Vertex(None, "I", level))

        LHS.add_edges_from([(v1, v2), (v2, v4), (v3, v4), (v1, v3),
                            (v1, i), (v2, i), (v3, i), (v4, i)])

        matches = GraphMatcherByLabel(self.graph, LHS).subgraph_isomorphisms_iter()
        try:
            match = next(matches)
            if direction == Direction.HORIZONTAL:
                while list(match.keys())[0].position[0] != list(match.keys())[1].position[0]:
                    match = next(matches)
            elif direction == Direction.VERTICAL:
                while list(match.keys())[0].position[1] != list(match.keys())[1].position[1]:
                    match = next(matches)
        except StopIteration:
            print(f"P2: No match for {LHS} found!")
            return self

        # change I -> i
        matched_i = [v for v in list(match.keys()) if v.label == "I"]
        matched_i[0].label = "i"

        print(f"Isomorfic matched graph {match}")

        for k, v in match.items():
            v.position = k.position

        RHS = nx.Graph()
        RHS.add_node(new_v1 := Vertex(v1.position, "E", level + 1))
        RHS.add_node(
            new_v1_5 := Vertex(((v1.position[0] + v2.position[0]) / 2, (v1.position[1] + v2.position[1]) / 2), "E",
                               level + 1))
        RHS.add_node(new_v2 := Vertex(v2.position, "E", level + 1))
        RHS.add_node(new_v3 := Vertex(v3.position, "E", level + 1))
        RHS.add_node(
            new_v3_5 := Vertex(((v3.position[0] + v4.position[0]) / 2, (v3.position[1] + v4.position[1]) / 2), "E",
                               level + 1))
        RHS.add_node(new_v4 := Vertex(v4.position, "E", level + 1))

        if direction == Direction.HORIZONTAL:
            RHS.add_node(new_i_left := Vertex(
                ((new_v1.position[0] + new_v3.position[0]) / 2, (new_v1.position[1] + new_v1_5.position[1]) / 2), "I",
                level + 1))

            RHS.add_node(new_i_right := Vertex(
                ((new_v1_5.position[0] + new_v3_5.position[0]) / 2, (new_v1_5.position[1] + new_v2.position[1]) / 2), "I",
                level + 1))
        else:
            RHS.add_node(new_i_left := Vertex(
                ((new_v1.position[0] + new_v1_5.position[0]) / 2, (new_v1.position[1] + new_v3.position[1]) / 2), "I",
                level + 1))

            RHS.add_node(new_i_right := Vertex(
                ((new_v1_5.position[0] + new_v2.position[0]) / 2, (new_v1_5.position[1] + new_v3_5.position[1]) / 2), "I",
                level + 1))

        edges = [(new_v1, new_v1_5), (new_v1_5, new_v2), (new_v1, new_v3), (new_v3, new_v3_5), (new_v1_5, new_v3_5),
                 (new_v3_5, new_v4), (new_v2, new_v4),
                 (new_v1, new_i_left), (new_v1_5, new_i_left), (new_v3, new_i_left), (new_v3_5, new_i_left),
                 (new_v1_5, new_i_right), (new_v2, new_i_right), (new_v3_5, new_i_right), (new_v4, new_i_right)]
        RHS.add_edges_from(edges)

        # appending RHS to new level - powinno uwzględniać poziom "parenta"
        if level+1 >= len(self.tiers):
            self.tiers.append([])
        self.tiers[level+1].extend([new_v1, new_v1_5, new_v2, new_v3, new_v3_5, new_v4, new_i_left, new_i_right])
        print(f"Tiers after P2 {self.tiers}")

        # add edges between layers (between i and Is)
        self.graph.add_edges_from(edges)
        self.graph.add_edges_from([(matched_i[0], new_i_left), (matched_i[0], new_i_right)])

        self.productions.append(Production.P2)
        return self

    def P3(self, level):
        LHS = nx.Graph()
        LHS.add_node(v1 := Vertex(None, "E", level))
        LHS.add_node(v2 := Vertex(None, "E", level))
        LHS.add_node(v3 := Vertex(None, "E", level))
        LHS.add_node(v4 := Vertex(None, "E", level))
        LHS.add_node(i := Vertex(None, "I", level))

        LHS.add_edges_from([(v1, v2), (v2, v4), (v3, v4), (v1, v3), (v1, i), (v2, i), (v3, i), (v4, i)])

        matches = GraphMatcherByLabel(self.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P2: No match for {LHS} found!"

        # change I -> i
        matched_i = [v for v in list(match.keys()) if v.label == "I"]
        matched_i[0].label = "i"

        print(f"Isomorfic matched graph {match}")

        for k, v in match.items():
            v.position = k.position

        RHS = nx.Graph()
        RHS.add_node(new_v1 := Vertex(v1.position, "E", level + 1))
        RHS.add_node(new_v1_5 := Vertex(((v1.position[0] + v2.position[0]) / 2, (v1.position[1] + v2.position[1]) / 2), "E", level + 1))
        RHS.add_node(new_v2 := Vertex(v2.position, "E", level + 1))
        RHS.add_node(new_v3 := Vertex(v3.position, "E", level + 1))
        RHS.add_node(new_v3_5 := Vertex(((v3.position[0] + v4.position[0]) / 2, (v3.position[1] + v4.position[1]) / 2), "E", level + 1))
        RHS.add_node(new_v4 := Vertex(v4.position, "E", level + 1))

        RHS.add_node(new_v5 := Vertex(((v1.position[0] + v3.position[0]) / 2, (v1.position[1] + v3.position[1]) / 2), "E", level + 1))
        RHS.add_node(new_v5_5 := Vertex(((v1.position[0] + v4.position[0]) / 2, (v1.position[1] + v4.position[1]) / 2), "E", level + 1))
        RHS.add_node(new_v6 := Vertex(((v2.position[0] + v4.position[0]) / 2, (v2.position[1] + v4.position[1]) / 2), "E", level + 1))

        RHS.add_node(new_i_left := Vertex(((new_v1.position[0] + new_v1_5.position[0]) / 2, (new_v1.position[1] + new_v5.position[1]) / 2), "I", level + 1))
        RHS.add_node(new_i_right := Vertex(((new_v1_5.position[0] + new_v2.position[0]) / 2, (new_v1_5.position[1] + new_v5_5.position[1]) / 2), "I", level + 1))

        RHS.add_node(new_i_bottom_left := Vertex(((new_v1.position[0] + new_v1_5.position[0]) / 2, (new_v5.position[1] + new_v3.position[1]) / 2), "I", level + 1))
        RHS.add_node(new_i_bottom_right := Vertex(((new_v1_5.position[0] + new_v2.position[0]) / 2, (new_v5_5.position[1] + new_v3_5.position[1]) / 2), "I", level + 1))

        edges = [
            (new_v1, new_v1_5),
            (new_v1_5, new_v2),
            (new_v2, new_v6),
            (new_v6, new_v4),
            (new_v4, new_v3_5),
            (new_v3_5, new_v3),
            (new_v3, new_v5),
            (new_v5, new_v1),

            (new_v5_5, new_v1_5),
            (new_v5_5, new_v5),
            (new_v5_5, new_v6),
            (new_v5_5, new_v3_5),

            (new_i_left, new_v1),
            (new_i_left, new_v1_5),
            (new_i_left, new_v5_5),
            (new_i_left, new_v5),

            (new_i_right, new_v1_5),
            (new_i_right, new_v2),
            (new_i_right, new_v6),
            (new_i_right, new_v5_5),

            (new_i_bottom_left, new_v5),
            (new_i_bottom_left, new_v5_5),
            (new_i_bottom_left, new_v3_5),
            (new_i_bottom_left, new_v3),

            (new_i_bottom_right, new_v5_5),
            (new_i_bottom_right, new_v6),
            (new_i_bottom_right, new_v4),
            (new_i_bottom_right, new_v3_5),
        ]

        RHS.add_edges_from(edges)

        # appending RHS to new level - powinno uwzględniać poziom "parenta"
        self.tiers.append([new_v1, new_v1_5, new_v2, new_v3, new_v3_5, new_v4, new_v5, new_v5_5, new_v6, new_i_left, new_i_right, new_i_bottom_left, new_i_bottom_right])
        print(f"Tiers after P3 {self.tiers}")

        # add edges between layers (between i and Is)
        self.graph.add_edges_from(edges)
        self.graph.add_edges_from([(matched_i[0], new_i_left), (matched_i[0], new_i_right)])

        self.productions.append(Production.P3)
        return self

    def P4(self, level):
        LHS = nx.Graph()
        LHS.add_node(v1 := Vertex(None, "E", level))
        LHS.add_node(v1_5 := Vertex(None, "E", level))
        LHS.add_node(v2 := Vertex(None, "E", level))
        LHS.add_node(v3 := Vertex(None, "E", level))
        LHS.add_node(v4 := Vertex(None, "E", level))
        LHS.add_node(i := Vertex(None, "I", level))

        LHS.add_edges_from([(v1, v1_5), (v1_5, v2), (v2, v4), (v3, v4), (v1, v3), (v1, i), (v2, i), (v3, i), (v4, i)])

        matches = GraphMatcherByLabel(self.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P2: No match for {LHS} found!"

        # change I -> i
        matched_i = [v for v in list(match.keys()) if v.label == "I"]
        matched_i[0].label = "i"

        print(f"Isomorfic matched graph {match}")

        for k, v in match.items():
            v.position = k.position

        RHS = nx.Graph()
        RHS.add_node(new_v1 := Vertex(v1.position, "E", level + 1))
        RHS.add_node(new_v1_5 := Vertex(v1_5.position, "E", level + 1))
        RHS.add_node(new_v2 := Vertex(v2.position, "E", level + 1))
        RHS.add_node(new_v3 := Vertex(v3.position, "E", level + 1))
        RHS.add_node(new_v3_5 := Vertex(((v3.position[0] + v4.position[0]) / 2, (v3.position[1] + v4.position[1]) / 2), "E", level + 1))
        RHS.add_node(new_v4 := Vertex(v4.position, "E", level + 1))

        RHS.add_node(new_i_left := Vertex(((new_v1.position[0] + new_v1_5.position[0]) / 2, (new_v1.position[1] + new_v3.position[1]) / 2), "I", level + 1))

        RHS.add_node(new_i_right := Vertex(((new_v1_5.position[0] + new_v2.position[0]) / 2, (new_v1_5.position[1] + new_v3_5.position[1]) / 2), "I", level + 1))

        edges = [
            (new_v1, new_v1_5),
            (new_v1_5, new_v2),
            (new_v1, new_v3),
            (new_v3, new_v3_5),
            (new_v1_5, new_v3_5),
            (new_v3_5, new_v4),
            (new_v2, new_v4),
            (new_v1, new_i_left),
            (new_v1_5, new_i_left),
            (new_v3, new_i_left),
            (new_v3_5, new_i_left),
            (new_v1_5, new_i_right),
            (new_v2, new_i_right),
            (new_v3_5, new_i_right),
            (new_v4, new_i_right),
        ]
        RHS.add_edges_from(edges)

        # appending RHS to new level - powinno uwzględniać poziom "parenta"
        self.tiers.append([new_v1, new_v1_5, new_v2, new_v3, new_v3_5, new_v4, new_i_left, new_i_right])
        print(f"Tiers after P4 {self.tiers}")

        # add edges between layers (between i and Is)
        self.graph.add_edges_from(edges)
        self.graph.add_edges_from([(matched_i[0], new_i_left), (matched_i[0], new_i_right)])

        self.productions.append(Production.P4)
        return self


    def P7(self, level):
        LHS = nx.Graph()
        LHS.add_node(v1 := Vertex(None, "E", level))
        LHS.add_node(v1_5 := Vertex(None, "E", level))
        LHS.add_node(v2 := Vertex(None, "E", level))
        LHS.add_node(v2_5 := Vertex(None, "E", level))
        LHS.add_node(v3 := Vertex(None, "E", level))
        LHS.add_node(v4 := Vertex(None, "E", level))
        LHS.add_node(v3_5 := Vertex(None, "E", level))
        LHS.add_node(i := Vertex(None, "I", level))

        LHS.add_edges_from([(v1, v1_5), (v1_5, v2), (v2, v2_5), (v2_5, v4), (v3, v4), (v1, v3_5), (v3, v3_5),
                            (v1, i), (v2, i), (v3, i), (v4, i)])

        matches = GraphMatcherByLabel(self.graph, LHS).subgraph_isomorphisms_iter()

        # match = None
        try:
            match = next(matches)
        except StopIteration:
            print(f"P7: No match for found!")
            return self
        # assert match is not None, f"P7: No match for {LHS} found!"

        # change I -> i
        matched_i = [v for v in list(match.keys()) if v.label == "I"]
        matched_i[0].label = "i"

        print(f"Isomorfic matched graph {match}")

        for k, v in match.items():
            v.position = k.position

        if (((v1.position[0] + v2.position[0]) / 2, (v1.position[1] + v2.position[1]) / 2) != v1_5.position) or \
            (((v2.position[0] + v4.position[0]) / 2, (v2.position[1] + v4.position[1]) / 2) != v2_5.position) or \
                (((v1.position[0] + v3.position[0]) / 2, (v1.position[1] + v3.position[1]) / 2) != v3_5.position):
            print(f"P7: One of vertices is not on middle!")
            return self

        RHS = nx.Graph()
        RHS.add_node(new_v1 := Vertex(v1.position, "E", level + 1))
        RHS.add_node(new_v1_5 := Vertex(((v1.position[0] + v2.position[0]) / 2, (v1.position[1] + v2.position[1]) / 2), "E", level + 1))
        RHS.add_node(new_v2 := Vertex(v2.position, "E", level + 1))
        RHS.add_node(new_v2_5 := Vertex(((v2.position[0] + v4.position[0])/ 2, (v2.position[1] + v4.position[1])/ 2), "E", level + 1))
        RHS.add_node(new_v3 := Vertex(v3.position, "E", level + 1))
        RHS.add_node(new_v3_5 := Vertex(((v1.position[0] + v3.position[0]) / 2, (v1.position[1] + v3.position[1]) / 2), "E", level + 1))
        RHS.add_node(new_v4 := Vertex(v4.position, "E", level + 1))

        RHS.add_node(new_v4_5 := Vertex(((v3.position[0] + v4.position[0]) / 2, (v3.position[1] + v4.position[1]) / 2), "E", level + 1))
        RHS.add_node(new_v5 := Vertex(((v1.position[0] + v4.position[0]) / 2, (v1.position[1] + v4.position[1]) / 2), "E", level + 1))

        RHS.add_node(new_i_top_left := Vertex(((new_v1.position[0] + new_v5.position[0]) / 2, (new_v1.position[1] + new_v5.position[1]) / 2), "I", level + 1))
        RHS.add_node(new_i_top_right := Vertex(((new_v2.position[0] + new_v5.position[0]) / 2, (new_v2.position[1] + new_v5.position[1]) / 2), "I", level + 1))

        RHS.add_node(new_i_bottom_left := Vertex(((new_v3.position[0] + new_v5.position[0]) / 2, (new_v3.position[1] + new_v5.position[1]) / 2), "I", level + 1))
        RHS.add_node(new_i_bottom_right := Vertex(((new_v4.position[0] + new_v5.position[0]) / 2, (new_v4.position[1] + new_v5.position[1]) / 2), "I", level + 1))

        edges = [
            (new_v1, new_v1_5),
            (new_v1_5, new_v2),
            (new_v2, new_v2_5),
            (new_v2_5, new_v4),
            (new_v4, new_v4_5),
            (new_v4_5, new_v3),
            (new_v3, new_v3_5),
            (new_v3_5, new_v1),

            (new_v5, new_v1_5),
            (new_v5, new_v2_5),
            (new_v5, new_v4_5),
            (new_v5, new_v3_5),

            (new_i_top_left, new_v1),
            (new_i_top_left, new_v1_5),
            (new_i_top_left, new_v3_5),
            (new_i_top_left, new_v5),

            (new_i_top_right, new_v1_5),
            (new_i_top_right, new_v2),
            (new_i_top_right, new_v2_5),
            (new_i_top_right, new_v5),

            (new_i_bottom_left, new_v5),
            (new_i_bottom_left, new_v3_5),
            (new_i_bottom_left, new_v4_5),
            (new_i_bottom_left, new_v3),

            (new_i_bottom_right, new_v5),
            (new_i_bottom_right, new_v2_5),
            (new_i_bottom_right, new_v4_5),
            (new_i_bottom_right, new_v4),
        ]

        RHS.add_edges_from(edges)

        # add edges between layers (between i and Is)
        self.tiers.append([new_v1, new_v1_5, new_v2, new_v3, new_v3_5, new_v4, new_v5, new_v2_5, new_v4_5, new_i_top_left, new_i_top_right, new_i_bottom_left, new_i_bottom_right])
        print(f"Tiers after P7 {self.tiers}")

        # add edges between layers (between i and Is)
        self.graph.add_edges_from(edges)
        self.graph.add_edges_from([(matched_i[0], new_i_top_left), (matched_i[0], new_i_top_right),  (matched_i[0], new_i_bottom_right),  (matched_i[0], new_i_bottom_right)])

        return self

    def P8(self, level):
        LHS = nx.Graph()
        LHS.add_node(v1 := Vertex(None, "E", level))
        LHS.add_node(v1_5 := Vertex(None, "E", level))
        LHS.add_node(v2 := Vertex(None, "E", level))
        LHS.add_node(v2_5 := Vertex(None, "E", level))
        LHS.add_node(v3 := Vertex(None, "E", level))
        LHS.add_node(v4_5 := Vertex(None, "E", level))
        LHS.add_node(v4 := Vertex(None, "E", level))
        LHS.add_node(v3_5 := Vertex(None, "E", level))
        LHS.add_node(i := Vertex(None, "I", level))

        LHS.add_edges_from([(v1, v1_5), (v1_5, v2), (v2, v2_5), (v2_5, v4), (v1, v3_5), (v3, v3_5), (v3, v4_5), (v4, v4_5),
                            (v1, i), (v2, i), (v3, i), (v4, i)])

        matches = GraphMatcherByLabel(self.graph, LHS).subgraph_isomorphisms_iter()
        try:
            match = next(matches)
        except StopIteration:
            print(f"P8: No match for found!")
            return self

        # change I -> i
        matched_i = [v for v in list(match.keys()) if v.label == "I"]
        matched_i[0].label = "i"

        print(f"Isomorfic matched graph {match}")

        for k, v in match.items():
            v.position = k.position

        if (((v1.position[0] + v2.position[0]) / 2, (v1.position[1] + v2.position[1]) / 2) != v1_5.position) or \
            (((v2.position[0] + v4.position[0]) / 2, (v2.position[1] + v4.position[1]) / 2) != v2_5.position) or \
            (((v1.position[0] + v3.position[0]) / 2, (v1.position[1] + v3.position[1]) / 2) != v3_5.position) or \
                (((v3.position[0] + v4.position[0]) / 2, (v3.position[1] + v4.position[1]) / 2) != v4_5.position):
            print(f"P8: One of vertices is not on middle!")
            return self

        RHS = nx.Graph()
        RHS.add_node(new_v1 := Vertex(v1.position, "E", level + 1))
        RHS.add_node(new_v1_5 := Vertex(((v1.position[0] + v2.position[0]) / 2, (v1.position[1] + v2.position[1]) / 2), "E", level + 1))
        RHS.add_node(new_v2 := Vertex(v2.position, "E", level + 1))
        RHS.add_node(new_v2_5 := Vertex(((v2.position[0] + v4.position[0])/ 2, (v2.position[1] + v4.position[1])/ 2), "E", level + 1))
        RHS.add_node(new_v3 := Vertex(v3.position, "E", level + 1))
        RHS.add_node(new_v3_5 := Vertex(((v1.position[0] + v3.position[0]) / 2, (v1.position[1] + v3.position[1]) / 2), "E", level + 1))
        RHS.add_node(new_v4 := Vertex(v4.position, "E", level + 1))

        RHS.add_node(new_v4_5 := Vertex(((v3.position[0] + v4.position[0]) / 2, (v3.position[1] + v4.position[1]) / 2), "E", level + 1))
        RHS.add_node(new_v5 := Vertex(((v1.position[0] + v4.position[0]) / 2, (v1.position[1] + v4.position[1]) / 2), "E", level + 1))

        RHS.add_node(new_i_top_left := Vertex(((new_v1.position[0] + new_v5.position[0]) / 2, (new_v1.position[1] + new_v5.position[1]) / 2), "I", level + 1))
        RHS.add_node(new_i_top_right := Vertex(((new_v2.position[0] + new_v5.position[0]) / 2, (new_v2.position[1] + new_v5.position[1]) / 2), "I", level + 1))

        RHS.add_node(new_i_bottom_left := Vertex(((new_v3.position[0] + new_v5.position[0]) / 2, (new_v3.position[1] + new_v5.position[1]) / 2), "I", level + 1))
        RHS.add_node(new_i_bottom_right := Vertex(((new_v4.position[0] + new_v5.position[0]) / 2, (new_v4.position[1] + new_v5.position[1]) / 2), "I", level + 1))

        edges = [
            (new_v1, new_v1_5),
            (new_v1_5, new_v2),
            (new_v2, new_v2_5),
            (new_v2_5, new_v4),
            (new_v4, new_v4_5),
            (new_v4_5, new_v3),
            (new_v3, new_v3_5),
            (new_v3_5, new_v1),

            (new_v5, new_v1_5),
            (new_v5, new_v2_5),
            (new_v5, new_v4_5),
            (new_v5, new_v3_5),

            (new_i_top_left, new_v1),
            (new_i_top_left, new_v1_5),
            (new_i_top_left, new_v3_5),
            (new_i_top_left, new_v5),

            (new_i_top_right, new_v1_5),
            (new_i_top_right, new_v2),
            (new_i_top_right, new_v2_5),
            (new_i_top_right, new_v5),

            (new_i_bottom_left, new_v5),
            (new_i_bottom_left, new_v3_5),
            (new_i_bottom_left, new_v4_5),
            (new_i_bottom_left, new_v3),

            (new_i_bottom_right, new_v5),
            (new_i_bottom_right, new_v2_5),
            (new_i_bottom_right, new_v4_5),
            (new_i_bottom_right, new_v4),
        ]

        RHS.add_edges_from(edges)

        # add edges between layers (between i and Is)
        self.tiers.append([new_v1, new_v1_5, new_v2, new_v3, new_v3_5, new_v4, new_v5, new_v2_5, new_v4_5, new_i_top_left, new_i_top_right, new_i_bottom_left, new_i_bottom_right])
        print(f"Tiers after P8 {self.tiers}")

        # add edges between layers (between i and Is)
        self.graph.add_edges_from(edges)
        self.graph.add_edges_from([(matched_i[0], new_i_top_left), (matched_i[0], new_i_top_right),  (matched_i[0], new_i_bottom_right),  (matched_i[0], new_i_bottom_right)])

        return self

    def P9(self, level):
        LHS = nx.Graph()

        LHS.add_node(v1 := Vertex(None, "E", level))
        LHS.add_node(v1_1 := Vertex(None, "E", level))
        LHS.add_node(v2 := Vertex(None, "E", level))
        LHS.add_node(v2_2 := Vertex(None, "E", level))
        LHS.add_node(v3 := Vertex(None, "E", level))
        LHS.add_node(v3_3 := Vertex(None, "E", level))
        LHS.add_node(I_1 := Vertex(None, "I", level))
        LHS.add_node(I_2 := Vertex(None, "I", level))
        LHS.add_node(I_3 := Vertex(None, "I", level))
        LHS.add_node(I_4 := Vertex(None, "I", level))

        LHS.add_edges_from(
            [(I_1, v1), (I_1, v2), (I_2, v2), (I_2, v3), (I_3, v1_1), (I_3, v2_2), (I_4, v2_2), (I_4, v3_3), (v1, v2),
             (v2, v3), (v1_1, v2_2), (v2_2, v3_3)])

        matches = GraphMatcherByLabel(self.graph, LHS).subgraph_isomorphisms_iter()
        nodes_to_remove = []
        while match := next(matches):
            nodes_to_remove = []

            for k, v in match.items():
                v.position = k.position
                if v1_1.position == k.position or v2_2.position == k.position or v3_3.position == k.position:
                    nodes_to_remove.append(k)
            if v1_1.position == v1.position and v2.position == v2_2.position and v3_3.position == v3.position and v1.position[0]/2 + v3.position[0]/2 == v2.position[0] and v1.position[1]/2 + v3.position[1]/2 == v2.position[1]:
                break
        assert match is not None, f"P9: No match for {LHS} found!"
        print(match.items())

        RHS = nx.Graph()
        RHS.add_node(new_v1 := Vertex(v1.position, "E", level))
        RHS.add_node(new_v2 := Vertex(v2.position, "E", level))
        RHS.add_node(new_v3 := Vertex(v3.position, "E", level))
        RHS.add_node(new_I_1 := Vertex(I_1.position, "I", level))
        RHS.add_node(new_I_2 := Vertex(I_2.position, "I", level))
        RHS.add_node(new_I_3 := Vertex(I_3.position, "I", level))
        RHS.add_node(new_I_4 := Vertex(I_4.position, "I", level))

        v1_1_edges = [edge for edge in self.graph.edges.keys() if v1_1.__repr__() in [edge[0].__repr__(), edge[1].__repr__()]]
        v2_2_edges = [edge for edge in self.graph.edges.keys() if v2_2.__repr__() in [edge[0].__repr__(), edge[1].__repr__()]]
        v3_3_edges = [edge for edge in self.graph.edges.keys() if v3_3.__repr__() in [edge[0].__repr__(), edge[1].__repr__()]]

        edges = [(new_v1, new_I_1),
                 (new_v1, new_I_3),
                 (new_v1, new_v2),
                 (new_v2, new_I_1),
                 (new_v2, new_I_2),
                 (new_v2, new_I_3),
                 (new_v2, new_I_4),
                 (new_v2, new_v3),
                 (new_v3, new_I_2),
                 (new_v3, new_I_4)
                 ]

        RHS.add_edges_from(edges)

        verticesFromLevel = self.tiers[level]
        self.tiers[level] = [v for v in verticesFromLevel if v not in nodes_to_remove]

        # add edges between layers (between i and Is)
        self.graph.add_edges_from(edges)

        self.graph.remove_nodes_from(nodes_to_remove)

        print(f"Tiers after P9 {self.tiers}")
        self.productions.append(Production.P9)

        return self

    def P10(self, level):
        LHS = nx.Graph()

        LHS.add_node(v0 := Vertex(None, "E", level))
        LHS.add_node(v1 := Vertex(None, "E", level))
        LHS.add_node(v2 := Vertex(None, "E", level))
        LHS.add_node(v2_2 := Vertex(None, "E", level))
        LHS.add_node(v3 := Vertex(None, "E", level))
        LHS.add_node(v3_3 := Vertex(None, "E", level))
        LHS.add_node(I_1 := Vertex(None, "I", level))
        LHS.add_node(I_2 := Vertex(None, "I", level))
        LHS.add_node(I_3 := Vertex(None, "I", level))
        LHS.add_node(I_4 := Vertex(None, "I", level))

        LHS.add_node(I_0_1 := Vertex(None, "I", level))
        LHS.add_node(I_0_2 := Vertex(None, "I", level))

        LHS.add_edges_from(
            [(I_0_1, I_1), (I_0_1, I_2), (I_0_2, I_3), (I_0_2, I_4), (v0, I_0_1), (v0, I_0_2), (I_1, v1), (I_1, v2), (I_2, v2), (I_2, v3), (I_3, v1), (I_3, v2_2), (I_4, v2_2), (I_4, v3_3), (v1, v2),
             (v2, v3), (v1, v2_2), (v2_2, v3_3)])

        matches = GraphMatcherByLabel(self.graph, LHS).subgraph_isomorphisms_iter()
        nodes_to_remove = []
        while match := next(matches):
            nodes_to_remove = []

            for k, v in match.items():
                v.position = k.position
                if  v2_2.position == k.position or v3_3.position == k.position:
                    nodes_to_remove.append(k)
            if v2.position == v2_2.position and v3_3.position == v3.position and \
                    v1.position[0] / 2 + v3.position[0] / 2 == v2.position[0] and v1.position[1] / 2 + v3.position[
                1] / 2 == v2.position[1]:
                break

        assert match is not None, f"P9: No match for {LHS} found!"
        print(match.items())


        RHS = nx.Graph()
        RHS.add_node(new_v0 := Vertex(v0.position, "E", level + 1))
        RHS.add_node(new_v1 := Vertex(v1.position, "E", level + 1))
        RHS.add_node(new_v2 := Vertex(v2.position, "E", level + 1))
        RHS.add_node(new_v3 := Vertex(v3.position, "E", level + 1))
        RHS.add_node(new_I_1 := Vertex(I_1.position, "I", level + 1))
        RHS.add_node(new_I_2 := Vertex(I_2.position, "I", level + 1))
        RHS.add_node(new_I_3 := Vertex(I_3.position, "I", level + 1))
        RHS.add_node(new_I_4 := Vertex(I_4.position, "I", level + 1))
        RHS.add_node(new_I_0_1 := Vertex(I_0_1.position, "I", level + 1))
        RHS.add_node(new_I_0_2 := Vertex(I_0_2.position, "I", level + 1))

        edges = [(new_v1, new_I_1),
                 (new_v1, new_I_3),
                 (new_v1, new_v2),
                 (new_v2, new_I_1),
                 (new_v2, new_I_2),
                 (new_v2, new_I_3),
                 (new_v2, new_I_4),
                 (new_v2, new_v3),
                 (new_v3, new_I_2),
                 (new_v3, new_I_4),
                 (new_v0, new_I_0_1),
                 (new_v0, new_I_0_2),
                 (new_I_0_1, new_I_1),
                 (new_I_0_1, new_I_2),
                 (new_I_0_2, new_I_3),
                 (new_I_0_2, new_I_4)
                 ]

        RHS.add_edges_from(edges)

        self.tiers.append([new_v0,new_v1, new_v2, new_v3, new_v3, new_I_1, new_I_2, new_I_3, new_I_4, new_I_0_1, new_I_0_2])
        # add edges between layers (between i and Is)
        self.graph.add_edges_from(edges)

        self.graph.remove_nodes_from(nodes_to_remove)

        print(f"Tiers after P10 {self.tiers}")
        self.productions.append(Production.P10)

        return self


def setUp():
    v1 = (-1, 1)
    v2 = (1, 1)
    v3 = (-1, -1)
    v4 = (1, -1)
    return TieredGraph((v1, v2, v3, v4))

g = setUp()
g.P1()
g.P2(1, direction = Direction.HORIZONTAL)
g.P2(2)
g.P2(2)
# g.show3d()
# g.showLevel(3)
g.P9(3)
g.showLevel(3)
g.show3d()
