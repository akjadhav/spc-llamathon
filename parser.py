import subprocess
import json
import networkx as nx
import sys
import os
import matplotlib.pyplot as plt
import pdb
from graph_node import GraphNode as Node

def get_func_dependencies_json(paths):
    if not isinstance(paths, list):
        paths = [paths]

    args = ['node', 'parser.js']
    args += paths
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    json_str = stdout.decode()
    data = json.loads(json_str)
    return data

def clean_path(path, dir):
    return path.replace(dir, "")[1:]

# Create graph for a single path
def create_dependency_graph(paths, dir):
    graph = nx.DiGraph()
    json_data = get_func_dependencies_json(paths)
    # pdb.set_trace()
    
    for f, dependencies in json_data.items():
        graph.add_node(Node(f, clean_path(dependencies["path"], dir), dependencies["start"], dependencies["end"]))

    for f, dependencies in json_data.items():
        a = Node(f, clean_path(dependencies["path"], dir), dependencies["start"], dependencies["end"])
        for dep in dependencies["dependencies"]:
            # Note: Nodes are indexed by function name and file path
            # Line number is not included, since in this context it refers to
            # the function call location rather than definition location
            b = Node(dep["name"], clean_path(dep["path"], dir), dep["start"], dep["end"])
            graph.add_edge(a, b)

    return graph

def get_js_file_paths(directory):
    js_file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".js"):
                js_file_paths.append(os.path.join(root, file))
    return js_file_paths

def plot_graph(graph):
    nx.draw(graph, with_labels=True, node_color='lightblue', node_size=500, font_weight='bold', edge_color='gray')
    plt.show()

if __name__ == "__main__":
    dir = sys.argv[1]

    if os.path.isfile(dir):
        paths = [dir]
    else:
        paths = get_js_file_paths(dir)

    G = create_dependency_graph(paths, dir)
    plot_graph(G)