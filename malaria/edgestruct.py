import math

import numpy as np
import pickle
from collections import defaultdict

def intdefaultdict():
    return defaultdict(int)

def save(filename, struct):
    with open(filename+".pkl", "wb") as f:
        pickle.dump(struct, f, pickle.HIGHEST_PROTOCOL)

def load(filename):
    with open(filename+".pkl", "rb") as f:
        return pickle.load(f)

def create_corr_struct(predictor_paths, outcome_paths, M=0, N=0):
    corr_struct = defaultdict(intdefaultdict)
    ns = defaultdict(int)
    for path, p_nodes in predictor_paths.items():
        o_nodes = outcome_paths[path]
        o_edges = list(zip([0]+o_nodes[:-1], o_nodes))
        p_edges = list(zip([0]+p_nodes[:-1], p_nodes))
        for e in p_edges:
            ns[e] += 1
            for e2 in o_edges:
                corr_struct[e][e2] += 1
    for key, v_dict in corr_struct.items():
        for k in v_dict.keys():
            v_dict[k] /= ns[key]
            # v_dict[k] = math.log(v_dict[k]+0.001)
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
