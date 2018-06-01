from Bio import SeqIO, pairwise2
import matplotlib.pyplot as plt

def get_seqs(filename):
    seqs = SeqIO.to_dict(SeqIO.parse(filename, "fasta"))
    return {name: r.seq for name, r in seqs.items()}

def check_align(seq1, seq2):
    #print(seq1, seq2)
    return pairwise2.align.globalxx(seq1, seq2, score_only=True)/len(seq2)

def main(pred_seqs, true_seqs):
    pairs = {}
    for name, seq in pred_seqs.items():
        pairs[name] = (seq, true_seqs[name])
        
    vals = {name: check_align(*pair) for name, pair in pairs.items()}
    return vals

def plot_hist(vals):
    plt.hist(vals)
    plt.show()
    

if __name__ == "__main__":
    import sys
    pred_graph = get_seqs(sys.argv[1])
    pred_linear = get_seqs(sys.argv[2])
    true = get_seqs(sys.argv[3])
    res_graph = main(pred_graph, true)
    res_linear = main(pred_linear, true)
    print("Res graph: %d" % len(res_graph))
    print("Res graph: %d" % len(res_linear))
    print(res_graph)
    print(res_linear)
    graph_scores = sorted(res_graph.items(), key=lambda x: x[0])
    graph_scores = [item[1] for item in graph_scores]
    print("N linear: %d" % len(res_linear.items()))
    linear_scores = sorted(res_linear.items(), key=lambda x: x[0])
    linear_scores = [item[1] for item in linear_scores]
    print(len(graph_scores))
    print(len(linear_scores))
    plt.scatter(graph_scores, linear_scores)
    plt.show()
    print("Mean graph:: ", sum(res_graph.values())/len(res_graph))
    print("Mean graph:: ", sum(res_linear.values())/len(res_linear))

    

