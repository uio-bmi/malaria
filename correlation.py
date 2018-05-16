from pyvg import Graph, Path
from pyvg.conversion import get_json_paths_from_json
import offsetbasedgraph as obg
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
    N = len(p_graph.nodes) + 1
    M = len(o_graph.nodes) + 1
    corr_struct = np.zeros((N, M), dtype="int")

    for path, p_nodes in predictor_nodes.items():
        o_nodes = outcome_nodes[path]
        for p_node in p_nodes:
            corr_struct[p_node, list(o_nodes)] += 1

    return corr_struct/len(predictor_nodes)


def get_path_correlation(corr_struct, nodes):
    node_correlation = corr_struct[nodes, :]
    correlation = np.sum(node_correlation, axis=0)/len(nodes)
    return correlation


def get_correlations(path, corr):
    node_ids = {mapping.start_position.node_id for mapping in path.mappings}
    return get_path_correlation(corr, list(node_ids))

def predict_path(corr, graph):
    next_nodes = list(graph.get_first_blocks())
    nodes = []
    while next_nodes:
        vals = corr[next_nodes]
        next_node = next_nodes[np.argmax(vals)]
        nodes.append(next_node)
        next_nodes = list(graph.adj_list[next_node])
    return nodes

def get_sequence(sequence_graph, node_ids):
    interval = obg.Interval(0, sequence_graph._node_sizes[node_ids[-1]], node_ids)
    return sequence_graph.get_interval_sequence(interval)

def main(alignments_file_name, corr_file_name):
    corr_struct = np.load(corr_file_name)
    paths = get_json_paths_from_json(alignments_file_name)
    paths = (Path.from_json(path) for path in paths)
    corrs = (get_correlations(path, corr_struct) for path in paths)
    cidra_graph = obg.Graph.from_file(data_folder + "cidra.nobg")
    cidra_sequence_graph = obg.SequenceGraph.from_file(data_folder + "cidra.nobg.sequences")
    predicted = (predict_path(corr, cidra_graph)
                 for corr in corrs)
    return (get_sequence(cidra_sequence_graph, pred) for pred in predicted)

if __name__ == "__main__":
    data_folder = "../../data/malaria/pfemp_sequences/150genes/"
    # corr = get_correlation(data_folder+"dbla.json", data_folder+"cidra.json")
    # np.save(data_folder + "dbla_cidra_corr.npy", corr)
    # alignment_corr = get_correlations(data_folder+"alignments.json", data_folder+"dbla_cidra_corr.npy")
    # np.save(data_folder + "tmp_align_corr.npy", alignment_corr)
    res = main(data_folder + "alignments.json",
               data_folder + "dbla_cidra_corr.npy")
    for r in res:
        print(r)
        print("****************")
    # 
    # path = predict_path(np.load(data_folder + "tmp_align_corr.npy"), 
    #                     obg.Graph.from_file(data_folder + "cidra.nobg"))
    # print(get_sequence(obg.SequenceGraph.from_file(data_folder + "cidra.nobg.sequences"),
    #                    path))
    
                       
    

