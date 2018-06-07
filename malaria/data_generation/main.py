import sys


"""
Steps when creating data.
Input: Fasta file with all possible protein sequences + clustal file with domain predictions for some sequences

Step 1: Filter out protein sequences that are also in clustal file and that have DBLa and CIDRa
Step 2: Choose only one sequence per isolate
Step 3: Split in train, test and validation
Step 4: Run mafft on train dbla and cidra
Step 5: Creat vg graphs, convert to json and creat ob graphs for both domains

"""


class DataCreator:
    def __init__(self, protein_sequences_file_name, domain_predictions_file_name):
        self.protein_sequences_file_name = protein_sequences_file_name
        self.domain_predictions_file_name = domain_predictions_file_name

    def run(self):
        self.



if __name__ == "__main__":
    assert len(sys.argv) == 3, "Usage: main.py fasta_sequences.fasta domain_predictions.clustal"





