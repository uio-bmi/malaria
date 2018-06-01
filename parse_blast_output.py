import sys
from Bio import SeqIO, pairwise2 
from pyfaidx import Fasta

blast_output = open(sys.argv[1])
train_seqs = Fasta(sys.argv[2])

mappings = {}
for line in blast_output:
    l = line.split()
    from_name = l[0]
    to_name = l[1]
    score = float(l[3])
    
    if from_name not in mappings or (from_name in mappings and mappings[from_name][1] < score):
        mappings[from_name] = (to_name, score)

for from_name, info in mappings.items():
    to_name = info[0]
    fasta_sequence = train_seqs[to_name]
    print(">" + from_name)
    print(fasta_sequence)


