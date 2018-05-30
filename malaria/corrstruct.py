import numpy as np
from collections import defaultdict


def save(filename, struct):
    np.save(filename+".npy", struct)


def load(filename, struct):
    return np.load(filename)


def create_corr_struct(predictor_paths, outcome_paths, M, N):
    corr_struct = np.zeros((N, M), dtype="float")
    scale = np.zeros(N, dtype="float")
    for path, p_nodes in predictor_paths.items():
        o_nodes = outcome_paths[path]
        for p_node in p_nodes:
            corr_struct[p_node, list(o_nodes)] += 1
            scale[p_node] += 1
    print(np.flatnonzero(scale == 0))
    corr_struct[1:, 1:] /= scale[1:, None]
    return corr_struct

def get_path_correlation(corr_struct, nodes):
    node_correlation = corr_struct[nodes, :]
    correlation = np.sum(node_correlation, axis=0)
    return correlation

def predict_path(corr, graph):
    next_nodes = list(graph.get_first_blocks())
    nodes = []
    while next_nodes:
        vals = corr[next_nodes]
        best_next = np.argmax(vals)
        next_node = next_nodes[best_next]
        nodes.append(next_node)
        next_nodes = list(graph.adj_list[next_node])

    return nodes
