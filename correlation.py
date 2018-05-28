from pyvg import Graph, Path, Alignment
from pyvg.conversion import get_json_paths_from_json

import offsetbasedgraph as obg
import numpy as np
import json
from malaria.edgestruct import create_corr_struct, \
    get_path_correlation, predict_path, save, load


def get_alignments(filename):
    return (json.loads(line) for line in open(filename))


def get_path_nodes(graph):
    paths = graph.paths
    return {path.name:
            [mapping.start_position.node_id for mapping in path.mappings]
            for path in paths}


def get_correlation(predictor_graph_name, outcome_graph_name):
    p_graph = Graph.from_file(predictor_graph_name)
    o_graph = Graph.from_file(outcome_graph_name)
    predictor_nodes = get_path_nodes(p_graph)
    outcome_nodes = get_path_nodes(o_graph)
    M = len(o_graph.nodes) + 1
    N = len(p_graph.nodes) + 1

    return create_corr_struct(
        predictor_nodes, outcome_nodes,
        M, N)


def get_correlations(path, corr):
    node_ids = {mapping.start_position.node_id
                for mapping in path.mappings}

    corr = get_path_correlation(corr, list(node_ids))
    return corr


def get_sequence(sequence_graph, node_ids):
    interval = obg.Interval(
        0, sequence_graph._node_sizes[node_ids[-1]], node_ids)
    return sequence_graph.get_interval_sequence(interval)


def main(alignments_file_name, corr_file_name):
    corr_struct = load(corr_file_name)
    # corr_struct = np.log(corr_struct + 0.01)
    paths = get_alignments(alignments_file_name)
    paths = [Alignment.from_json(path) for path in paths]
    print(len(paths))
    corrs = {path.name: get_correlations(path.path, corr_struct)
             for path in paths}
    print(len(corrs))
    cidra_graph = obg.Graph.from_file(data_folder + "cidra.nobg")
    cidra_sequence_graph = obg.SequenceGraph.from_file(
        data_folder + "cidra.nobg.sequences")
    predicted = {name: predict_path(corr, cidra_graph)
                 for name, corr in corrs.items()}
    return {name: get_sequence(cidra_sequence_graph, pred)
            for name, pred in predicted.items()}


if __name__ == "__main__":
    import sys
    data_folder = "../../data/malaria/pfemp_sequences/504sequences/"
    corr = get_correlation(data_folder+"dbla.json", data_folder+"cidra.json")
    save(data_folder + "dbla_cidra_corr", corr)
    # alignment_cporr = get_correlations(data_folder+"alignments.json", data_folder+"dbla_cidra_corr.npy")
    # np.save(data_folder + "tmp_align_corr.npy", alignment_corr)
    res = main(sys.argv[1],
               data_folder + "dbla_cidra_corr")

    with open(sys.argv[1] + "graph_predictions.fasta", "w") as f:
        for name, r in res.items():
            f.write(">%s\n" % name)
            f.write(r.upper()+"\n")

    # 
    # path = predict_path(np.load(data_folder + "tmp_align_corr.npy"), 
    #                     obg.Graph.from_file(data_folder + "cidra.nobg"))
    # print(get_sequence(obg.SequenceGraph.from_file(data_folder + "cidra.nobg.sequences"),
    #                    path))
