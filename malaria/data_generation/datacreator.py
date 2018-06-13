import sys
import clustal_parser
import logging
from Bio import SeqIO
from Bio.Seq import Seq
from random import shuffle, seed
seed(1)
from amino_acid_to_nucleotide import translate

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s, %(levelname)s: %(message)s")


class DataCreator:
    def __init__(self, protein_sequences_file_name, domain_predictions_file_name, n_train, n_test):
        self.n_test = n_test
        self.n_train = n_train
        self.proteins_file_name = protein_sequences_file_name
        self.domains = clustal_parser.parse_file(domain_predictions_file_name)
        self.fasta_entries_with_domains = []
        self.unique_sample_entries = []
        self.unique_sequence_entries = []
        self.train_records = []
        self.test_records = []

        self.run()

    def run(self):
        self.get_sequences_in_domain_predictions()
        self.remove_duplicate_samples()
        self.remove_duplicate_sequences()
        self.create_machine_learning_sets()
        self.write_machine_learning_sets_to_files()

    def get_sequences_in_domain_predictions(self):
        for record in SeqIO.parse(self.proteins_file_name, "fasta"):
            if record.id in self.domains:
                domains = self.domains[record.id]
                if "DBLa" in domains and "CIDRa" in domains:
                    record.protein_seq = record.seq
                    record.seq = Seq(translate(str(record.seq)))
                    self.fasta_entries_with_domains.append(record)


        logging.info("In total %d fasta entries having both domains" % len(self.fasta_entries_with_domains))

    def remove_duplicate_samples(self):
        samples_kept = set()
        assert len(self.fasta_entries_with_domains) > 0, "Run get_sequences_in_domains_predictions first"
        for record in self.fasta_entries_with_domains:
            sample_id = record.id.split("-")[0]
            if sample_id in samples_kept:
                continue

            samples_kept.add(sample_id)
            self.unique_sample_entries.append(record)

        logging.info("Kept %s/%s entries after removing"
                     " duplicates with same sample ids" %
                     (len(self.unique_sample_entries), len(self.fasta_entries_with_domains)))

    def remove_duplicate_sequences(self):
        # Remove based on identical sequences
        kept = set()
        assert len(self.unique_sample_entries) > 0, "Run remove_duplicate_samples() first"
        for record in self.unique_sample_entries:
            if record.seq in kept:
                continue
            kept.add(record.seq)
            self.unique_sequence_entries.append(record)

        logging.info("Kept %s/%s entries after removing"
                     " duplicates with same sequences " %
                     (len(self.unique_sequence_entries), len(self.unique_sample_entries)))

    def create_machine_learning_sets(self):
        logging.info("Creating sets. Train size: %d, test size: %d"
                        % (self.n_train, self.n_test))
        n_tot = self.n_train + self.n_test
        assert n_tot <= len(self.unique_sequence_entries), "There are fewer sequences than sum of set sizes. There are %d sequences." % len(self.unique_sequence_entries)

        sequences = self.unique_sequence_entries
        shuffle(sequences)
        self.train_records = sequences[0:self.n_train]
        self.test_records = sequences[self.n_train:self.n_train + self.n_test]

    def write_machine_learning_sets_to_files(self):
        for domain in ["DBLa", "CIDRa"]:
            for set_type, records in {"test": self.test_records, "train": self.train_records}.items():
                file_name = "%s_%s.fasta" % (domain.lower(), set_type)
                protein_file_name = "%s_%s_protein.fasta" % (domain.lower(), set_type)
                n_seqs = 0
                with open(file_name, "w") as f, open(protein_file_name, "w") as f_protein:
                    for record in records:
                        if domain in self.domains[record.id]:
                            domain_positions = self.domains[record.id][domain][0]
                            domain_sequence = record.seq[3*domain_positions[0]:3*(domain_positions[1]+1)]  # *3 since DNA
                            domain_sequence_protein = record.protein_seq[domain_positions[0]:domain_positions[1]+1]
                            f.writelines([">%s\n" % record.id])
                            f.writelines([str(domain_sequence + "\n")])
                            f_protein.writelines([">%s\n" % record.id])
                            f_protein.writelines([str(domain_sequence_protein) + "\n"])
                            n_seqs += 1

                logging.info("Wrote %d sequences to %s and %s" % (n_seqs, file_name, protein_file_name))
        logging.info("Done writing files")



if __name__ == "__main__":
    assert len(sys.argv) == 5, "Usage: main.py fasta_sequences.fasta domain_predictions.clustal n_test n_train"
    creator = DataCreator(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
    creator.get_sequences_in_domain_predictions()
    creator.remove_duplicate_samples()
    creator.remove_duplicate_sequences()
    creator.create_machine_learning_sets()
    creator.write_machine_learning_sets_to_files()






