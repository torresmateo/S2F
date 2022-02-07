import abc

import numpy as np
import pandas as pd
from scipy import sparse
from itertools import combinations
from Utils import FancyApp
from rich.progress import track

class Graph(FancyApp.FancyApp):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def compute_graph(self):
        """
        Computes protein-protein graph(s)
        """

    @abc.abstractmethod
    def get_graph(self, **kwargs):
        """
        Return the computed graph
        :return: scipy matrix or dictionary of scipy matrices
        """

    @abc.abstractmethod
    def write_graph(self, filename):
        """
        Saves the computed graph in text format
        :param filename: the path to write the graph
        """

    @staticmethod
    def assert_lexicographical_order(df, p1='Protein 1', p2='Protein 2'):
        """
        Guarantees that lexicographical order is maintained in the
        dataframe so that df[p1] < df_col[p2]
        :param df: The dataframe to modify
        :param p1: the name of the min column
        :param p2: the name of the max column
        :return: None
        """
        # 3.- we guarantee the lexicographical order between
        # the protein columns, that is,
        # that df_col.protein1 < df_col.protein2
        min_protein = df[[p1, p2]].min(axis=1)
        max_protein = df[[p1, p2]].max(axis=1)
        df.loc[:, p1] = min_protein
        df.loc[:, p2] = max_protein

    @staticmethod
    def ij2triangular(rows, cols, n):
        """
        Transforms the rows and columns coordinates to a 1 dimensional index
        which corresponds to the upper triangle of a n*n matrix.

        This mapping is consistent only for coordinates over the main diagnonal

        taken from https://stackoverflow.com/q/27086195/943138

        :param rows: np.array of the rows
        :param cols: np.array of the columns
        :param n: number of nodes in the matrix
        :return: np.array indexing in 1 dimension
        """
        return (n*(n-1)/2) - (n-rows)*((n-rows)-1)/2 + cols - rows - 1
        # return ((cols-1)*n + rows) - ( n*(n-1)/2 - (n-cols)*(n-cols+1)/2 )

    @staticmethod
    def cumulative_row_lengths(n):
        x = np.arange(n-1, 0, -1)
        a = []
        for i, v in enumerate(x):
            if i == 0:
                a.append(v)
            else:
                a.append(a[i-1]+v)
        return np.array(a)
    
    @staticmethod
    def triangular2ij(indices, n):
        """
        Inverse of `ij2triangular`
        :param indices: np.array of indices
        :param n: number of nodes in the matrix
        :return: rows, cols in 2D coordinates
        """
        if n > 25000:
            rows = []
            cols = []
            for i in track(range(n), description="creating full rows and cols"):
                for j in range(i+1, n):
                    rows.append(i)
                    cols.append(j)
        else:
            rows = n - 2 - np.floor(np.sqrt(-8 * indices + 4 * n * (n - 1) - 7) /
                                    2.0 - 0.5)
            cols = indices + rows + 1 - n * (n - 1) / 2 +\
                (n - rows) * ((n - rows) - 1) / 2
        return rows, cols

    @staticmethod
    def to_sparse_vector(x):
        """
        Given a (N, N) sparse matrix in COO format, returns a sparse matrix
        of dimensions (N*(N-1)/2, 1), which keeps only the upper triangle
        above the main diagonal.

        This function requires that x is the output of scipy.sparse.triu(m, 1)

        :param x: scipy.sparse.coo_matrix with shape (N, N)
        :return: scipy.sparse.coo_matrix with shape (N*(N-1)/2, 1)
        """
        n = x.shape[0]
        cols = np.zeros(x.data.shape[0])
        rows = Graph.ij2triangular(x.row, x.col, n)
        return sparse.coo_matrix((x.data, (rows, cols)),
                                 shape=(int(n*(n-1)/2), 1))

    @staticmethod
    def to_sparse_matrix(x):
        """
        The inverse of `to_sparse_vector`
        :param x: scipy.sparse.coo_matrix with shape (N*(N-1)/2, 1)
        :return: scipy.sparse.coo_matrix with shape (N, N)
        """
        n = int((1+np.sqrt(8*x.shape[0] + 1))/2)
        rows, cols = Graph.triangular2ij(x.row, n)
        return sparse.coo_matrix((x.data, (rows, cols)),
                                 shape=(n, n))

    @staticmethod
    def fill_lower_triangle(x):
        """
        Given a sparse matrix with only the upper triangle, fill the
        lower triangle and return.

        :param x: scipy.sparse.coo_matrix with shape (N, N)
        :return: scipy.sparse.coo_matrix with shape (N, N)
        """
        return sparse.coo_matrix(
            sparse.triu(x, 1) + sparse.triu(x, 1).T
        )

    @staticmethod
    def numpy_to_pandas(adjacency, proteins):
        """transform a numpy array into a pandas DataFrame

        Parameters
        ----------
        adjacency : np.ndarray
            adjacency matrix
        proteins : List[str]
            the names of the nodes, it must correspond to the adjacency matrix

        Returns
        -------
        pd.DataFrame
            the PPI in pandas format
        """
        data = {'p1': [], 'p2': [], 'w': []}
        for p1, p2 in combinations(range(len(proteins)), 2):
            data['p1'].append(proteins[p1])
            data['p2'].append(proteins[p2])
            data['w'].append(adjacency[p1, p2])
        return pd.DataFrame(data)
