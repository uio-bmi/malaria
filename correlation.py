from pyvg import Graph
import numpy as np


def get_path_nodes(graph):
    paths = graph.paths
    return {path.name:
            {mapping.start_position.node_id for mapping in path.mappings}
            for path in paths}


def get_correlation(predictor_graph_name, outcome_graph_name):
    p_graph = Graph.from_file(predictor_graph_name)
    o_graph = Graph.from_file(outcome_graph_name)
    predictor_nodes = get_path_nodes(p_graph)
    outcome_nodes = get_path_nodes(o_graph)
    N = len(p_graph.nodes)
    M = len(o_graph.nodes)
    corr_struct = np.zeros(N, M, dtype="int")

    for path, p_nodes in predictor_nodes.items():
        o_nodes = outcome_nodes[path]
        for p_node in p_nodes:
            corr_struct[p_node, o_nodes] += 1

    return np.log(corr_struct)


def get_path_correlation(corr_struct, nodes):
    node_correlation = corr_struct[nodes, :]
    correlation = np.sum(node_correlation)
    return correlation
