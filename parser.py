import subprocess
import json
import networkx as nx
import sys
import matplotlib.pyplot as plt

def get_func_dependencies_json(file_path):
    process = subprocess.Popen(['node', 'parser.js', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    json_str = stdout.decode()
    data = json.loads(json_str)
    return data

# Create graph for a single path
def create_dependency_graph(path):
    graph = nx.DiGraph()
    json_data = get_func_dependencies_json(path)
    
    for function, dependencies in json_data.items():
        # name = None
        # if dependencies["class_name"] is None:
        #     name = function
        # else:
        #     name = dependencies["class_name"] + "." + function
        # graph.add_node(name)
        graph.add_node(function)

    for function, dependencies in json_data.items():
        for dep in dependencies["dependencies"]:
            graph.add_edge(function, dep)

    return graph

def plot_graph(graph):
    nx.draw(graph, with_labels=True, node_color='lightblue', node_size=500, font_weight='bold', edge_color='gray')
    plt.show()

if __name__ == "__main__":
    path = sys.argv[1]
    G = create_dependency_graph(path)
    plot_graph(G)