from collections import defaultdict
import itertools


def parse_file(filename):
    cur_seq = None
    domains = {}
    with open(filename) as f:
        for line in f:
            if line.startswith("Query sequence"):
                cur_seq = line.split()[-1].strip()
                domains[cur_seq] = defaultdict(list)
            parts = line.split()
            if not ("from" in parts and "to" in parts):
                continue
            domain = parts[0][:-1]
            start = int(parts[6])
            end = int(parts[8][:-1])
            domains[cur_seq][domain].append((start, end))
    return domains


def get_domain(lookup, name, file_name, f=None, count=-1):
    out_file = open(name + "_" + file_name, "w")
    cur_lines = []
    cur_name = None

    with open(file_name) as f:
        for line in f:
            if line.startswith(">"):
                if cur_name is not None:
                    seq = "".join(cur_lines)
                    for i, part in enumerate(lookup[cur_name][name]):
                        out_file.write(">%s %s %s\n" % (cur_name, name, i))
                        out_file.write(seq[part[0]:part[1]+1]+"\n")
                cur_name = line.split()[0][1:]
                cur_lines = []
            else:
                cur_lines.append(line.strip())
    seq = "".join(cur_lines)
    for i, part in enumerate(lookup[cur_name][name]):
        out_file.write(">%s %s %s" % (cur_name, name, i))
        out_file.write(seq[part[0]:part[1]+1])
        cur_name = line.split()[0][1:]
        cur_lines = []
    out_file.close()


def test():
    lookup = parse_file("train.clustal")
    domains = set(itertools.chain.from_iterable(lookup.values()))
    for domain in domains:
        get_domain(lookup, domain, "1000_train_dna.fasta_all.fasta")
    print("FINISHED!")
    # get_domain(lookup, "DBLa", "1000_train_dna.fasta_all.fasta")

if __name__ == "__main__":
    test()
