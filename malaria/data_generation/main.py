import sys
import logging
from datacreator import DataCreator
from graph_creation import run_mafft
from pyvg.construct import construct_graph_from_msa
from pyvg.view import graph_to_json
from pyvg.conversion import json_file_to_obg_numpy_graph

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

if __name__ == "__main__":
    assert len(sys.argv) == 5, "Usage: main.py fasta_sequences.fasta domain_predictions.clustal n_test n_train"

    creator = DataCreator(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))

    logging.info("Running mafft")
    run_mafft("dbla_train.fasta", "dbla.msa")
    run_mafft("cidra_train.fasta", "cidra.msa")

    logging.info("Constructing graphs")
    construct_graph_from_msa("dbla.msa", "dbla.vg")
    construct_graph_from_msa("cidra.msa", "cidra.vg")

    graph_to_json("dbla.vg", "dbla.json")
    graph_to_json("cidra.vg", "cidra.json")

    json_file_to_obg_numpy_graph("dbla.json")
    json_file_to_obg_numpy_graph("cidra.json")








