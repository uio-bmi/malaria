import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC, SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from collections import defaultdict


class DummyModel:
    def __init__(self, out):
        self._out = out

    def predict(self, input):
        return self._out


class NodeModel:
    def __init__(self, predictor_graph, outcome_graph=None):
        self._create_edge_lookup(predictor_graph.edges)

    def _create_edge_lookup(self, edges):
        adj_list = defaultdict(set)
        for edge in edges:
            adj_list[edge.from_node].add(edge.to_node)
        edges = [(edge.from_node, edge.to_node) for edge in edges
                 if len(adj_list[edge.from_node]) > 1]
        self.n_features = len(edges) + 1
        self.edge_lookup = defaultdict(int)
        self.edge_lookup.update({edge: i+1 for i, edge in enumerate(edges)})

    def _get_classifier(self):
        return LogisticRegression(penalty="l1", C=2)
        # LogisticRegression(multi_class="multinomial") # , penalty="l1", C=0.01)

    def get_X_matrix(self, predictor_paths):
        predictors = np.zeros((len(predictor_paths), self.n_features))
        for i, predictor_path in enumerate(predictor_paths):
            predictors[i, :] = self._path_to_feature_vector(predictor_path)
        return predictors

    def get_Y_dicts(self, outcome_paths):
        idx_dict = defaultdict(list)
        next_dict = defaultdict(list)
        for i, path in enumerate(outcome_paths):
            for node, next_node in zip([0]+path[:-1], path):
                idx_dict[node].append(i)
                next_dict[node].append(next_node)
        return idx_dict, next_dict

    def fit(self, predictor_paths, outcome_paths):
        X = self.get_X_matrix(predictor_paths)
        idx_dict, next_dict = self.get_Y_dicts(outcome_paths)
        self.models = {}
        for node, idx_list in idx_dict.items():
            nexts = np.array(next_dict[node])
            if np.unique(nexts).size == 1 or not len(idx_list):
                self.models[node] = DummyModel(nexts[0])
                continue
            features = X[idx_list]
            self.models[node] = self._get_classifier()
            self.models[node].fit(features, nexts)

    def _path_to_feature_vector(self, path):
        vec = np.zeros(self.n_features)
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
            last_node = cur_node
            cur_node = int(self.models[cur_node].predict(features))
            outcome_path.append(cur_node)
            i += 1
        return outcome_path


class NodeModelSVM(NodeModel):
    def _get_classifier(self):
        return SVC(decision_function_shape="ovo") # , kernel="poly", degree=2, C=0.5)


class NodeModelRF(NodeModel):
    def _get_classifier(self):
        return RandomForestClassifier()
