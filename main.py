import json
from malaria.classification import NodeModel

import offsetbasedgraph as obg
from pyvg import Graph, Alignment


def get_path_dict(filename):
    alignments = (json.loads(line) for line in open(filename))
    alignments = (Alignment.from_json(alignment) for alignment in alignments)
    return {alignment.name: [mapping.start_position.node_id
                             for mapping in alignment.path.mappings]
            for alignment in alignments}


def get_path_nodes(graph):
    paths = graph.paths
    return {path.name:
            [mapping.start_position.node_id for mapping in path.mappings]
            for path in paths}


def get_sequence(sequence_graph, node_ids):
    interval = obg.Interval(
        0, sequence_graph._node_sizes[node_ids[-1]], node_ids)
    return sequence_graph.get_interval_sequence(interval)


def train_model(predictor_graph_name, outcome_graph_name):
    print("Training")
    pred_graph = Graph.from_file(predictor_graph_name)
    out_graph = Graph.from_file(outcome_graph_name)
    model = NodeModel(pred_graph, out_graph)
    pred_paths = get_path_nodes(pred_graph)
    out_paths = get_path_nodes(out_graph)
    keys = list(pred_paths.keys())
    out_paths = [out_paths[key] for key in keys]
    pred_paths = [pred_paths[key] for key in keys]
    model.fit(pred_paths, out_paths)
    return model


def predict_sequences(model, alignments, sequence_graph):
    print("Predicting")
    paths = get_path_dict(alignments)
    predicted_paths = {name: model.predict(path) for
                       name, path in paths.items()}
    sequence_graph = obg.SequenceGraph.from_file(sequence_graph)
    sequences = {name: get_sequence(sequence_graph, path)
                 for name, path in predicted_paths.items()}
    return sequences

if __name__ == "__main__":
    import sys
    predictor_graph_name = sys.argv[1]
    outcome_graph_name = sys.argv[2]
    test_alignments = sys.argv[3]
    # get_path_dict(test_alignments)
    # model = train_model(predictor_graph_name, outcome_graph_name)
    import pickle
    model = pickle.load(open("tmpmodel.pkl", "rb"))
    # try:
    #     with open("tmpmodel.pkl", "wb") as f:
    #         pickle.dump(model, f, pickle.HIGHEST_PROTOCOL)
    # except:
    #    pass
    sequences = predict_sequences(
        model, test_alignments,
        outcome_graph_name.replace(".json", ".nobg.sequences"))
    f = open("out.txt", "w")
    for name, seq in sequences:
        f.write(">" + name + "\n")
        f.write(str(seq)+"\n")
