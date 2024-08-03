import subprocess
import json
import networkx as nx
import sys
import os
import matplotlib.pyplot as plt

from node import Node

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

# Create graph for a single path
def create_dependency_graph(paths):
    graph = nx.DiGraph()
    json_data = get_func_dependencies_json(paths)
    
    for f, dependencies in json_data.items():
        graph.add_node(f, data=Node(f, dependencies["path"], dependencies["start"], dependencies["end"]))

    for f, dependencies in json_data.items():
        for dep in dependencies["dependencies"]:
            graph.add_edge(f, dep)

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
    paths = get_js_file_paths(dir)
    G = create_dependency_graph(paths)
    plot_graph(G)