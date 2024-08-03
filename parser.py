import subprocess
import json
import networkx as nx
import sys
import matplotlib.pyplot as plt

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
    
    for function, dependencies in json_data.items():
        graph.add_node(function)

    for function, dependencies in json_data.items():
        for dep in dependencies["dependencies"]:
            graph.add_edge(function, dep)

    return graph

def plot_graph(graph):
    nx.draw(graph, with_labels=True, node_color='lightblue', node_size=500, font_weight='bold', edge_color='gray')
    plt.show()

if __name__ == "__main__":
    paths = sys.argv[1:]
    print(paths)
    G = create_dependency_graph(paths)
    plot_graph(G)