import matplotlib.pyplot as plt
import sys                                                                                                                                                                                                                                                                            
import numpy as np
from offsetbasedgraph import NumpyIndexedInterval, Graph, Interval, SequenceGraph
from pyvg.conversion import vg_json_file_to_interval_collection


dbla_graph = Graph.from_file(sys.argv[1])
cidra_graph = Graph.from_file(sys.argv[2])

dbla_paths = []
cidra_paths = []
f = open(sys.argv[3])
j = 0
for path in f: 
     indexed = NumpyIndexedInterval.from_file("dbla_paths/" + path.strip() + ".interval")
     interval = indexed.get_exact_subinterval(0, indexed.length())  # Hack to get interval
     interval.graph = dbla_graph
     dbla_paths.append(interval)

     indexed = NumpyIndexedInterval.from_file("cidra_paths/" + path.strip() + ".interval")
     interval = indexed.get_exact_subinterval(0, indexed.length())  # Hack to get interval
     interval.graph = cidra_graph
     cidra_paths.append(interval)

     j += 1

print(dbla_paths)

def get_sim_matrix(paths):
    similarities = np.zeros((len(paths), len(paths)))
    for i, path in enumerate(paths):
         print(i)
         for j, path2 in enumerate(paths):
             if j >= i:
                break
             match = path.overlap(path2) / path2.length()
             similarities[i, j] = match
             #if j >= 15:
             #    break
 
         #if i >= 15:
         #    break
 
    return similarities

dbla_sims = get_sim_matrix(dbla_paths)
cidra_sims = get_sim_matrix(cidra_paths)

print(dbla_sims)
print(cidra_sims)

pair_sims_dbla = []
pair_sims_cidra = []


for i in range(0, len(dbla_paths)):
    for j in range(0, len(cidra_paths)):
        if j >= i:
            break

        pair_sims_dbla.append(dbla_sims[i, j])
        pair_sims_cidra.append(cidra_sims[i, j])


print(pair_sims_dbla)
print(pair_sims_cidra)

plt.scatter(pair_sims_dbla, pair_sims_cidra)
plt.show()
