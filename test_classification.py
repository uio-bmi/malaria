from malaria.classification import NodeModel
from collections import namedtuple
import numpy as np
import pytest

Graph = namedtuple("Graph", ["edges"])
Edge = namedtuple("Edge", ["from_node", "to_node"])

@pytest.fixture
def predictor_graph():
    edges = [(1, 2), (1, 3), (2, 4), (3, 4)]
    edges = [Edge(*e) for e in edges]
    return Graph(edges)

@pytest.fixture
def outcome_graph():
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 6), (5, 6)]
    edges = [Edge(*e) for e in edges]
    return Graph(edges)

    
@pytest.fixture
def predictor_paths():
    return [[1, 2, 4], [1, 3, 4]]

@pytest.fixture
def outcome_paths():
    return [[1, 3, 6], [1, 2, 4, 6]]

@pytest.fixture
def node_model():
    return NodeModel(predictor_graph())


def test_init(predictor_graph):
    model = NodeModel(predictor_graph)
    true_lookup = {(1, 2): 1, (1, 3): 2}
    assert model.edge_lookup == true_lookup
    assert model.n_features == 3

def test_get_X(node_model, predictor_paths):
    X = node_model.get_X_matrix(predictor_paths)
    true_X = np.array([[1, 1, 0],
                       [1, 0, 1]])
    assert np.all(X == true_X)

def test_get_Y(node_model, outcome_paths):
    idx_dict, next_dict = node_model.get_Y_dicts(outcome_paths)
    true_idx_dict = {0: [0, 1], 1: [0, 1], 2: [1], 3: [0], 4: [1]}
    assert idx_dict == true_idx_dict

    true_next_dict = {0: [1, 1], 1: [3, 2], 2: [4], 3: [6], 4: [6]}
    assert next_dict == true_next_dict

def test_fit(predictor_graph, predictor_paths, outcome_paths):
    model = NodeModel(predictor_graph)
    model.fit(predictor_paths, outcome_paths)

    
    

