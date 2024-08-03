import subprocess
import json
import networkx as nx
import matplotlib.pyplot as plt

def get_func_dependencies_json(file_path):
    process = subprocess.Popen(['node', 'parser.js', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    json_str = stdout.decode()
    data = json.loads(json_str)
    return data

def create_dependency_graph(path):
    graph = nx.DiGraph()
    json_data = get_func_dependencies_json(path)

    print(json_data)
    
    for function, dependencies in json_data.items():
        graph.add_node(function)

    for function, dependencies in json_data.items():
        for dep in dependencies:
            graph.add_edge(function, dep)

    return graph

G = create_dependency_graph("/Users/cc/Code/llamathon/spc-llamathon-example/components/auth/auth.controller.js")

print(G)

nx.draw(G, with_labels=True, node_color='lightblue', node_size=500, font_weight='bold', edge_color='gray')

# Show the plot
plt.show()