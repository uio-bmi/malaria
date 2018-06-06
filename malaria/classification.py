import numpy as np
import sklearn.linear_model.LogisticRegression 
from collections import defaultdict

class SparseEdges:
    def __init__(self, edges):
        edges = np.asanyarray(edges)
        args = np.lexsort((edges[:, 0], edges[:, 1]))
        self._to_nodes = edges[args, 1]
        from_edges = edges[args, 0]
        self._row_pointers = np.flatnonzero(from_edges[:-1] != from_edges[1:])


class NodeModel:
    def __init__(self, predictor_graph, outcome_graph):
        self.edges = np.array([(getattr(edge, "from"), edge.to)
                               for edge in predictor_graph.edges])
        self.nodes = np.array([node.id for node in outcome_graph.nodes])
        self.edge_lookup = {edge: i for i, edge in enumerate(self.edges)}
        self.node_lookup = {node: i for i, node in enumerate(self.nodes)}

    def fit(self, predictor_paths, outcome_paths):
        predictors = np.zeros((len(predictor_paths), self.edges.shape[0]))
        idx_dict = defaultdict(list)
        next_dict = defaultdict(list)
        for i, path in enumerate(outcome_paths):
            for node, next_node in zip([0]+path[:-1], path]):
                idx_dict[node].append(i)
                next_dict[node].append(i)

        for node, idx_list in idx_dict.items():
            idxs = 

        for i, predictor_path in enumerate(predictor_paths):
            predictors[i, :] = self._path_to_feature_vector(predictor_path)

        for outcome_path in outcome_paths:
            for node, next_node in outcome_paths:
                pass

    def _path_to_feature_vector(self, path):
        pass

    def predict(self, predictor_path):



class LogisticNodeModel:
    pass
