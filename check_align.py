from Bio import SeqIO, pairwise2

def get_seqs(filename):
    seqs = SeqIO.to_dict(SeqIO.parse(filename, "fasta"))
    return {name: r.seq for name, r in seqs.items()}

def check_align(seq1, seq2):
    print(seq1, seq2)
    return pairwise2.align.globalxx(seq1, seq2, score_only=True)/len(seq2)

def main(pred_seqs, true_seqs):
    pairs = []
    for name, seq in pred_seqs.items():
        pairs.append((seq, true_seqs[name]))
        
    vals = [check_align(*pair) for pair in pairs]
    return vals

if __name__ == "__main__":
    import sys
    pred = get_seqs(sys.argv[1])
    true = get_seqs(sys.argv[2])
    res = main(pred, true)
    print(res)
    print("Mean: ", sum(res)/len(res))

    

