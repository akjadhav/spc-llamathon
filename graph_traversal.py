from graph_node import GraphNode
import networkx as nx
from parser import get_js_file_paths, create_dependency_graph

def find_tree_root(G):
    # Find the root node
    for node in G.nodes:
        if G.in_degree(node) == 0:
            return node
    return None

def get_traversal_list(G):
    bfs_tree = nx.bfs_tree(G, find_tree_root(G))
    bfs_nodes = list(bfs_tree.nodes())
    return bfs_nodes

# Asssume graph is connected
# `G` is a networkx graph 
def _get_subtree(G, root, items_changed):
    def dfs(node, subtree):
        if node in items_changed or any(descendant in items_changed for descendant in nx.descendants(G, node)):
            subtree.add_node(node)
            for child in G.successors(node):
                if child not in subtree:
                    dfs(child, subtree)
                if child in subtree:
                    subtree.add_edge(node, child)

    new_subtree = nx.DiGraph()
    dfs(root, new_subtree)
    return new_subtree

# Graph is not necessarily connected
def get_target_subtrees(graph, node_list):
    # G = nx.DiGraph()
    out = []
    for component in nx.connected_components(graph):
        subgraph = graph.subgraph(component)
        filtered_subgraph = _get_subtree(subgraph, find_tree_root(subgraph), node_list)

        l = get_traversal_list(filtered_subgraph)
        out += l

        # G.add_nodes_from(filtered_subgraph.nodes(data=True))
        # G.add_edges_from(filtered_subgraph.edges(data=True))
    return l


# Insertion point for flask-app
def create_traversal_list_from_nodes(dir, node_list):
    paths = get_js_file_paths(dir)
    G = create_dependency_graph(paths)
    return get_target_subtrees(G, node_list)