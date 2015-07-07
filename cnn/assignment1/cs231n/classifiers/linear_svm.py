import numpy as np
from random import shuffle


def svm_loss_naive(W, X, y, reg):
    """
    Structured SVM loss function, naive implementation (with loops)
    Inputs:
    - W: C x D array of weights
    - X: D x N array of data. Data are D-dimensional columns
    - y: 1-dimensional array of length N with labels 0...K-1, for K classes
    - reg: (float) regularization strength
    Returns:
    a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    dW = np.zeros(W.shape)  # initialize the gradient as zero

    # compute the loss and the gradient
    num_classes = W.shape[0]
    num_train = X.shape[1]
    loss = 0.0
    dW += reg * W

    for i in xrange(num_train):
        n = 0
        scores = W.dot(X[:, i])
        correct_class_score = scores[y[i]]
        for j in xrange(num_classes):
            if j == y[i]:
                continue
            margin = scores[j] - correct_class_score + 1  # note delta = 1
            if margin > 0:
                n += 1
                loss += margin
                dW[j, :] += X[:, i].T / (float(num_train))
        dW[y[i], :] += -n * X[:, i].T / (float(num_train))

    # Right now the loss is a sum over all training examples, but we want it
    # to be an average instead so we divide by num_train.
    loss /= num_train

    # Add regularization to the loss.
    loss += 0.5 * reg * np.sum(W * W)

    #############################################################################
    # TODO:                                                                     #
    # Compute the gradient of the loss function and store it dW.                #
    # Rather that first computing the loss and then computing the derivative,   #
    # it may be simpler to compute the derivative at the same time that the     #
    # loss is being computed. As a result you may need to modify some of the    #
    # code above to compute the gradient.                                       #
    #############################################################################


    return loss, dW


def _transY(y, classes):
    N = y.shape[0]
    C = len(classes)
    Y = np.zeros((N, C))
    for i, yi in enumerate(y):
        Y[i, yi] = 1
    return Y


def svm_loss_vectorized(W, X, y, reg):
    """
    Structured SVM loss function, vectorized implementation.

    Inputs and outputs are the same as svm_loss_naive.
    """
    loss = 0.0
    dW = np.zeros(W.shape)  # initialize the gradient as zero
    dW += reg * W
    #############################################################################
    # TODO:                                                                     #
    # Implement a vectorized version of the structured SVM loss, storing the    #
    # result in loss.                                                           #
    #############################################################################
    num_classes = W.shape[0]
    num_train = X.shape[1]
    scores = W.dot(X)
    correct_class_scores = scores[y, range(num_train)]
    margins = scores - correct_class_scores + 1
    margins[margins < 0] = 0
    margins[margins == 1.0] = 0

    signs = margins > 0

    # for j in xrange(num_classes):
    # dW[j, :] += signs[j, :].dot(X.T) / (float(num_train))
    dW += signs.dot(X.T) / (float(num_train))
    ns = np.sum(signs, axis=0)
    t = X * ns
    Y = _transY(y, range(num_classes))
    dW -= t.dot(Y).T / (float(num_train))
    loss = sum(sum(margins))

    loss /= num_train
    loss += 0.5 * reg * np.sum(W * W)
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################


    #############################################################################
    # TODO:                                                                     #
    # Implement a vectorized version of the gradient for the structured SVM     #
    # loss, storing the result in dW.                                           #
    #                                                                           #
    # Hint: Instead of computing the gradient from scratch, it may be easier    #
    # to reuse some of the intermediate values that you used to compute the     #
    # loss.                                                                     #
    #############################################################################
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################

    return loss, dW