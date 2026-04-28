import numpy as np
from measure_operator import *
from state import QState

class MomentMatrix:
    def __init__(self, ops: list, state: QState):
        self.words = [IdentityOp(state.matrix.shape)]
        for op in ops:
            if isinstance(op, SingleOp):
                self.words.append(OpContainer(op))
            else:
                self.words.append(op)
        
