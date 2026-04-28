import numpy as np

class IdentityOp:
    def __init__(self, shape):
        self.op = np.identity(shape)

class OpContainer:
    NEXT_INDEX = 0
    def __init__(self, single_op, coef = None):
        if not isinstance(single_op, SingleOp):
            raise ValueError('Argument type incorrect')
        if coef != None:
            self.op_list = [[coef, single_op]]
            self.op = single_op.op * coef
        else:
            self.op_list = [[single_op]]
            self.op = single_op.op

        self.id = self.NEXT_INDEX
        OpContainer.NEXT_INDEX += 1
    
    def __add__(self, other):
        if isinstance(other, SingleOp):
            self.op_list.append([other])
            self.op += other.op
            return self
        elif isinstance(other, OpContainer):
            self.op_list.extend(other.op_list)
            self.op += other.op
            return self
        raise ValueError('Invalid argument type')
    
    def __mul__(self, other):
        if isinstance(other, SingleOp):
            self.op_list[-1].append(other)
            self.op = np.matmul(self.op, other.op)
            return self
        raise ValueError('Invalid argument type')
    
    def __repr__(self):
        s = ''
        for i in range(len(self.op_list)):
            for j in range(len(self.op_list[i])):
                s += f'{self.op_list[i][j]} '
            if i < len(self.op_list) - 1:
                s += '+ '
        return s

class SingleOp:
    def __init__(self, id_observer, id_outcome, op):
        """
        :param id_observer: identifiant de l'observeur (0 Alice, 1 Bob)
        :param id_outcome: différencie les outcome (exemple alpha = 0, alpha' = 1 (alpha != alpha'))
        :param op: opérateur
        """
        self.id_observer = id_observer
        self.id_outcome = id_outcome
        self.op = op
    
    def __add__(self, other):
        if isinstance(other, SingleOp):
            return OpContainer(self) + other
        raise ValueError('Argument type incorrect')
    
    def __mul__(self, other):
        if isinstance(other, SingleOp):
            return OpContainer(self) * other
        raise ValueError('Argument type incorrect')
    
    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, complex):
            return OpContainer(self, other)
        raise ValueError('Argument type incorrect')
    
    def __repr__(self):
        return f"{chr(ord('A') + self.id_observer)}{self.id_outcome}"