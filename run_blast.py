import sys
from Bio import SeqIO
import subprocess

def run_blast_single_seq(fasta_entry, blast_database):
    # Write sequence temporary to file
    with open("blast_seq.tmp", "w") as f:
        f.writelines([">%s\n%s" % (fasta_entry.id, fasta_entry.seq)])

    blast_command = "blastn -query blast_seq.tmp -db %s -outfmt 6" % (blast_database)
    blast_result = subprocess.check_output(blast_command.split())
    blast_result = blast_result.decode("utf-8")
    best_hit = blast_result.split("\n")[0].split()[1]
    print("Blasting %s" % fasta_entry.id)
    return best_hit 
        

if __name__ == "__main__":
    blast_db = sys.argv[2]
    out_file_name = sys.argv[4]

    cidra_sequences = {entry.id: entry.seq for entry in SeqIO.parse(sys.argv[3], "fasta")}
    blast_hits = {entry.id: run_blast_single_seq(entry, blast_db) for entry in SeqIO.parse(sys.argv[1], "fasta")}
    predicted = [(fasta_id, cidra_sequences[predicted_id]) for fasta_id, predicted_id in blast_hits.items()] 
    
    with open(out_file_name, "w") as f:
        for fasta_id, sequence in predicted:
            f.writelines([">%s\n%s\n" % (fasta_id, sequence)])

    print("Wrote predictions to %s" % out_file_name)
    



