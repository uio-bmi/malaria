from data_generation.amino_acid_to_nucleotide import translate
from Bio import SeqIO
import sys

in_fasta = sys.argv[1]
out_fasta = sys.argv[2]

with open(out_fasta, "w") as out_file:
    for entry in SeqIO.parse(in_fasta, "fasta"):
        out_file.writelines([">%s\n%s\n" % (entry.id, translate(str(entry.seq)))])
    print("Translated %s from protein to dna %s" % (in_fasta, out_fasta))
