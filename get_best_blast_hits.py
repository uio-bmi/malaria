import sys

already_returned = set()
with open(sys.argv[1]) as in_file:
    for line in in_file:
        query_id = line.split()[0]
        if query_id not in already_returned:
            print(line.strip())
            already_returned.add(query_id)
        
