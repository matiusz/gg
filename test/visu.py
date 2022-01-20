import networkx as nx
from matplotlib import pyplot as plt


class Vertex:
    def __init__(self, position: tuple((int, int)), label: str, level: int, id=[0]):
        self.label = label
        self.position = position
        self.level = level
        self.id = id[0]
        id[0] += 1

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
            (3, "i"): "blue"
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

        plt.title("Whole graph")
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

        plt.title(f"Graph at level {level}")
        plt.show()

    def P1(self):
        LHS = nx.Graph()
        LHS.add_node(v0 := Vertex(None, "E", 0))

        matches = GraphMatcherByLabel(self.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)
        assert match is not None, f"P1: No match for {v0} found!"

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
                            (v1, i), (v2, i), (v3, i), (v4, i)])
        self.tiers[0] = [v0]
        self.tiers.append([v1, v2, v3, v4, i])  # appending RHS to first level

        self.graph = RHS

        return self

    def P2(self, level):  # TODO: uwzględnić poziom

        LHS = nx.Graph()
        LHS.add_node(v1 := Vertex(None, "E", level))
        LHS.add_node(v2 := Vertex(None, "E", level))
        LHS.add_node(v3 := Vertex(None, "E", level))
        LHS.add_node(v4 := Vertex(None, "E", level))
        LHS.add_node(i := Vertex(None, "I", level))

        LHS.add_edges_from([(v1, v2), (v2, v4), (v3, v4), (v1, v3),
                            (v1, i), (v2, i), (v3, i), (v4, i)])

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
        RHS.add_node(
            new_v1_5 := Vertex(((v1.position[0] + v2.position[0]) / 2, (v1.position[1] + v2.position[1]) / 2), "E",
                               level + 1))
        RHS.add_node(new_v2 := Vertex(v2.position, "E", level + 1))
        RHS.add_node(new_v3 := Vertex(v3.position, "E", level + 1))
        RHS.add_node(
            new_v3_5 := Vertex(((v3.position[0] + v4.position[0]) / 2, (v3.position[1] + v4.position[1]) / 2), "E",
                               level + 1))
        RHS.add_node(new_v4 := Vertex(v4.position, "E", level + 1))

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
        self.tiers.append([new_v1, new_v1_5, new_v2, new_v3, new_v3_5, new_v4, new_i_left, new_i_right])
        print(f"Tiers after P2 {self.tiers}")

        # add edges between layers (between i and Is)
        self.graph.add_edges_from(edges)
        self.graph.add_edges_from([(matched_i[0], new_i_left), (matched_i[0], new_i_right)])

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

        return self
    
    
    def P5(self, level):
        LHS = nx.Graph()
        LHS.add_node(v1 := Vertex(None, "E", level))
        LHS.add_node(v1_3 := Vertex(None, "E", level))
        LHS.add_node(v2 := Vertex(None, "E", level))
        LHS.add_node(v3 := Vertex(None, "E", level))
        LHS.add_node(v4 := Vertex(None, "E", level))
        LHS.add_node(i := Vertex(None, "I", level))
        
    


        
        LHS.add_edges_from([(v1, v2), 
                            (v2, v4), 
                            (v4, v3), 
                            (v3, v1_3), 
                            (v1_3, v1), 
                            (v1, i),
                            (v2, i),
                            (v3, i), 
                            (v4, i)])
        


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
            
        RHS = nx.Graph()
        
        new_v1 = Vertex(v1.position, "E", level + 1)
        new_v2 = Vertex(v2.position, "E", level + 1)
        new_v3 = Vertex(v3.position, "E", level + 1)
        new_v4 = Vertex(v4.position, "E", level + 1)
        v12 = Vertex(((v1.position[0] + v2.position[0]) / 2, (v1.position[1] + v2.position[1]) / 2), "E", level + 1)
        v13 = Vertex(((v1.position[0] + v3.position[0]) / 2, (v1.position[1] + v3.position[1]) / 2), "E", level + 1)
        v24 = Vertex(((v2.position[0] + v4.position[0]) / 2, (v2.position[1] + v4.position[1]) / 2), "E", level + 1)
        v34 = Vertex(((v3.position[0] + v4.position[0]) / 2, (v3.position[1] + v4.position[1]) / 2), "E", level + 1)
        vc = Vertex(((v1.position[0] + v4.position[0]) / 2, (v1.position[1] + v4.position[1]) / 2), "E", level + 1)
        
        RHS.add_node(new_v1)
        RHS.add_node(new_v2)
        RHS.add_node(new_v3)
        RHS.add_node(new_v4)
        RHS.add_node(v12)
        RHS.add_node(v13)
        RHS.add_node(v24)
        RHS.add_node(v34)
        RHS.add_node(vc)
        
        # RHS.add_node(new_i_left_up := Vertex(
        #     ((new_v1.position[0] + v13.position[0]) / 2 + abs(v13.position[1] - v1.position[1]) / 2, (new_v1.position[1] + v12.position[1]) / 2 - abs(v12.position[0] - v1.position[0]) / 2), "I",
        #     level + 1))

        # RHS.add_node(new_i_right_up := Vertex(
        #     ((v12.position[0] + vc.position[0]) / 2 + abs(v12.position[1] - vc.position[1]) / 2, (v12.position[1] + new_v2.position[1]) / 2 - abs(v12.position[0] - new_v2.position[0]) / 2), "I",
        #     level + 1))
        # RHS.add_node(new_i_left_down := Vertex(
        #     ((v13.position[0] + new_v3.position[0]) / 2 + abs(v13.position[1] - new_v3.position[1]) / 2, (v13.position[1] + vc.position[1]) / 2 - abs(v13.position[0] - vc.position[0]) / 2), "I",
        #     level + 1))

        # RHS.add_node(new_i_right_down := Vertex(
        #     ((vc.position[0] + v34.position[0]) / 2 + abs(vc.position[1] - v34.position[1]) / 2, (vc.position[1] + v24.position[1]) / 2 - abs(vc.position[0] - v24.position[0]) / 2), "I",
        #     level + 1))
        
        
        RHS.add_node(new_i_top_left := Vertex(((new_v1.position[0] + vc.position[0]) / 2, (new_v1.position[1] + vc.position[1]) / 2), "I", level + 1))
        RHS.add_node(new_i_top_right := Vertex(((new_v2.position[0] + vc.position[0]) / 2, (new_v2.position[1] + vc.position[1]) / 2), "I", level + 1))

        RHS.add_node(new_i_bottom_left := Vertex(((new_v3.position[0] + vc.position[0]) / 2, (new_v3.position[1] + vc.position[1]) / 2), "I", level + 1))
        RHS.add_node(new_i_bottom_right := Vertex(((new_v4.position[0] + vc.position[0]) / 2, (new_v4.position[1] + vc.position[1]) / 2), "I", level + 1))
        
        # else:
        #     RHS.add_node(new_i_left_up := Vertex(
        #         ((new_v1.position[0] + v12.position[0]) / 2, (new_v1.position[1] + v13.position[1]) / 2), "I",
        #         level + 1))

        #     RHS.add_node(new_i_right_up := Vertex(
        #         ((v12.position[0] + new_v2.position[0]) / 2,( v12.position[1] + vc.position[1]) / 2), "I",
        #         level + 1))
            
        #     RHS.add_node(new_i_left_down := Vertex(
        #         ((v13.position[0] + vc.position[0]) / 2, (v13.position[1] + new_v3.position[1]) / 2), "I",
        #         level + 1))

        #     RHS.add_node(new_i_right_down := Vertex(
        #         ((vc.position[0] + v24.position[0]) / 2, (vc.position[1] + v34.position[1]) / 2), "I",
        #         level + 1))
            
        edges = [(new_v1, v12), (v12, new_v2), (new_v2, v24), (v24, new_v4), (new_v4, v34),
                 (v34, new_v3), (new_v3, v13),
                 (v13, new_v1), (v12, vc), (v13, vc), (v24, vc),
                 (v34, vc), (new_v1, new_i_top_left), (v12, new_i_top_left), (vc, new_i_top_left), (v13, new_i_top_left),
                 (v12, new_i_top_right), (new_v2, new_i_top_right), (v24, new_i_top_right), (vc, new_i_top_right),
                 (v13, new_i_bottom_left), (vc, new_i_bottom_left), (v34, new_i_bottom_left), (new_v3, new_i_bottom_left),
                 (vc, new_i_bottom_right), (v24, new_i_bottom_right), (new_v4, new_i_bottom_right), (v34, new_i_bottom_right)]
        
        RHS.add_edges_from(edges)
        
        self.tiers.append([new_v1, new_v2, new_v3, new_v4, v12, v13, v24, v34, vc, new_i_top_left, new_i_top_right, new_i_bottom_left, new_i_bottom_right])
        
        print(f"Tiers after P5 {self.tiers}")

        # add edges between layers (between i and Is)
        self.graph.add_edges_from(edges)
        
        self.graph.add_edges_from([(matched_i[0], new_i_top_left), (matched_i[0], new_i_top_right)])
    
        return self
    
    def P6(self, level):
        LHS = nx.Graph()
        LHS.add_node(v1 := Vertex(None, "E", level))
        LHS.add_node(v1_3 := Vertex(None, "E", level))
        LHS.add_node(v1_2 := Vertex(None, "E", level))
        LHS.add_node(v2 := Vertex(None, "E", level))
        LHS.add_node(v3 := Vertex(None, "E", level))
        LHS.add_node(v4 := Vertex(None, "E", level))
        LHS.add_node(i := Vertex(None, "I", level))

        
        LHS.add_edges_from([(v1, v1_2), 
                            (v1_2, v2),
                            (v2, v4), 
                            (v4, v3), 
                            (v3, v1_3), 
                            (v1_3, v1), 
                            (v1, i),
                            (v2, i),
                            (v3, i), 
                            (v4, i)])
            

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
            
        RHS = nx.Graph()
        
        new_v1 = Vertex(v1.position, "E", level + 1)
        new_v2 = Vertex(v2.position, "E", level + 1)
        new_v3 = Vertex(v3.position, "E", level + 1)
        new_v4 = Vertex(v4.position, "E", level + 1)
        v12 = Vertex(((v1.position[0] + v2.position[0]) / 2, (v1.position[1] + v2.position[1]) / 2), "E", level + 1)
        v13 = Vertex(((v1.position[0] + v3.position[0]) / 2, (v1.position[1] + v3.position[1]) / 2), "E", level + 1)
        v24 = Vertex(((v2.position[0] + v4.position[0]) / 2, (v2.position[1] + v4.position[1]) / 2), "E", level + 1)
        v34 = Vertex(((v3.position[0] + v4.position[0]) / 2, (v3.position[1] + v4.position[1]) / 2), "E", level + 1)
        vc = Vertex(((v1.position[0] + v4.position[0]) / 2, (v1.position[1] + v4.position[1]) / 2), "E", level + 1)
        
        RHS.add_node(new_v1)
        RHS.add_node(new_v2)
        RHS.add_node(new_v3)
        RHS.add_node(new_v4)
        RHS.add_node(v12)
        RHS.add_node(v13)
        RHS.add_node(v24)
        RHS.add_node(v34)
        RHS.add_node(vc)
        
        RHS.add_node(new_i_top_left := Vertex(((new_v1.position[0] + vc.position[0]) / 2, (new_v1.position[1] + vc.position[1]) / 2), "I", level + 1))
        RHS.add_node(new_i_top_right := Vertex(((new_v2.position[0] + vc.position[0]) / 2, (new_v2.position[1] + vc.position[1]) / 2), "I", level + 1))

        RHS.add_node(new_i_bottom_left := Vertex(((new_v3.position[0] + vc.position[0]) / 2, (new_v3.position[1] + vc.position[1]) / 2), "I", level + 1))
        RHS.add_node(new_i_bottom_right := Vertex(((new_v4.position[0] + vc.position[0]) / 2, (new_v4.position[1] + vc.position[1]) / 2), "I", level + 1))
        # else:
        #     RHS.add_node(new_i_left_up := Vertex(
        #         ((new_v1.position[0] + v12.position[0]) / 2, (new_v1.position[1] + v13.position[1]) / 2), "I",
        #         level + 1))

        #     RHS.add_node(new_i_right_up := Vertex(
        #         ((v12.position[0] + new_v2.position[0]) / 2,( v12.position[1] + vc.position[1]) / 2), "I",
        #         level + 1))
            
        #     RHS.add_node(new_i_left_down := Vertex(
        #         ((v13.position[0] + vc.position[0]) / 2, (v13.position[1] + new_v3.position[1]) / 2), "I",
        #         level + 1))

        #     RHS.add_node(new_i_right_down := Vertex(
        #         ((vc.position[0] + v24.position[0]) / 2, (vc.position[1] + v34.position[1]) / 2), "I",
        #         level + 1))
            
        edges = [(new_v1, v12), (v12, new_v2), (new_v2, v24), (v24, new_v4), (new_v4, v34),
                 (v34, new_v3), (new_v3, v13),
                 (v13, new_v1), (v12, vc), (v13, vc), (v24, vc),
                 (v34, vc), (new_v1, new_i_top_left), (v12, new_i_top_left), (vc, new_i_top_left), (v13, new_i_top_left),
                 (v12, new_i_top_right), (new_v2, new_i_top_right), (v24, new_i_top_right), (vc, new_i_top_right),
                 (v13, new_i_bottom_left), (vc, new_i_bottom_left), (v34, new_i_bottom_left), (new_v3, new_i_bottom_left),
                 (vc, new_i_bottom_right), (v24, new_i_bottom_right), (new_v4, new_i_bottom_right), (v34, new_i_bottom_right)]
        RHS.add_edges_from(edges)
        
        self.tiers.append([new_v1, new_v2, new_v3, new_v4, v12, v13, v24, v34, vc, new_i_top_left, new_i_top_right, new_i_bottom_left, new_i_bottom_right])
        print(f"Tiers after P5 {self.tiers}")

        # add edges between layers (between i and Is)
        self.graph.add_edges_from(edges)
        
        self.graph.add_edges_from([(matched_i[0], new_i_top_left), (matched_i[0], new_i_top_right)])
    
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