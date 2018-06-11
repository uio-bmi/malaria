import json
from malaria.classification import NodeModel, NodeModelSVM, NodeModelRF
import malaria.interface
import offsetbasedgraph as obg
from pyvg import Graph, Alignment

classifier = NodeModelRF

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


def train_model(predictor_graph_name, outcome_graph_name, train_alignmens=None, train_cidra_alignments=None):
    print("Training")
    pred_graph = Graph.from_file(predictor_graph_name)
    out_graph = Graph.from_file(outcome_graph_name)
    model = classifier(pred_graph, out_graph)
    if train_alignments is not None:
        pred_paths = get_path_dict(train_alignments)
    else:
        pred_paths = get_path_nodes(pred_graph)
    if train_cidra_alignments is not None:
        out_paths = get_path_dict(train_cidra_alignments)
    else:
        out_paths = get_path_nodes(out_graph)
    keys = list(pred_paths.keys())
    pred_paths = [pred_paths[key] for key in keys if key in out_paths]
    out_paths = [out_paths[key] for key in keys if key in out_paths]
    print("Number in both: %s / %s" % (len(out_paths), len(keys)))
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
    malaria.interface.main()
    # python3 main.py --dbla_graph dbla.json --dbla_paths graph_alignments_train.json --cidra_paths graph_alignments_train_cidra.json --test_paths graph_alignments.json --cidra_seq cidra.nobg.sequences -o testrun/

    # import sys
    # import pickle
    # predictor_graph_name = sys.argv[1]
    # outcome_graph_name = sys.argv[2]
    # test_alignments = sys.argv[3]
    # train_alignments = sys.argv[4]
    # train_cidra_alignments = sys.argv[5] if len(sys.argv) > 5 else None
    # model = train_model(predictor_graph_name, outcome_graph_name, train_alignments, train_cidra_alignments)
    # # model = pickle.load(open("tmpmodel.pkl", "rb"))
    # pickle.dump(model, open("tmpmodel.pkl", "wb"), pickle.HIGHEST_PROTOCOL)
    # sequences = predict_sequences(
    #     model, test_alignments,
    #     outcome_graph_name.replace(".json", ".nobg.sequences"))
    # f = open("out.txt", "w")
    # for name, seq in sequences.items():
    #     f.write(">" + name + "\n")
    #     f.write(str(seq).upper()+"\n")
