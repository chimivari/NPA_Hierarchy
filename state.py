import numpy as np

class QState:
    def __init__(self, matrix):
        if abs(np.trace(matrix) - 1.0) > 0.0001:
            raise ValueError('State should be normalized so that tr(rho) = 1')
        self.matrix = matrix


