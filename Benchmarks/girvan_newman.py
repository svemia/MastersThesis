import sys
from itertools import permutations, product
from copy import deepcopy

class GNAlgorithm:

    def __init__(self, graph: dict, feats: dict, edges: dict, start_edges: dict):
        self.graph = graph
        self.feats = feats
        self.edges = edges
        self.start_edges = start_edges
        self.no_nodes = len(feats)

    def find_all_paths(self, start, end, path=None):
        if path is None:
            path = []
        path = path + [start]
        if start == end:
            return [path]
        if start not in self.graph:
            return []
        paths = []
        for node in self.graph[start]:
            if node not in path:
                newpaths = self.find_all_paths(node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def find_shortest_paths(self, pair):
        paths = self.find_all_paths(pair[0], pair[1])
        # print("pair {p}: {s}".format(p=pair, s=paths))
        if len(paths) == 0:
            return None
        mtest = 10 ** 99
        mpaths = []
        for path in paths:
            suma = 0
            for edg in zip(path, path[1::]):
                if (edg[0], edg[1]) in self.edges:
                    suma += self.edges[(edg[0], edg[1])][0]
                elif (edg[1], edg[0]) in self.edges:
                    suma += self.edges[(edg[1], edg[0])][0]
            if suma < mtest:
                mtest = suma
            mpaths.append((path, suma))

        shortest = []
        for p in mpaths:
            if p[1] == mtest:
                shortest.append(p[0])
        return shortest

    def check_modularity(self):
        m = self.total_weight()
        all_pairs = product(self.feats.keys(), self.feats.keys())
        modularity = 0
        for pair in all_pairs:
            paths = self.find_all_paths(pair[0], pair[1])
            if len(paths) == 0:
                continue
            if (pair[0], pair[1]) in self.edges:
                Auv = self.start_edges[(pair[0], pair[1])][0]
            elif (pair[1], pair[0]) in self.edges:
                Auv = self.start_edges[(pair[1], pair[0])][0]
            else:
                Auv = 0

            k_u, k_v = 0, 0
            for edge in self.edges:
                if pair[0] in edge:
                    k_u += self.edges[edge][0]
                if pair[1] in edge:
                    k_v += self.edges[edge][0]
            modularity += (Auv - ((k_u * k_v) / (2 * m)))

        return round(modularity / (2 * m), 4)

    def calculate_centrality(self):
        all_pairs = permutations(self.graph.keys(), 2)
        for pair in all_pairs:
            shortest = self.find_shortest_paths(pair)
            #print("pair {p}: {s}".format(p=pair, s=shortest))
            if shortest is None:
                continue
            N = len(shortest)
            for path in shortest:
                for i, j in zip(path, path[1::]):
                    if (i, j) in self.edges:
                        self.edges[(i, j)][1] += (1 / N)
                    elif (j, i) in self.edges:
                        self.edges[(j, i)][1] += (1 / N)

        for edge in self.edges:
            self.edges[edge][1] = round(self.edges[edge][1] / 2, 4)

    def total_weight(self):
        total = 0
        for edge in self.start_edges:
            total += self.start_edges[edge][0]
        return total

    def remove_edges(self):
        edges_rm = self.find_rm_edges()
        for edge in edges_rm:
            del self.edges[edge]
        self.restore_centrality()
        self.update_graph(edges_rm)
        return edges_rm, self.graph

    def find_rm_edges(self):
        maximum = 0
        for edge in self.edges:
            if self.edges[edge][1] > maximum:
                maximum = self.edges[edge][1]
        remove = []
        for edge in self.edges:
            if self.edges[edge][1] == maximum:
                remove.append(edge)
        return remove

    def restore_centrality(self):
        for edge in self.edges:
            self.edges[edge][1] = 0

    def update_graph(self, removed):
        for rem in removed:
            self.graph[rem[0]].remove(rem[1])
            self.graph[rem[1]].remove(rem[0])


def set_weights(edges, feats):
    max_sim = len(feats[list(feats.keys())[0]])
    for pair in edges:
        sim = 0
        for (fst, snd) in zip(feats[pair[0]], feats[pair[1]]):
            if fst == snd:
                sim += 1
        final_weight = max_sim - (sim - 1)
        edges[pair][0] = final_weight

    return edges


def read_file(reader):
    graph, feats, edges = {}, {}, {}
    while True:
        line = reader.readline().strip()
        if line == "":
            break
        split_line = line.split()
        fst, snd = split_line[0].strip(), split_line[1].strip()
        if fst not in graph:
            graph[fst] = [snd]
        else:
            graph[fst].append(snd)
        if snd not in graph:
            graph[snd] = [fst]
        else:
            graph[snd].append(fst)
        if (fst, snd) not in edges and (snd, fst) not in edges:
            edges[(fst, snd)] = [1, 0]

    while True:
        line = reader.readline().strip()
        if line == "":
            break
        split_line = line.split(" ", 1)
        fst, snd = split_line[0].strip(), split_line[1].strip().split()
        if fst not in feats:
            feats[fst] = snd
        if fst not in graph:
            graph[fst] = []

    return graph, feats, edges


def find_partitions(graph):
    nodes = list(graph.keys())
    visited = set()
    partitions = {}
    i_part = 0
    while True:
        if all(item in visited for item in nodes):
            break

        go = None
        for node in nodes:
            if node in visited:
                continue
            go = node
            break

        part = dfs(graph, go)
        visited.update(part)
        partitions[i_part] = part
        i_part += 1

    return partitions


def dfs(graph, node, partition=None):
    if partition is None:
        partition = set()

    if node not in partition:
        partition.add(node)
        if node not in graph:
            return partition
        for neighbour in graph[node]:
            partition = dfs(graph, neighbour, partition)

    return partition


def print_removed(removed):
    change = list(list(x) for x in removed)
    sort = sorted(change, key=lambda x: (x[0], x[1]))
    for rem in sort:
        list_rem = list(rem)
        list_rem.sort()
        # print("{fst} {snd}".format(fst=list_rem[0], snd=list_rem[1]))

        sys.stdout.write("{fst} {snd}".format(fst=list_rem[0], snd=list_rem[1]))
        sys.stdout.write("\n")


def print_partitions(results):
    maxi = 0
    parts = None
    for res in results:
        if results[res]["MOD"] >= maxi:
            maxi = results[res]["MOD"]
            parts = results[res]["PARTS"]

    # print(parts)
    output = ""
    for k in sorted(parts, key=lambda x: len(parts[x])):
        sorted_p = sorted(parts[k])
        for i in range(len(sorted_p)):
            output += sorted_p[i]
            output += "-"
        output = output[:-1]
        output += " "
    # print(output)
    sys.stdout.write(output)


def main():
    reader = open("t2.in", "r")
    # reader = sys.stdin
    graph, feats, edges = read_file(reader)
    edges = set_weights(edges, feats)
    start_edges = deepcopy(edges)
    gn_alg = GNAlgorithm(graph, feats, edges, start_edges)

    result = {}
    removed = {}
    it = 0
    while True:
        gn_alg.calculate_centrality()
        if it == 0:
            print(gn_alg.edges)
        rem, grph = gn_alg.remove_edges()
        print_removed(rem)
        if len(gn_alg.edges) == 0:
            break
        mod = gn_alg.check_modularity()
        partitions = find_partitions(grph)

        removed[it] = rem
        result[it] = {"MOD": mod,
                      "PARTS": partitions}
        it += 1

    print_partitions(result)


if __name__ == '__main__':
    # main()
    for i in range(20):
        main()
