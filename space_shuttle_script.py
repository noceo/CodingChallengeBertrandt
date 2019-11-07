import json

nodes = []
edges = []

edges_dict = {}
cost_dict = {}


def search(nodes, edges, start, end):
    visited_nodes = []
    shortest_paths = {start: (None, 0)}
    current_node = start

    while current_node != end:
        next_nodes = edges_dict[current_node]
        cost_to_cur = shortest_paths[current_node][1]

        for n in next_nodes:
            cost = cost_to_cur + cost_dict[(current_node, n)]
            if n not in shortest_paths:
                shortest_paths[n] = (current_node, cost)
            else:
                if shortest_paths[n][1] > cost:
                    cost_dict[n] = (current_node, cost)
        visited_nodes.append(current_node)

        possible_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited_nodes}

        if not possible_destinations:
            return None

        current_node = min(possible_destinations, key=lambda k: possible_destinations[k][1])

    path = []
    while current_node:
        path.append(current_node)
        current_node = shortest_paths[current_node][0]

    path = path[::-1]

    # Compute cost of the evaluated path
    cost = 0
    for x, y in zip(path[:-1], path[1:]):
        cost += cost_dict[(x, y)]

    return path, cost


with open("generatedGraph.json") as file:
    x = json.load(file)
    nodes = x["nodes"]
    edges = x["edges"]
    for list_ele in nodes:
        if not list_ele["label"].startswith("n"):
            if list_ele["label"] == "Erde":
                start = x["nodes"].index(list_ele)
            elif list_ele["label"] == "b3-r7-r4nd7":
                dest = x["nodes"].index(list_ele)

    for e in edges:
        s = e["source"]
        t = e["target"]
        c = e["cost"]

        edges_dict[s] = edges_dict.get(s, []) + [t]

        edges_dict[t] = edges_dict.get(t, []) + [s]

        cost_dict[(s, t)] = c
        cost_dict[(t, s)] = c

res = search(nodes, edges, start, dest)

print('Shortest path from Earth to "b3-r7-r4nd7":')

for e in res[0][:-1]:
    print(f"{e} -> ", end="")
print(f"{res[0][-1]}\n")

print(f"Costs: {res[1]}")
