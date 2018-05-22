import pytest
import numpy as np
import offsetbasedgraph as obg


from malaria.corrstruct import *


@pytest.fixture
def corr_vec():
    return np.array([0, 1, 10, 2, 20])


@pytest.fixture
def corr_mat():
    return np.array(

        [[0, 0, 0, 0, 0],
         [0, 1, 10, 2, 20],
         [0, 2, 10, 4, 20],
         [0, 3, 10, 6, 20],
         [0, 4, 10, 8, 20]])


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


def test_get_correlation(path, corr_mat):
    c_vec = get_path_correlation(corr_mat, path)
    assert np.all(c_vec == [0, 4, 20, 8, 40])


def test_create_corr_stuct():
    predict_paths = {"A": {1, 3},
                     "B": {2, 4}}

    outcome_paths = {"B": {1, 3},
                     "A": {2, 4}}

    corr_mat = create_corr_struct(predict_paths,
                                  outcome_paths, 5, 5)

    assert np.all(corr_mat == np.array([[0, 0, 0, 0, 0],
                                        [0, 0, 1, 0, 1],
                                        [0, 1, 0, 1, 0],
                                        [0, 0, 1, 0, 1],
                                        [0, 1, 0, 1, 0]])/2)
