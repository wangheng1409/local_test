# -*- coding:utf-8 -*-

"""Utilities to evaluate pairwise distances or metrics between 2
sets of points.

Distance metrics are a function d(a, b) such that d(a, b) < d(a, c) if objects
a and b are considered "more similar" to objects a and c. Two objects exactly
alike would have a distance of zero.
One of the most popular examples is Euclidean distance.
To be a 'true' metric, it must obey the following four conditions::

    1. d(a, b) >= 0, for all a and b
    2. d(a, b) == 0, if and only if a = b, positive definiteness
    3. d(a, b) == d(b, a), symmetry
    4. d(a, c) <= d(a, b) + d(b, c), the triangle inequality

"""

from scipy import sparse
import numpy as np
import scipy.spatial.distance as ssd
from scipy.stats import spearmanr as spearman
from scipy.sparse import issparse
from scipy.sparse import csr_matrix
import inspect

from math import *
from decimal import Decimal

if 'order' in inspect.getargspec(np.copy)[0]:
    def safe_copy(X):
        # Copy, but keep the order
        return np.copy(X, order='K')
else:
    # Before an 'order' argument was introduced, numpy wouldn't muck with
    # the ordering
    safe_copy = np.copy


def _assert_all_finite(X):
    """Like assert_all_finite, but only for ndarray."""
    if X.dtype.char in np.typecodes['AllFloat'] and not np.isfinite(X.sum()) and not np.isfinite(X).all():
        raise ValueError("Array contains NaN or infinity.")


def assert_all_finite(X):
    """Throw a ValueError if X contains NaN or infinity.

    Input MUST be an np.ndarray instance or a scipy.sparse matrix."""

    # First try an O(n) time, O(1) space solution for the common case that
    # there everything is finite; fall back to O(n) space np.isfinite to
    # prevent false positives from overflow in sum method.
    _assert_all_finite(X.data if sparse.issparse(X) else X)


def safe_asarray(X, dtype=None, order=None):
    """Convert X to an array or sparse matrix.

    Prevents copying X when possible; sparse matrices are passed through."""
    if sparse.issparse(X):
        assert_all_finite(X.data)
    else:
        X = np.asarray(X, dtype, order)
        assert_all_finite(X)
    return X


def array2d(X, dtype=None, order=None, copy=False):
    """Returns at least 2-d array with data from X"""
    if sparse.issparse(X):
        raise TypeError('A sparse matrix was passed, but dense data '
                        'is required. Use X.toarray() to convert to dense.')
    X_2d = np.asarray(np.atleast_2d(X), dtype=dtype, order=order)
    _assert_all_finite(X_2d)
    if X is X_2d and copy:
        X_2d = safe_copy(X_2d)
    return X_2d


def _atleast2d_or_sparse(X, dtype, order, copy, sparse_class, convmethod):
    if sparse.issparse(X):
        # Note: order is ignored because CSR matrices hold data in 1-d arrays
        if dtype is None or X.dtype == dtype:
            X = getattr(X, convmethod)()
        else:
            X = sparse_class(X, dtype=dtype)
        _assert_all_finite(X.data)
    else:
        X = array2d(X, dtype=dtype, order=order, copy=copy)
        _assert_all_finite(X)
    return X


def atleast2d_or_csc(X, dtype=None, order=None, copy=False):
    """Like numpy.atleast_2d, but converts sparse matrices to CSC format.

    Also, converts np.matrix to np.ndarray.
    """
    return _atleast2d_or_sparse(X, dtype, order, copy, sparse.csc_matrix,
                                "tocsc")


def atleast2d_or_csr(X, dtype=None, order=None, copy=False):
    """Like numpy.atleast_2d, but converts sparse matrices to CSR format

    Also, converts np.matrix to np.ndarray.
    """
    return _atleast2d_or_sparse(X, dtype, order, copy, sparse.csr_matrix,
                                "tocsr")


def safe_sparse_dot(a, b, dense_output=False):
    """Dot product that handle the sparse matrix case correctly"""
    from scipy import sparse
    if sparse.issparse(a) or sparse.issparse(b):
        ret = a * b
        if dense_output and hasattr(ret, "toarray"):
            ret = ret.toarray()
        return ret
    else:
        return np.dot(a, b)


# Utility Functions
def check_pairwise_arrays(X, Y):
    """ Set X and Y appropriately and checks inputs

    If Y is None, it is set as a pointer to X (i.e. not a copy).
    If Y is given, this does not happen.
    All distance metrics should use this function first to assert that the
    given parameters are correct and safe to use.

    Specifically, this function first ensures that both X and Y are arrays,
    then checks that they are at least two dimensional. Finally, the function
    checks that the size of the second dimension of the two arrays is equal.

    Parameters
    ----------
    X : {array-like, sparse matrix}, shape = [n_samples_a, n_features]

    Y : {array-like, sparse matrix}, shape = [n_samples_b, n_features]

    Returns
    -------
    safe_X : {array-like, sparse matrix}, shape = [n_samples_a, n_features]
        An array equal to X, guaranteed to be a numpy array.

    safe_Y : {array-like, sparse matrix}, shape = [n_samples_b, n_features]
        An array equal to Y if Y was not None, guaranteed to be a numpy array.
        If Y was None, safe_Y will be a pointer to X.

    """
    if Y is X or Y is None:
        X = safe_asarray(X)
        X = Y = atleast2d_or_csr(X, dtype=np.float)
    else:
        X = safe_asarray(X)
        Y = safe_asarray(Y)
        X = atleast2d_or_csr(X, dtype=np.float)
        Y = atleast2d_or_csr(Y, dtype=np.float)
    if len(X.shape) < 2:
        raise ValueError("X is required to be at least two dimensional.")
    if len(Y.shape) < 2:
        raise ValueError("Y is required to be at least two dimensional.")
    if X.shape[1] != Y.shape[1]:
        raise ValueError("Incompatible dimension for X and Y matrices: "
                         "X.shape[1] == %d while Y.shape[1] == %d" % (
                             X.shape[1], Y.shape[1]))
    return X, Y


# Distances
def euclidean_distances(X, Y=None, Y_norm_squared=None, squared=False,
                        inverse=False):
    """
    Considering the rows of X (and Y=X) as vectors, compute the
    distance matrix between each pair of vectors.

    For efficiency reasons, the euclidean distance between a pair of row
    vector x and y is computed as::

        dist(x, y) = sqrt(dot(x, x) - 2 * dot(x, y) + dot(y, y))

    This formulation has two main advantages. First, it is computationally
    efficient when dealing with sparse data. Second, if x varies but y
    remains unchanged, then the right-most dot-product `dot(y, y)` can be
    pre-computed.


    An implementation of a "similarity" based on the Euclidean "distance"
    between two users X and Y. Thinking of items as dimensions and
    preferences as points along those dimensions, a distance is computed
    using all items (dimensions) where both users have expressed a preference
    for that item. This is simply the square root of the sum of the squares
    of differences in position (preference) along each dimension.

    The similarity could be computed as 1 / (1 + distance), so the resulting
    values are in the range (0,1].

    Parameters
    ----------
    X : {array-like, sparse matrix}, shape = [n_samples_1, n_features]

    Y : {array-like, sparse matrix}, shape = [n_samples_2, n_features]

    Y_norm_squared : array-like, shape = [n_samples_2], optional
        Pre-computed dot-products of vectors in Y (e.g.,
        ``(Y**2).sum(axis=1)``)

    squared : boolean, optional
        This routine will return squared Euclidean distances instead.

    inverse: boolean, optional
        This routine will return the inverse Euclidean distances instead.


    Returns
    -------
    distances : {array, sparse matrix}, shape = [n_samples_1, n_samples_2]


    """
    # should not need X_norm_squared because if you could precompute that as
    # well as Y, then you should just pre-compute the output and not even
    # call this function.
    X, Y = check_pairwise_arrays(X, Y)

    if issparse(X):
        XX = X.multiply(X).sum(axis=1)
    else:
        XX = np.sum(X * X, axis=1)[:, np.newaxis]

    if X is Y:  # shortcut in the common case euclidean_distances(X, X)
        YY = XX.T
    elif Y_norm_squared is None:
        if issparse(Y):
            # scipy.sparse matrices don't have element-wise scalar
            # exponentiation, and tocsr has a copy kwarg only on CSR matrices.
            YY = Y.copy() if isinstance(Y, csr_matrix) else Y.tocsr()
            YY.data **= 2
            YY = np.asarray(YY.sum(axis=1)).T
        else:
            YY = np.sum(Y ** 2, axis=1)[np.newaxis, :]
    else:
        YY = atleast2d_or_csr(Y_norm_squared)
        if YY.shape != (1, Y.shape[0]):
            raise ValueError(
                "Incompatible dimensions for Y and Y_norm_squared")

    # TODO: a faster Cython implementation would do the clipping of negative
    # values in a single pass over the output matrix.
    distances = safe_sparse_dot(X, Y.T, dense_output=True)
    distances *= -2
    distances += XX
    distances += YY
    np.maximum(distances, 0, distances)

    if X is Y:
        # Ensure that distances between vectors and themselves are set to 0.0.
        # This may not be the case due to floating point rounding errors.
        distances.flat[::distances.shape[0] + 1] = 0.0

    distances = np.divide(1.0, (1.0 + distances)) if inverse else distances

    return distances if squared else np.sqrt(distances)


euclidian_distances = euclidean_distances  # both spelling for backward compatibility


def manhattan_distances(X, Y):
    """
    Considering the rows of X (and Y=X) as vectors, compute the
    distance matrix between each pair of vectors.

    This distance implementation is the distance between two points in a grid
    based on a strictly horizontal and/or vertical path (that is, along the
    grid lines as opposed to the diagonal or "as the crow flies" distance.
    The Manhattan distance is the simple sum of the horizontal and vertical
    components, whereas the diagonal distance might be computed by applying the
    Pythagorean theorem.

    The resulting unbounded distance is then mapped between 0 and 1.

    Parameters
    ----------
    X: array of shape (n_samples_1, n_features)

    Y: array of shape (n_samples_2, n_features)

    Returns
    -------
    distances: array of shape (n_samples_1, n_samples_2)

    """

    if issparse(X) or issparse(Y):
        raise ValueError("manhattan_distance does"
                         "not support sparse matrices.")
    X, Y = check_pairwise_arrays(X, Y)
    n_samples_X, n_features_X = X.shape
    n_samples_Y, n_features_Y = Y.shape
    if n_features_X != n_features_Y:
        raise Exception("X and Y should have the same number of features!")
    D = np.abs(X[:, np.newaxis, :] - Y[np.newaxis, :, :])
    D = np.sum(D, axis=2)

    return 1.0 - (D / float(n_features_X))


def pearson_correlation(X, Y):
    """
    Considering the rows of X (and Y=X) as vectors, compute the
    distance matrix between each pair of vectors.

    This correlation implementation is equivalent to the cosine similarity
    since the data it receives is assumed to be centered -- mean is 0. The
    correlation may be interpreted as the cosine of the angle between the two
    vectors defined by the users preference values.

    Parameters
    ----------
    X : {array-like, sparse matrix}, shape = [n_samples_1, n_features]

    Y : {array-like, sparse matrix}, shape = [n_samples_2, n_features]

    Returns
    -------
    distances : {array, sparse matrix}, shape = [n_samples_1, n_samples_2]

    """

    X, Y = check_pairwise_arrays(X, Y)

    # should not need X_norm_squared because if you could precompute that as
    # well as Y, then you should just pre-compute the output and not even
    # call this function.

    # TODO: Fix to work with sparse matrices.
    if issparse(X) or issparse(Y):
        raise ValueError('Pearson does not yet support sparse matrices.')

    if X is Y:
        X = Y = np.asanyarray(X)
    else:
        X = np.asanyarray(X)
        Y = np.asanyarray(Y)

    if X.shape[1] != Y.shape[1]:
        raise ValueError("Incompatible dimension for X and Y matrices")

    XY = ssd.cdist(X, Y, 'correlation')

    return 1 - XY


def adjusted_cosine(X, Y, E):
    """
    For item based recommender systems, the basic cosine measure and Pearson correlation measure does not take the
    differences in the average rating behavior of the users into account. Some users tend to be too harsh while others
    tend to do be too soft. This behaviour, known as "grade inflation", is solved by using the adjusted cosine measure,
    which subtracts the user average from the item vector of ratings. The values for the adjusted cosine
    measure correspondingly range from −1 to +1, as in the Pearson measure. The adjusted cosine distance is obtained
    adding 1 to the measure value.

    This formula is from a seminal article in collaborative filtering: "Item-based collaborative filtering
    recommendation algorithms" by Badrul Sarwar, George Karypis, Joseph Konstan, and John Reidl
    (http://www.grouplens.org/papers/pdf/www10_sarwar.pdf)

    Considering the rows of X (and Y=X) as vectors, compute the
    distance matrix between each pair of vectors after normalize or adjust
    the vector using the EFV vector. EFV vector contains expected value for
    each feature from vectors X and Y, i.e., the mean of the values
    of each feature vector from X and Y.

    Parameters
    ----------
    X : {array-like, sparse matrix}, shape = [n_samples_1, n_features]

    Y : {array-like, sparse matrix}, shape = [n_samples_2, n_features]

    E: {array-like, sparse matrix}, shape = [n_samples_3, n_features]

    Returns
    -------
    distances : {array, sparse matrix}, shape = [n_samples_1, n_samples_2]

    Examples
    --------

    """

    X, Y = check_pairwise_arrays(X, Y)
    # TODO: fix next line
    E, _ = check_pairwise_arrays(E, None)

    # should not need X_norm_squared because if you could precompute that as
    # well as Y, then you should just pre-compute the output and not even
    # call this function.

    # TODO: Fix to work with sparse matrices.
    if issparse(X) or issparse(Y) or issparse(E):
        raise ValueError('Adjusted cosine does not yet support sparse matrices.')

    if X is Y:
        X = Y = np.asanyarray(X)
    else:
        X = np.asanyarray(X)
        Y = np.asanyarray(Y)

    if X.shape[1] != Y.shape[1] != E.shape[1]:
        raise ValueError("Incompatible dimension for X, Y and EFV matrices")

    X = X - E
    Y = Y - E

    XY = 1 - ssd.cdist(X, Y, 'cosine')

    return XY


def jaccard_coefficient(X, Y):
    """
    Considering the rows of X (and Y=X) as vectors, compute the
    distance matrix between each pair of vectors.

    This correlation implementation is a statistic used for comparing the
    similarity and diversity of sample sets.
    The Jaccard coefficient measures similarity between sample sets,
    and is defined as the size of the intersection divided by the size of the
    union of the sample sets.

    Parameters
    ----------
    X: array of shape (n_samples_1, n_features)

    Y: array of shape (n_samples_2, n_features)

    Returns
    -------
    distances: array of shape (n_samples_1, n_samples_2)


    """

    X = safe_asarray(X)
    Y = safe_asarray(Y)

    # TODO: Fix to work with sparse matrices.
    if issparse(X) or issparse(Y):
        raise ValueError('Jaccard does not yet support sparse matrices.')

    # TODO: Check if it is possible to optimize this function
    sX = X.shape[0]
    sY = Y.shape[0]
    dm = np.zeros((sX, sY))
    for i in xrange(0, sX):
        for j in xrange(0, sY):
            sx = set(X[i])
            sy = set(Y[j])
            n_XY = len(sx & sy)
            d_XY = len(sx | sy)
            dm[i, j] = n_XY / float(d_XY)
    return dm


def tanimoto_coefficient(X, Y):
    """
    Considering the rows of X (and Y=X) as vectors, compute the
    distance matrix between each pair of vectors.

    An implementation of a "similarity" based on the Tanimoto coefficient,
    or extended Jaccard coefficient.

    This is intended for "binary" data sets where a user either expresses a
    generic "yes" preference for an item or has no preference. The actual
    preference values do not matter here, only their presence or absence.

    Parameters
    ----------
    X: array of shape n_samples_1

    Y: array of shape n_samples_2

    Returns
    -------
    distances: array of shape (n_samples_1, n_samples_2)


    """
    return jaccard_coefficient(X, Y)


def cosine_distances(X, Y):
    """
    Considering the rows of X (and Y=X) as vectors, compute the
    distance matrix between each pair of vectors.

     An implementation of the cosine similarity. The result is the cosine of
     the angle formed between the two preference vectors.
     Note that this similarity does not "center" its data, shifts the user's
     preference values so that each of their means is 0. For this behavior,
     use Pearson Coefficient, which actually is mathematically
     equivalent for centered data.

    Parameters
    ----------
    X: array of shape (n_samples_1, n_features)

    Y: array of shape (n_samples_2, n_features)

    Returns
    -------
    distances: array of shape (n_samples_1, n_samples_2)


    """
    X, Y = check_pairwise_arrays(X, Y)

    # TODO: Fix to work with sparse matrices.
    if issparse(X) or issparse(Y):
        raise ValueError('Cosine does not yet support sparse matrices.')

    return 1. - ssd.cdist(X, Y, 'cosine')


def sorensen_coefficient(X, Y):
    """
    Considering the rows of X (and Y=X) as vectors, compute the
    distance matrix between each pair of vectors.

    The Sørensen index, also known as Sørensen’s similarity coefficient,
    is a statistic used for comparing the similarity of two samples.
    It was developed by the botanist Thorvald Sørensen and published in 1948.
    [1]
    See the link:http://en.wikipedia.org/wiki/S%C3%B8rensen_similarity_index

    This is intended for "binary" data sets where a user either expresses a
    generic "yes" preference for an item or has no preference. The actual
    preference values do not matter here, only their presence or absence.

    Parameters
    ----------
    X: array of shape (n_samples_1, n_features)

    Y: array of shape (n_samples_2, n_features)

    Returns
    -------
    distances: array of shape (n_samples_1, n_samples_2)


    """
    # should not need X_norm_squared because if you could precompute that as
    # well as Y, then you should just pre-compute the output and not even
    # call this function.
    if X is Y:
        X = Y = np.asanyarray(X)
    else:
        X = np.asanyarray(X)
        Y = np.asanyarray(Y)

    sX = X.shape[0]
    sY = Y.shape[0]
    dm = np.zeros((sX, sY))

    # TODO: Check if it is possible to optimize this function
    for i in xrange(0, sX):
        for j in xrange(0, sY):
            sx = set(X[i])
            sy = set(Y[j])
            n_XY = len(sx & sy)
            dm[i, j] = (2.0 * n_XY) / (len(X[i]) + len(Y[j]))

    return dm


def _spearman_r(X, Y):
    """
    Calculates a Spearman rank-order correlation coefficient
    and the p-value to test for non-correlation.
    """
    rho, p_value = spearman(X, Y)
    return rho


def spearman_coefficient(X, Y):
    """
    Considering the rows of X (and Y=X) as vectors, compute the
    distance matrix between each pair of vectors.

    Like  Pearson Coefficient , but compares relative ranking of preference
    values instead of preference values themselves. That is, each user's
    preferences are sorted and then assign a rank as their preference value,
    with 1 being assigned to the least preferred item.

    Parameters
    ----------
    X: array of shape (n_samples_1, n_features)

    Y: array of shape (n_samples_2, n_features)

    Returns
    -------
    distances: array of shape (n_samples_1, n_samples_2)


    """
    # should not need X_norm_squared because if you could precompute that as
    # well as Y, then you should just pre-compute the output and not even
    # call this function.
    if X is Y:
        X = Y = np.asanyarray(X, dtype=[('x', 'S30'), ('y', float)])
    else:
        X = np.asanyarray(X, dtype=[('x', 'S30'), ('y', float)])
        Y = np.asanyarray(Y, dtype=[('x', 'S30'), ('y', float)])

    if X.shape[1] != Y.shape[1]:
        raise ValueError("Incompatible dimension for X and Y matrices")

    X.sort(order='y')
    Y.sort(order='y')

    result = []

    # TODO: Check if it is possible to optimize this function
    i = 0
    for arrayX in X:
        result.append([])
        for arrayY in Y:
            Y_keys = [key for key, value in arrayY]

            XY = [(key, value) for key, value in arrayX if key in Y_keys]

            sumDiffSq = 0.0
            for index, tup in enumerate(XY):
                sumDiffSq += pow((index + 1) - (Y_keys.index(tup[0]) + 1), 2.0)

            n = len(XY)
            if n == 0:
                result[i].append(0.0)
            else:
                result[i].append(1.0 - ((6.0 * sumDiffSq) / (n * (n * n - 1))))
        result[i] = np.asanyarray(result[i])
        i += 1

    return np.asanyarray(result)


def loglikehood_coefficient(n_items, X, Y):
    """
    Considering the rows of X (and Y=X) as vectors, compute the
    distance matrix between each pair of vectors.

    Parameters
    ----------
    n_items: int
        Number of items in the model.

    X: array of shape (n_samples_1, n_features)

    Y: array of shape (n_samples_2, n_features)

    Returns
    -------
    distances: array of shape (n_samples_1, n_samples_2)

    References
    ----------
    See http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.14.5962 and
    http://tdunning.blogspot.com/2008/03/surprise-and-coincidence.html.
    """

    # should not need X_norm_squared because if you could precompute that as
    # well as Y, then you should just pre-compute the output and not even
    # call this function.

    def safeLog(d):
        if d <= 0.0:
            return 0.0
        else:
            return np.log(d)

    def logL(p, k, n):
        return k * safeLog(p) + (n - k) * safeLog(1.0 - p)

    def twoLogLambda(k1, k2, n1, n2):
        p = (k1 + k2) / (n1 + n2)
        return 2.0 * (logL(k1 / n1, k1, n1) + logL(k2 / n2, k2, n2)
                      - logL(p, k1, n1) - logL(p, k2, n2))

    if X is Y:
        X = Y = np.asanyarray(X)
    else:
        X = np.asanyarray(X)
        Y = np.asanyarray(Y)

    result = []

    # TODO: Check if it is possible to optimize this function

    i = 0
    for arrayX in X:
        result.append([])
        for arrayY in Y:
            XY = np.intersect1d(arrayX, arrayY)

            if XY.size == 0:
                result[i].append(0.0)
            else:
                nX = arrayX.size
                nY = arrayY.size
                if (nX - XY.size == 0) or (n_items - nY) == 0:
                    result[i].append(1.0)
                else:
                    logLikelihood = twoLogLambda(float(XY.size),
                                                 float(nX - XY.size),
                                                 float(nY),
                                                 float(n_items - nY))

                    result[i].append(1.0 - 1.0 / (1.0 + float(logLikelihood)))
        result[i] = np.asanyarray(result[i])
        i += 1

    return np.asanyarray(result)


class Similarity():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    """ Five similarity measures function """

    def euclidean_distance(self):
        x = self.x
        y = self.y
        """ return euclidean distance between two lists """

        return sqrt(sum(pow(a - b, 2) for a, b in zip(x, y)))

    def manhattan_distance(self):
        x = self.x
        y = self.y
        """ return manhattan distance between two lists """

        return sum(abs(a - b) for a, b in zip(x, y))

    def minkowski_distance(self, p_value):
        x = self.x
        y = self.y
        """ return minkowski distance between two lists """

        return self.nth_root(sum(pow(abs(a - b), p_value) for a, b in zip(x, y)), p_value)

    def nth_root(self, value, n_root):
        """ returns the n_root of an value """

        root_value = 1 / float(n_root)
        return round(Decimal(value) ** Decimal(root_value), 3)

    def cosine_similarity(self):
        x = self.x
        y = self.y
        """ return cosine similarity between two lists """

        numerator = sum(a * b for a, b in zip(x, y))
        denominator = self.square_rooted(x) * self.square_rooted(y)
        return round(numerator / float(denominator), 3)

    def square_rooted(self, x):
        """ return 3 rounded square rooted value """

        return round(sqrt(sum([a * a for a in x])), 3)

    def jaccard_similarity(self):
        x = self.x
        y = self.y
        """ returns the jaccard similarity between two lists """

        intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
        union_cardinality = len(set.union(*[set(x), set(y)]))
        return intersection_cardinality / float(union_cardinality)


import sys

SE = [0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, -1, -1, -1, 0, 1, 1, 0, 0, 1, -1, 0, 1, -1, -1, 1, 0, 1, 1, 1, 1, 1,
      1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1]


def get_expect_value(x, y):
    x_positive_num = 0
    y_positive_num = 0
    x_negative_num = 0
    y_negative_num = 0
    RE = []
    for index in range(len(SE)):
        if SE[index] == 0:
            RE.append(x[index] + y[index])
        else:
            if SE[index] == 1:
                x_positive_num += x[index]
                y_positive_num += y[index]
                RE.append(max(x[index], y[index]))
            elif SE[index] == -1:
                x_negative_num += x[index]
                y_negative_num += y[index]
                RE.append(min(x[index], y[index]))
    return RE, x_positive_num, y_positive_num, x_negative_num, y_negative_num


CITY_INFO = {
    52: {'gdp_2015': 2296860000000, 'residents': 21705000, 'area': 16412, 'population_density': 1323,
               'pgdp': 105822, 'adcode': '110100'},
    503: {'gdp_2015': 464020000000, 'residents': 3955000, 'area': 455, 'population_density': 8692, 'pgdp': 117325, 'adcode': '110105'},
    502: {'gdp_2015': 461350000000, 'residents': 3694000, 'area': 431, 'population_density': 8571, 'pgdp': 124892, 'adcode': '110108'},
    501: {'gdp_2015': 327040000000, 'residents': 1298000, 'area': 51, 'population_density': 25451, 'pgdp': 251957, 'adcode': '110102'},
    500: {'gdp_2015': 185780000000, 'residents': 905000, 'area': 42, 'population_density': 21548, 'pgdp': 205282, 'adcode': '110101'},
    506: {'gdp_2015': 116990000000, 'residents': 2324000, 'area': 306, 'population_density': 7595, 'pgdp': 50340, 'adcode': '110106'},
    507: {'gdp_2015': 43020000000, 'residents': 652000, 'area': 84, 'population_density': 7762, 'pgdp': 65982, 'adcode': '110107'},
    511: {'gdp_2015': 144090000000, 'residents': 1020000, 'area': 1020, 'population_density': 1000,
               'pgdp': 141265, 'adcode': '110113'},
    512: {'gdp_2015': 65730000000, 'residents': 1963000, 'area': 1344, 'population_density': 1461, 'pgdp': 33484, 'adcode': '110114'},
    510: {'gdp_2015': 59450000000, 'residents': 1378000, 'area': 906, 'population_density': 1521, 'pgdp': 43142, 'adcode': '110112'},
    508: {'gdp_2015': 55470000000, 'residents': 1046000, 'area': 1990, 'population_density': 526, 'pgdp': 53031, 'adcode': '110111'},
    515: {'gdp_2015': 15910000000, 'residents': 1562000, 'area': 1036, 'population_density': 1508, 'pgdp': 101895, 'adcode': '110115'},
    509: {'gdp_2015': 14450000000, 'residents': 308000, 'area': 1451, 'population_density': 212, 'pgdp': 46916, 'adcode': '110109'},
    513: {'gdp_2015': 23420000000, 'residents': 384000, 'area': 2123, 'population_density': 181, 'pgdp': 60990, 'adcode': '110116'},
    516: {'gdp_2015': 22670000000, 'residents': 479000, 'area': 2229, 'population_density': 215, 'pgdp': 47328, 'adcode': '110118'},
    514: {'gdp_2015': 19620000000, 'residents': 423000, 'area': 950, 'population_density': 445, 'pgdp': 46383, 'adcode': '110117'},
    517: {'gdp_2015': 10735000000, 'residents': 314000, 'area': 1993, 'population_density': 157, 'pgdp': 34188, 'adcode': '110119'},
}


def get_adjusted_cosine(x, y):
    RE, x_positive_num, y_positive_num, x_negative_num, y_negative_num = get_expect_value(x, y)
    return adjusted_cosine([x], [y], [RE])[0][0], x_positive_num, y_positive_num, x_negative_num, y_negative_num


if __name__ == '__main__':
    X2 = [982, 0, 2, 0, 26, 86, 8, 2, 0, 0, 42, 0, 5, 4, 339, 14, 0, 6, 93, 209, 289, 249, 1, 23, 81, 71, 92, 64, 21,
          11, 10, 27, 7, 57, 0, 2, 81, 50, 887, 0, 99, 1111, 820, 13, 30, 24, 8, 224, 0, 103, 69, 79]
    Y2 = [828, 0, 2, 0, 22, 86, 54, 2, 0, 0, 37, 1, 6, 5, 289, 11, 0, 6, 58, 251, 285, 214, 1, 16, 73, 56, 111, 31, 20,
          14, 10, 28, 11, 37, 0, 2, 57, 53, 694, 0, 57, 892, 620, 13, 32, 12, 6, 189, 0, 83, 71, 78]
    SE = [0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, -1, -1, -1, 0, 1, 1, 0, 0, 1, -1, 0, 1, -1, -1, 1, 0, 1, 1, 1, 1,
          1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1]

    RE, x_positive_num, y_positive_num, x_negative_num, y_negative_num = get_expect_value(X2, Y2)

    print RE
    print adjusted_cosine([X2], [Y2], [RE])
    print len(RE)
    print x_positive_num, y_positive_num, x_negative_num, y_negative_num
    print cosine_distances([X2], [Y2])
    print pearson_correlation([X2], [Y2])
