import argparse
import json
import pickle
import logging
from pyvg import Graph, Alignment
import offsetbasedgraph as obg

from .classification import NodeModel, NodeModelSVM, NodeModelRF


def get_sequence(sequence_graph, node_ids):
    interval = obg.Interval(
        0, sequence_graph._node_sizes[node_ids[-1]], node_ids)
    return sequence_graph.get_interval_sequence(interval)


def get_path_dict(filename):
    for line in open(filename):
        try: 
            json.loads(str(line).strip())
        except:
            print(str(line).strip())
            raise
    try:
        alignments = (json.loads(str(line).strip()) for line in open(filename) if line.strip())

        alignments = (Alignment.from_json(alignment) for alignment in alignments)
        path_dict = {alignment.name: [mapping.start_position.node_id
                                      for mapping in alignment.path.mappings]
                     for alignment in alignments}
    except Exception as e:
        print(e)
        raise
    
    return path_dict

def get_model(model_name):
    models = {"logistic": NodeModel,
              "svm": NodeModelSVM,
              "randomforest": NodeModelRF}
    return models[model_name]

def train(args):
    print("Training")
    model = args.classifier(args.dbla_graph)
    keys = list(args.dbla_paths.keys())
    pred_paths = [args.dbla_paths[key] for key in keys if key in args.cidra_paths]
    out_paths = [args.cidra_paths[key] for key in keys if key in args.cidra_paths]
    print("Fitting")
    model.fit(pred_paths, out_paths)
    pickle.dump(model, open(args.out+model.__class__.__name__+".mdl", "wb"),
                pickle.HIGHEST_PROTOCOL)
    return model


def predict_sequence(path, model, sequence_graph):
    predicted_path = model.predict(path)
    predicted_sequence = get_sequence(sequence_graph, predicted_path)
    return predicted_sequence

def test(args, model=None):
    print("Testing")
    paths = args.test_paths
    print("Predicting")
    N = len(paths)
    i = 0
    out_file = args.out+"predicted_cidra_sequences_%s.fasta" % model.name
    with open(out_file, "w") as f:
        for name, path in paths.items():
            if i % 100 == 0:
                print("\t Node %s of %s" % (i, N))
            i += 1
            seq = predict_sequence(path, model, args.cidra_seq)
            f.write(">" + name + "\n")
            f.write(str(seq).upper()+"\n")
            logging.info("Wrote predictions to %s" % (out_file))
    
    #predicted_paths = {name: model.predict(path) for
    #                   name, path in paths.items()}
    #print("Finding Sequences")
    #sequences = {name: get_sequence(args.cidra_seq, path)
    #             for name, path in predicted_paths.items()}
    #with open(args.out+"predicted_cidra_sequences.fasta", "w") as f:
    #    for name, seq in sequences.items():
    #        f.write(">" + name + "\n")
    #        f.write(str(seq).upper()+"\n")

def load_model(filename):
    return pickle.load(open(filename, "rb"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbla_graph", type=Graph.from_file, help="json graph of dbla")
    parser.add_argument("--dbla_paths", type=get_path_dict, help="json alignments for dbla training seqs")
    parser.add_argument("--cidra_paths", type=get_path_dict, help="json alignments for cidra training seqs")
    parser.add_argument("--cidra_seq", type=obg.SequenceGraph.from_file, help="Sequence graph for cidra")
    parser.add_argument("--test_paths", type=get_path_dict, help="json alignments for dbla test seqs")
    parser.add_argument("--classifier", "-c", type=get_model, default="logistic", help="[logistic, svm, randomforest]")
    parser.add_argument("--out", "-o", default="out", help="outfolder")
    parser.add_argument("--model", "-m", type=load_model, help="saved model")
    args = parser.parse_args()
    model = args.model
    if args.model is None:
        model = train(args)
    test(args, model)
    return args
