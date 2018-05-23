import numpy as np
from collections import defaultdict


def create_corr_struct(predictor_paths, outcome_paths):
    corr_struct = defaultdict(lambda: defaultdict(int))
    ns = defaultdict(int)
    for path, p_nodes in predictor_paths.items():
        o_nodes = outcome_paths[path]
        o_edges = list(zip([0]+o_nodes[:-1], o_nodes))
        p_edges = list(zip([0]+p_nodes[:-1], p_nodes))
        for e in p_edges:
            ns[e] += 1
            print("#", e)
            for e2 in o_edges:
                print("---", e2)
                corr_struct[e][e2] += 1
    for key, v_dict in corr_struct.items():
        for k in v_dict.keys():
            v_dict[k] /= ns[key]

    return corr_struct


def get_path_correlation(corr_struct, nodes):
    corr_vec = defaultdict(int)
    for edge in zip([0] + nodes[:-1], nodes):
        for out_edge, val in corr_struct[edge].items():
            corr_vec[out_edge] += val

    return corr_vec


def predict_path(corr, graph):
    next_edges = [e for e in corr if e[0] == 0]
    nodes = []
    while next_edges:
        vals = [corr[next_edge] for next_edge in next_edges]
        best_next = np.argmax(vals)
        next_edge = next_edges[best_next]
        next_node = next_edge[1]
        nodes.append(next_node)
        next_edges = [(next_node, n) for n in graph.adj_list[next_node]]

    return nodes
