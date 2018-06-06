import glob
import hashlib
import sys
from random import shuffle

def get_fasta_data(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        if len(lines) == 0:
            print("Warning: %s is empty" % file_name)
            return "", ""
        try:
            header = lines[0].split()[0].replace(">", "")
        except IndexError:
            print(lines)

        return header, ''.join(lines[1:])

def get_checksum(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


kept_checksums = set()
kept = {i: [] for i in range(0, 4)}

n_files = 0
n_tot = 0
files = glob.glob("*-*.fasta")
shuffle(files)

all_fasta_entries = []

sample_ids = set()
for file in files:
    header, text = get_fasta_data(file)
    sample_id = header.split("-")[0]
    sample_ids.add(sample_id)
    
    checksum = get_checksum(text)
    n_tot += 1
    if checksum in kept_checksums:
        print("Duplicate %s" % header)
        continue

    if n_files < 8000:
        kept[n_files//2000].append(">%s\nQ%s" % (header, text))

    all_fasta_entries.append(">%s\nQ%s" % (header, text))
    
    kept_checksums.add(checksum)

    n_files += 1

for i, kept in kept.items():
    with open("out" + str(i) + ".fasta", "w") as f:
        f.writelines(kept)
        print("Wrote part to out" + str(i) + ".fasta")
        
with open("all.fasta", "w") as f:
    f.writelines(all_fasta_entries)
    print("Wrote everything to all.fasta")

print("N unique samples: %d" % len(sample_ids))
print(n_files)
print("Tot: %d" % n_tot)
