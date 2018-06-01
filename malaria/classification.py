import numpy as np
from sklearn.linear_model import LogisticRegression
from collections import defaultdict


class DummyModel:
    def __init__(self, out):
        self._out = out

    def predict(self, input):
        return self._out


class NodeModel:
    def __init__(self, predictor_graph, outcome_graph):
        self.edges = np.array([(edge.from_node, edge.to_node)
                               for edge in predictor_graph.edges])
        # self.nodes = np.array([node.id for node in outcome_graph.nodes])
        self.edge_lookup = {(edge.from_node, edge.to_node): i
                            for i, edge in enumerate(predictor_graph.edges)}
        # self.node_lookup = {node: i for i, node in enumerate(self.nodes)}

    def fit(self, predictor_paths, outcome_paths):
        predictors = np.zeros((len(predictor_paths), self.edges.shape[0]))
        for i, predictor_path in enumerate(predictor_paths):
            predictors[i, :] = self._path_to_feature_vector(predictor_path)
        idx_dict = defaultdict(list)
        next_dict = defaultdict(list)
        for i, path in enumerate(outcome_paths):
            for node, next_node in zip([0]+path[:-1], path):
                idx_dict[node].append(i)
                next_dict[node].append(i)
        self.models = {}
        N = len(idx_dict.keys())
        i = 0
        for node, idx_list in idx_dict.items():
            if i % 100 == 0:
                print("Node %s/%s" % (i, N))
            i += 1
            nexts = np.array(next_dict[node])
            if np.unique(nexts).size == 1:
                self.models[node] = DummyModel(nexts[0])
                continue
            features = predictors[idx_list]
            self.models[node] = LogisticRegression()
            self.models[node].fit(features, nexts)

    def _path_to_feature_vector(self, path):
        vec = np.zeros(self.edges.shape[0])
        edges = zip(path[:-1], path[1:])
        idxs = [self.edge_lookup[edge] for edge in edges]
        vec[idxs] = 1
        return vec

    def predict(self, predictor_path):
        features = self._path_to_feature_vector(predictor_path)[None, :]
        cur_node = 0
        outcome_path = []
        i = 0
        while cur_node in self.models:
            print(i, cur_node)
            last_node = cur_node
            cur_node = int(self.models[cur_node].predict(features))
            if last_node == cur_node:
                print(cur_node)
                raise
            outcome_path.append(cur_node)
            i += 1
        return outcome_path
