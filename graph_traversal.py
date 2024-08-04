from graph_node import GraphNode
import networkx as nx
from parser import get_js_file_paths, create_dependency_graph, plot_graph
import pdb

def find_tree_root(G):
    all = []
    # Find the root node
    for node in G.nodes:
        if G.in_degree(node) == 0:
            all.append(node)
    return all

def get_traversal_list(G):
    topo_sort = list(nx.topological_sort(G))
    return topo_sort
    # bfs_tree = nx.bfs_tree(G, find_tree_root(G)[0])
    # bfs_nodes = list(bfs_tree.nodes())
    # return bfs_nodes

# Asssume graph is connected
# `G` is a networkx graph 
def _get_subtree(G, root, items_changed):
    def dfs(node, subtree):
        if node is None:
            return
        if node in items_changed or any(descendant in items_changed for descendant in nx.descendants(G, node)):
            subtree.add_node(node)
            for child in G.successors(node):
                if child not in subtree:
                    dfs(child, subtree)
                if child in subtree:
                    # pdb.set_trace()
                    subtree.add_edge(node, child)

    new_subtree = nx.DiGraph()
    dfs(root, new_subtree)
    return new_subtree

# Graph is not necessarily connected
def get_target_subtrees(graph, node_list):
    out = []
    for component in nx.weakly_connected_components(graph):
        subgraph = graph.subgraph(component)
        roots = find_tree_root(subgraph)
        filtered_subgraph = nx.DiGraph()
        for root in roots:
            _filtered_subgraph = _get_subtree(subgraph, root, node_list)
            filtered_subgraph = nx.compose(filtered_subgraph, _filtered_subgraph)

        if filtered_subgraph.number_of_nodes() == 0:
            continue

        out += get_traversal_list(filtered_subgraph)
    return out

# Insertion point for flask-app
def create_traversal_list_from_nodes(dir, node_list):
    paths = get_js_file_paths(dir)
    G = create_dependency_graph(paths, dir)
    out = get_target_subtrees(G, node_list)
    return out

if __name__ == "__main__":
    dir = "spc-llamathon-example/utils/"
    path = "spc-llamathon-example/utils/math.js"
    node_list = [GraphNode("multiply", path, 4, 6), GraphNode("sumOfSquares", path, 18, 21)]
    print(node_list)
    out = create_traversal_list_from_nodes(dir, node_list) 
    print(f"Length of traversal list: {len(out)}")
    for i in range(len(out)):
        print(out[i].get_code())
        print("--------------------")
