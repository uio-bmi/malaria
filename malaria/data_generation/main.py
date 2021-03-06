import sys
import logging
from datacreator import DataCreator
from graph_creation import run_mafft
from pyvg.construct import construct_graph_from_msa
from pyvg.view import graph_to_json
from pyvg.conversion import json_file_to_obg_numpy_graph
from offsetbasedgraph import SequenceGraph
from amino_acid_to_nucleotide import translate
from Bio import SeqIO

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s, %(levelname)s: %(message)s")

"""
Steps when creating data.
Input: Fasta file with all possible protein sequences + clustal file with domain predictions for some sequences

Step 1: Filter out protein sequences that are also in clustal file and that have DBLa and CIDRa
Step 2: Choose only one sequence per isolate
Step 3: Split in train, test and validation
Step 4: Run mafft on train dbla and cidra
Step 5: Creat vg graphs, convert to json and creat ob graphs for both domains

"""

def protein_msa_to_dna(in_fasta, out_fasta):
    with open(out_fasta, "w") as out_file:
        for entry in SeqIO.parse(in_fasta, "fasta"):
            out_file.writelines([">%s\n%s\n" % (entry.id, translate(str(entry.seq)))])

    logging.info("Translated %s from protein to dna %s" % (in_fasta, out_fasta)) 


if __name__ == "__main__":

    assert len(sys.argv) == 6, "Usage: main.py fasta_sequences.fasta domain_predictions.clustal n_test n_train n_train_in_graph out_path"

    creator = DataCreator(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))

    logging.info("Running mafft")
    run_mafft("dbla_train_protein.fasta", "dbla_protein.msa", gap_extension_penalty=-0.85, limit_to_n_first_sequences=int(sys.argv[5]))
    run_mafft("cidra_train_protein.fasta", "cidra_protein.msa", gap_extension_penalty=-0.85, limit_to_n_first_sequences=int(sys.argv[5]))
    protein_msa_to_dna("dbla_protein.msa", "dbla.msa") 
    protein_msa_to_dna("cidra_protein.msa", "cidra.msa") 

    logging.info("Constructing graphs")
    construct_graph_from_msa("dbla.msa", "dbla.vg")
    construct_graph_from_msa("cidra.msa", "cidra.vg")

    graph_to_json("dbla.vg", "dbla.json")
    graph_to_json("cidra.vg", "cidra.json")
 
    dbla_graph = json_file_to_obg_numpy_graph("dbla.json")
    dbla_graph.to_numpy_file("dbla.nobg")
    cidra_graph = json_file_to_obg_numpy_graph("cidra.json")
    cidra_graph.to_numpy_file("cidra.nobg") 
    sequence_graph = SequenceGraph.create_empty_from_ob_graph(dbla_graph)
    sequence_graph.set_sequences_using_vg_json_graph("dbla.json")
    sequence_graph.to_file("dbla.nobg.sequences")

    sequence_graph = SequenceGraph.create_empty_from_ob_graph(cidra_graph)
    sequence_graph.set_sequences_using_vg_json_graph("cidra.json")
    sequence_graph.to_file("cidra.nobg.sequences")



