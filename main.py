from measure_operator import SingleOp
from state import QState
import numpy as np

if __name__ == "__main__":
    a0 = SingleOp(0, 0, np.array([[1, 0], [0, 0]]))
    a1 = SingleOp(0, 1, np.array([[0, 0], [0, 1]]))
    
    b0 = SingleOp(1, 0, np.array([[1, 0], [0, 0]]))
    b1 = SingleOp(1, 1, np.array([[0, 0], [0, 1]]))

    rho = QState(0.5 * np.array([[1, 1], [1, 1]]))

    s0 = a0 * a1 + b0 * b1
    s1 = 3 * a0 * b0
    print(s0)

    