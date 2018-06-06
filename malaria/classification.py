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
    def __init__(self, predictor_graph, outcome_graph):
        # self.edges = np.array([(edge.from_node, edge.to_node)
        # for edge in predictor_graph.edges])
        # self.nodes = np.array([node.id for node in outcome_graph.nodes])
        self._create_edge_lookup(predictor_graph.edges)
        # self.edge_lookup = {(edge.from_node, edge.to_node): i
        #                     for i, edge in enumerate(predictor_graph.edges)}
        # self.node_lookup = {node: i for i, node in enumerate(self.nodes)}

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
        return LogisticRegression(multi_class="multinomial") # , penalty="l1", C=0.01)

    def set_pca(self, features):
        print(features.shape)
        self.pca = PCA(n_components=1000)
        self.pca.fit(features)

    def fit(self, predictor_paths, outcome_paths):
        predictors = np.zeros((len(predictor_paths), self.n_features))
        for i, predictor_path in enumerate(predictor_paths):
            predictors[i, :] = self._path_to_feature_vector(predictor_path)
        # self.set_pca(predictors)
        # predictors = self.pca.transform(predictors)
        idx_dict = defaultdict(list)
        next_dict = defaultdict(list)
        for i, path in enumerate(outcome_paths):
            for node, next_node in zip([0]+path[:-1], path):
                idx_dict[node].append(i)
                next_dict[node].append(next_node)
        self.models = {}
        N = len(idx_dict.keys())
        i = 0
        print(predictors.size)
        for node, idx_list in idx_dict.items():
            if i % 100 == 0:
                print("Node %s/%s" % (i, N))
            i += 1
            nexts = np.array(next_dict[node])
            if np.unique(nexts).size == 1 or not len(idx_list):
                self.models[node] = DummyModel(nexts[0])
                continue
            features = predictors[idx_list]
            self.models[node] = LogisticRegression(penalty="l1", C=2)
            self.models[node].fit(features, nexts)

    def _path_to_feature_vector(self, path):
        vec = np.zeros(self.n_features)
        edges = zip(path[:-1], path[1:])
        idxs = [self.edge_lookup[edge] for edge in edges]
        vec[idxs] = 1
        return vec

    def predict(self, predictor_path):
        features = self._path_to_feature_vector(predictor_path)[None, :]
        # features = self.pca.transform(features)
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
