import sys
import numpy as np
from offsetbasedgraph import NumpyIndexedInterval, Graph, Interval, SequenceGraph
from pyvg.conversion import vg_json_file_to_interval_collection

import sys
graph = Graph.from_file(sys.argv[2])
sequence_graph = SequenceGraph.from_file(sys.argv[2] + ".sequences")


alignments = vg_json_file_to_interval_collection(sys.argv[1], graph)
i = 1
alignment_intervals = []
for alignment in alignments:
    #indexed_alignments.append(alignment.to_numpy_indexed_interval())
    alignment_intervals.append(alignment)
    i += 1

paths = []
f = open("paths.txt")
j = 0
for path in f: 
    indexed = NumpyIndexedInterval.from_file(path.strip() + ".interval")
    interval = indexed.get_exact_subinterval(0, indexed.length())  # Hack to get interval
    interval.graph = graph
    paths.append(interval)
    j += 1

def show_sim_matrix():
    similarities = np.zeros((len(paths), len(paths)))
    for i, path in enumerate(paths):
        print(i)
        for j, path2 in enumerate(paths):
            match = path.overlap(path2) / path2.length()
            print(match)
            similarities[i, j] = match
            #if j >= 10:
            #    break
           
        #if i >= 10:
        #    break

    with open("sim_matrix.np", "w") as f:
        np.savetxt(f, similarities)
    print(similarities)

#show_sim_matrix()
#import sys
#sys.exit()

print(sequence_graph.get_interval_sequence(paths[3]))
print(sequence_graph.get_interval_sequence(alignment_intervals[0]))

print(paths[3])
print(alignment_intervals[0])
    
i = 0
alignment_intervals = [Interval(0, 1, [12, 14, 16, 19, 24, 26, 30, 33, 35, 37, 42, 43, 46], graph)]
for alignment in alignment_intervals:
    print("Alignment %d (length: %d) top matches:" % (i, alignment.length()))
    j = 0
    max_match = 0
    hits = []
    for path in paths:
        match = alignment.overlap(path)
        print("   Path %d: %.4f" % (j, match))
        hits.append((match, j, path.length()))
        j += 1

    hits = sorted(hits, key=lambda x: -x[0])
    for k in range(5):
        match = hits[k][0]
        print("  path %d with match %d bp, %.2f %% (%2.f %% of path length)" % (hits[k][1], match, 100 * match/alignment.length(), 100 * match/hits[k][2]))
    
    path1 = paths[hits[0][1]]
    path2 = paths[hits[1][1]]
    overlap = path1.overlap(path2)
    #print("  Bp overlap between path %d and %d: %.2f" % (hits[0][1], hits[1][1], overlap))

    i += 1

