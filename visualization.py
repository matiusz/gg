# %%
import networkx as nx
from matplotlib import pyplot as plt


# %%
class Vertex:
    def __init__(self, position: tuple((int, int)), label: str, color: str, id=[0]):
        self.label = label
        self.position = position
        self.color = color
        self.id = id[0]
        id[0] += 1

    def __hash__(self) -> int:
        return hash((self.id, self.label, self.color, self.position))

    def __eq__(self, G2_node):
        # TODO: kolor na razie wszędzie dawać ten sam dla uproszczenia?...
        # TODO: porównywać po odległościach między wierzchołkami??? bo trzeba chyba sprawdzić, czy w środku grafu jest I czy i?
        return self.label == G2_node.label and self.color == G2_node.color

    def __repr__(self):
        return f"{self.color} {self.label} vertex at {self.position}"


class GraphMatcherByLabel(nx.isomorphism.GraphMatcher):
    def __init__(self, graph1, graph2):
        super().__init__(graph1, graph2)

    def semantic_feasibility(self, G1_node, G2_node):
        # TODO: chyba po samej labelce? ale trzeba też sprawdzić, czy w środku grafu jest I czy i?
        # return G1_node.label == G2_node.label and G1_node.color == G2_node.color
        return True


# %% 
class TieredGraph:
    def __init__(self, corners: tuple):
        self.graph = nx.Graph()
        starting_vertex = Vertex((0, 0), "E", "red")
        self.graph.add_node(starting_vertex)
        self.corners = corners
        self.tiers = []
        self.tiers.append([starting_vertex])

    def show(self):
        fig, ax = plt.subplots()
        xs, ys = zip(*[node.position for node in self.graph.nodes])
        colors = [node.color for node in self.graph.nodes]
        labels = [node.label for node in self.graph.nodes]
        xs = list(xs)
        ys = list(ys)

        edges = [edge for edge in self.graph.edges]
        for edge in edges:
            ax.plot([edge[0].position[0], edge[1].position[0]], [edge[0].position[1], edge[1].position[1]],
                    color="black", zorder=1)

        ax.scatter(xs, ys, c=colors, s=200, zorder=2)

        for i, label in enumerate(labels):
            ax.annotate(label, (xs[i], ys[i]))
        plt.show()

    def showLevel(self, level: int):
        levelNodes = [node for node in self.graph.nodes if node in self.tiers[level]]
        graph = self.graph.subgraph(levelNodes)
        fig, ax = plt.subplots()
        xs, ys = zip(*[node.position for node in graph.nodes])
        colors = [node.color for node in graph.nodes]
        labels = [node.label for node in graph.nodes]
        xs = list(xs)
        ys = list(ys)

        edges = [edge for edge in graph.edges]
        for edge in edges:
            ax.plot([edge[0].position[0], edge[1].position[0]], [edge[0].position[1], edge[1].position[1]],
                    color="black", zorder=1)

        ax.scatter(xs, ys, c=colors, s=200, zorder=2)

        for i, label in enumerate(labels):
            ax.annotate(label, (xs[i], ys[i]))
        plt.show()

    def P1(self):
        LHS = nx.Graph()
        LHS.add_node(Vertex(None, "E", "red"))
        match = None
        matches = GraphMatcherByLabel(self.graph, LHS).subgraph_isomorphisms_iter()
        if matches:
            match = next(matches)

        # TODO: czy mamy kopiować lewą stronę produkcji w P1?
        RHS = nx.Graph()
        RHS.add_node(v0 := Vertex(list(match.keys())[0].position, "e", "red"))
        RHS.add_node(v1 := Vertex(self.corners[0], "E", "blue"))
        RHS.add_node(v2 := Vertex(self.corners[1], "E", "blue"))
        RHS.add_node(v3 := Vertex(self.corners[2], "E", "blue"))
        RHS.add_node(v4 := Vertex(self.corners[3], "E", "blue"))
        # TODO: czy współrzędne idą pionowo/poziomo względem OX i OY??
        RHS.add_node(
            i := Vertex(((self.corners[0][0] + self.corners[1][0]) / 2, (self.corners[0][1] + self.corners[2][1]) / 2),
                        "I", "red"))
        RHS.add_edges_from([(v1, v2), (v2, v4), (v4, v3), (v3, v1),
                            (v1, i), (v2, i), (v3, i), (v4, i)])
        self.tiers[0] = v0
        self.tiers.append([v1, v2, v3, v4, i])  # appending RHS to first level

        self.graph = RHS

    def P2(self):  # TODO: uwzględnić poziom
        # levelNodes = [node for node in self.graph.nodes if node in self.tiers[level]]
        # graph = self.graph.subgraph(levelNodes)

        LHS = nx.Graph()
        LHS.add_node(v1 := Vertex(1, "E", "blue"))
        LHS.add_node(v2 := Vertex(2, "E", "blue"))
        LHS.add_node(v3 := Vertex(3, "E", "blue"))
        LHS.add_node(v4 := Vertex(4, "E", "blue"))
        LHS.add_node(i := Vertex(None, "I", "red"))

        LHS.add_edges_from([(v1, v2), (v2, v4), (v3, v4), (v1, v3),
                            (v1, i), (v2, i), (v3, i), (v4, i)])

        matches = GraphMatcherByLabel(self.graph, LHS).subgraph_isomorphisms_iter()
        match = next(matches)

        # change I -> i
        matched_i = [v for v in list(match.keys()) if v.label == "I"]
        matched_i[0].label = "i"

        print(match)

        for k, v in match.items():
            v.position = k.position

        RHS = nx.Graph()
        # TODO: uwzględnić różne kolory na róznych poziomach?
        RHS.add_node(new_v1 := Vertex(v1.position, "E", "green"))
        RHS.add_node(
            new_v1_5 := Vertex(((v1.position[0] + v2.position[0]) / 2, (v1.position[1] + v2.position[1]) / 2), "E",
                               "green"))
        RHS.add_node(new_v2 := Vertex(v2.position, "E", "green"))
        RHS.add_node(new_v3 := Vertex(v3.position, "E", "green"))
        RHS.add_node(
            new_v3_5 := Vertex(((v3.position[0] + v4.position[0]) / 2, (v3.position[1] + v4.position[1]) / 2), "E",
                               "green"))
        RHS.add_node(new_v4 := Vertex(v4.position, "E", "green"))

        RHS.add_node(new_i_left := Vertex(
            ((new_v1.position[0] + new_v1_5.position[0]) / 2, (new_v1.position[0] + new_v3.position[1]) / 2), "I",
            "orange"))

        RHS.add_node(new_i_right := Vertex(
            ((new_v1_5.position[0] + new_v3.position[0]) / 2, (new_v1_5.position[0] + new_v3_5.position[1]) / 2), "I",
            "orange"))

        # for v in [new_v1, new_v1_5, new_v2, new_v3, new_v3_5, new_v4, new_i_left, new_i_right]:
        #    print(v)
        #    print(v.position[0])
        #    print(v.position[1])

        edges = [(new_v1, new_v1_5), (new_v1_5, new_v2), (new_v1, new_v3), (new_v3, new_v3_5), (new_v1_5, new_v3_5),
                 (new_v3_5, new_v4), (new_v2, new_v4),
                 (new_v1, new_i_left), (new_v1_5, new_i_left), (new_v3, new_i_left), (new_v3_5, new_i_left),
                 (new_v1_5, new_i_right), (new_v2, new_i_right), (new_v3_5, new_i_right), (new_v4, new_i_right)]
        RHS.add_edges_from(edges)

        # appending RHS to new level - powinno uwzględniać poziom "parenta"
        self.tiers.append([new_v1, new_v1_5, new_v2, new_v3, new_v3_5, new_v4, new_i_left, new_i_right])
        print(self.tiers)
        # add edges between layers (between i and Is)
        self.graph.add_edges_from(edges)
        self.graph.add_edges_from([(matched_i[0], new_i_left), (matched_i[0], new_i_right)])


if __name__ == '__main__':
    g = TieredGraph(((-1, 1), (1, 1), (-1, -1), (1, -1)))
    # g.showLevel(0)
    g.P1()
    # g.showLevel(1)
    g.P2()
    # g.showLevel(0)
    # g.showLevel(1)
    g.showLevel(2)
    # g.P2(2)
    # g.P2(2)
    # g.showLevel(1)
    # g.showLevel(2)
