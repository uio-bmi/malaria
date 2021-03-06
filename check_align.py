from Bio import SeqIO, pairwise2
from Bio.SubsMat import MatrixInfo as matlist
import matplotlib.pyplot as plt
import logging
import csv


def get_seqs(filename):
    seqs = SeqIO.to_dict(SeqIO.parse(filename, "fasta"))
    return {name: r.seq for name, r in seqs.items()}


def check_align(seq1, seq2):
    matrix = matlist.blosum62
    return pairwise2.align.globaldx(seq1, seq2, matrix, score_only=True)/len(seq2)


def main(pred_seqs, true_seqs):
    pairs = {}
    for name, seq in pred_seqs.items():
        try:
            pairs[name] = (seq, true_seqs[name])
        except KeyError:
            print("Error: %s not found in true sequences." % name) 

    vals = {name: check_align(*pair) for name, pair in pairs.items()}
    return vals

def plot_hist(vals):
    plt.hist(vals)
    plt.show()
    

def plot_curves(graph_scores, linear_scores):
    def plt_curve(scores):
        fails = [1-s for s in scores]
        fails.sort()
        counts = list(range(len(fails)))
        plt.plot(fails, counts)
    plt_curve(graph_scores)
    plt_curve(linear_scores)
    plt.show()

def write_results(filename, graph_dict, linear_dict):
    triplets = ((name, graph_dict[name], linear_dict[name])
                for name in linear_dict)
    with open(filename, "w") as f:
        f.write("# " + "\t".join(("SeqId", "GraphScore", "LinearScore")) + "\n")
        f.writelines("%s\t%s\t%s\n" % triplet for triplet in triplets)


if __name__ == "__main__":
    import sys
    pred_graph = get_seqs(sys.argv[1])

    true = get_seqs(sys.argv[3])
    res_graph = main(pred_graph, true)
    print("###GRAPH:", sum(res_graph.values())/len(res_graph))
    pred_linear = get_seqs(sys.argv[2])
    res_linear = main(pred_linear, true)
    print("N graph: %d" % len(res_graph))
    print("N linear: %d" % len(res_linear))
    #write_results(sys.argv[1]+"_compare.csv", res_graph, res_linear)
    graph_scores = []
    linear_scores = []
    for seq_name, score in res_graph.items():
        # if seq_name in res_linear:
        graph_scores.append(score)
        linear_scores.append(res_linear[seq_name])
    
    #graph_scores = sorted(res_graph.items(), key=lambda x: x[0])
    #graph_scores = [item[1] for item in graph_scores]
    print("N linear: %d" % len(res_linear.items()))
    #linear_scores = sorted(res_linear.items(), key=lambda x: x[0])
    #linear_scores = [item[1] for item in linear_scores]
    print(len(graph_scores))
    print(len(linear_scores))
    print("Mean graph:: ", sum(res_graph.values())/len(res_graph))
    print("Mean linear:: ", sum(res_linear.values())/len(res_linear))
    try:
        plot_curves(graph_scores, linear_scores)
        plt.scatter(linear_scores, graph_scores)
        plt.plot([0.65,1], [0.65, 1])
        plt.xlabel("Linear")
        plt.ylabel("Graph")
        plt.show()
    except Exception:
        logging.error("Could not show plot.")
    

