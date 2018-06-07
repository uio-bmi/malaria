import logging

amino_acid_to_dna_dict = \
    {
        "I": "ATT",
        "L": "CTT",
        "V": "GTT",
        "F": "TTT",
        "M": "ATG",
        "C": "TGT",
        "A": "GCT",
        "G": "GGT",
        "P": "CCT",
        "T": "ACT",
        "S": "TCT",
        "Y": "TAT",
        "W": "TGG",
        "Q": "CAA",
        "N": "AAT",
        "H": "CAT",
        "E": "GAA",
        "D": "GAT",
        "K": "AAA",
        "R": "CGT",
        "*": "TAA",
        "X": "NNN" # Unknown
    }

def translate(sequence):
    nucleotides = []
    for amino_acid in sequence:
        try:
            nucleotides.append(amino_acid_to_dna_dict[amino_acid])
        except KeyError:
            logging.error("Could not find amino acid %s in translation dict" % amino_acid)
            raise
    return ''.join(nucleotides)