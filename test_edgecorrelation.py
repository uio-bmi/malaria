import pytest
import numpy as np
import offsetbasedgraph as obg


from malaria.edgestruct import *


@pytest.fixture
def corr_vec():
    return {(0, 1): 1,
            (1, 2): 10,
            (1, 3): 2,
            (2, 4): 10,
            (3, 4): 2}

@pytest.fixture
def corr_dict():
    return {
        (0, 1): {(0, 1): 1, (1, 2): 10, (1, 3): 2, (2, 4): 20, (3, 4): 20},
        (1, 2): {(0, 1): 2, (1, 2): 10, (1, 3): 4, (2, 4): 20, (3, 4): 20},
        (1, 3): {(0, 1): 3, (1, 2): 10, (1, 3): 6, (2, 4): 20, (3, 4): 20},
        (2, 4): {(0, 1): 4, (1, 2): 10, (1, 3): 8, (2, 4): 20, (3, 4): 20},
        (3, 4): {(0, 1): 4, (1, 2): 10, (1, 3): 8, (2, 4): 20, (3, 4): 20}}

@pytest.fixture
def path():
    return [1, 3]


@pytest.fixture
def graph():
    return obg.Graph({i+1: obg.Block(10) for i in range(4)},
                     {1: [2, 3], 2: [4], 3: [4]})


def test_predict(corr_vec, graph):
    path = predict_path(corr_vec, graph)
    assert path == [1, 2, 4]


def test_get_correlation(path, corr_dict):
    c_vec = get_path_correlation(corr_dict, path)
    true = {(0, 1): 4,
            (1, 2): 20,
            (1, 3): 8,
            (2, 4): 40,
            (3, 4): 40}
    assert c_vec == true

def test_create_corr_stuct():
    predict_paths = {"A": [1, 3, 4],
                     "B": [1, 2, 4]}

    outcome_paths = {"B": [1, 3, 4],
                     "A": [1, 2, 4]}

    corr_mat = create_corr_struct(predict_paths,
                                  outcome_paths)
    print(corr_mat.keys())
    true = {
        (0, 1): {(0, 1):   1, (1, 2): 0.5, (1, 3): 0.5,  (2, 4): 0.5, (3, 4): 0.5},
        (1, 2): {(0, 1):   1, (1, 2): 0,   (1, 3): 1,   (2, 4): 0,   (3, 4): 1},
        (1, 3): {(0, 1):   1, (1, 2): 1,   (1, 3): 0,   (2, 4): 1,   (3, 4): 0},
        (2, 4): {(0, 1):   1, (1, 2): 0,   (1, 3): 1,   (2, 4): 0,   (3, 4): 1},
        (3, 4): {(0, 1):   1, (1, 2): 1,   (1, 3): 0,   (2, 4): 1,   (3, 4): 0}}

    for k, v in true.items():
        for k2, v2 in v.items():
            assert corr_mat[k][k2] == v2

    # assert corr_mat == true
