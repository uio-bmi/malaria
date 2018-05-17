import sys

mappings = {}

f = open(sys.argv[1])
for line in f:
    l = line.strip().split()
    from_id = l[1]
    to_id = l[0]

    mappings[from_id] = to_id
f.close()

f = open(sys.argv[2])
for line in f:
    line = line.strip()
    if not line.startswith(">"):
        print(line)
    else:
        id = line.replace(">", "").split()[0]
        line = line.replace(id, mappings[id])    
        print(line)
