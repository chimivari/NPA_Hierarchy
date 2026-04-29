import copy

class MomentMatrixElement:
    def __init__(self, group):
        if isinstance(group[0], identity):
            self.value = 1
        else:
            self.value = group
    
    def __repr__(self):
        if self.value == 1:
            return '1'
        return f'<{self.value}>'
    
    def is_one(self):
        return self.value == 1

class symbol:
    def __init__(self, who, output):
        """
        :param who: Alice ou Bob (A ou B)
        :param output: 0, 1, ...
        """
        self.who = who
        self.output = output
    
    def __repr__(self):
        return f'{self.who}{self.output}'
    
    def __eq__(self, value):
        return self.who == value.who and self.output == value.output
    
    def __ne__(self, value):
        return not (self == value)
    
    def same_who(self, who):
        return self.who == who

class identity:
    def __init__(self):
        self.who = 'I'
    
    def __repr__(self):
        return 'I'

class group:
    def __init__(self, s = None):
        if s == None:
            self.first_b_index = 0
            self.symbols = []
            return
        if isinstance(s, identity):
            self.symbols = [s]
            self.first_b_index = 1
            return
        elif isinstance(s, symbol):
            self.first_b_index = int(s.same_who('A'))
            self.symbols = [s]
            return
        self.symbols = []
        last_who = ''
        start = 0
        self.first_b_index = 0
        for i in range(len(s)):
            c = s[i]
            if c == 'A' or c == 'B':
                if last_who != '':
                    self.symbols.append(symbol(last_who, int(s[start:i])))
                    self.first_b_index += int(self.symbols[-1].same_who('A'))
                if last_who == 'A' and c == 'B':
                    self.first_b_index = len(self.symbols)
                start = i + 1
                last_who = c
        if last_who != '':
            self.symbols.append(symbol(last_who, int(s[start:len(s)])))
            self.first_b_index += int(self.symbols[-1].same_who('A'))
    
    def __repr__(self):
        rst = ''
        for s in self.symbols:
            rst += f'{s}'
        return rst
    
    def __len__(self):
        return len(self.symbols)
    
    def __getitem__(self, i):
        return self.symbols[i]
    
    def __iter__(self):
        return self.symbols.__iter__()
    
    def append(self, s: symbol):
        if s.same_who('A'):
            self.first_b_index += 1
        elif s.same_who('B') and (len(self) == 0 or self.symbols[-1].same_who('A')):
            self.first_b_index = len(self)
        self.symbols.append(s)

    def dagger(self):
        if len(self) <= 1 or (len(self) == 2 and self.first_b_index == 1):
            return self
        As = self.symbols[:self.first_b_index]
        Bs = self.symbols[self.first_b_index:]
        As.reverse()
        Bs.reverse()
        self.symbols = As + Bs
        return self

    def reduce_with(self, other):
        if isinstance(self[0], identity):
            return other
        elif isinstance(other[0], identity):
            return self
        rst = group()
        # Réduire les A
        i1 = self.first_b_index - 1
        i2 = 0
        while i1 >= 0 and i2 < other.first_b_index:
            s1 = self[i1]
            s2 = other[i2]
            if s1 != s2:
                break
            i1 -= 1
            i2 += 1
        rst.symbols = self[:i1 + 1] + other[i2:other.first_b_index]
        rst.first_b_index = len(rst)
        # Réduire les B
        j1 = len(self) - 1
        j2 = other.first_b_index
        while j1 >= self.first_b_index and j2 < len(other):
            s1 = self[j1]
            s2 = other[j2]
            if s1 != s2:
                break
            j1 -= 1
            j2 += 1
        rst.symbols += self[self.first_b_index:j1 + 1] + other[j2:len(other)]
        if len(rst.symbols) == 0:
            return group(identity())
        return rst

    def trace_with_density_op(self):
        return MomentMatrixElement(self)

class MomentMatrix:
    def __init__(self, N, M, d):
        """
        :param N: Nombre d'input pour Alice
        :param M: Nombre d'input pour Bob
        :param d: Degré du NPA (> 0)
        """
        assert(d > 0)

        # Construire les labels pour les lignes et les colonnes
        col_labels = [group(identity())] 
        for i in range(1, d + 1):
            col_labels += generate_combinations(N, M, i)
        row_labels = copy.deepcopy(col_labels)
        row_labels = [l.dagger() for l in row_labels]

        self.mat_width = len(col_labels) + 1
        self.mat_height = len(row_labels) + 1

        # Commencer à remplir la matrice avec les labels
        self.matrix = [None for _ in range((len(row_labels) + 1) * (len(col_labels) + 1))]
        self.matrix[0] = ''
        for i in range(len(col_labels)):
            self.matrix[(i + 1) * self.mat_width] = col_labels[i]
        for i in range(len(row_labels)):
            self.matrix[i + 1] = row_labels[i]

        # Remplir la matrice et les contraintes
        constraints = {}
        for y in range(1, self.mat_height):
            for x in range(y, self.mat_width):
                elt = self.matrix[y * self.mat_width].reduce_with(self.matrix[x]).trace_with_density_op()
                if not elt.is_one():
                    s = elt.__repr__()
                    if s in constraints:
                        constraints[s].append((x, y))
                    else:
                        constraints[s] = [(x, y)]
                self.matrix[y * self.mat_width + x] = elt
        self.constraints = constraints

    def __repr__(self):
        s = ''
        lengts = []
        for x in range(self.mat_width):
            max_len = 0
            for y in range(self.mat_height):
                max_len = max(max_len, len(self.matrix[y * self.mat_width + x].__repr__()))
            lengts.append(max_len)
        for y in range(self.mat_height):
            for x in range(self.mat_width):
                elt = self.matrix[y * self.mat_width + x]
                s += elt.__repr__().ljust(lengts[x]) + '  '
            s += '\n'
        return s

    def get_constraints(self):
        return self.constraints


def generate_combinations(N, M, d):
    # Création des listes de labels
    labels_A = [f"A{i}" for i in range(N)]
    labels_B = [f"B{j}" for j in range(M)]
    all_labels = labels_A + labels_B
    
    results = []

    def backtrack(current_sequence):
        # Condition d'arrêt : on a atteint la profondeur d
        if len(current_sequence) == d:
            results.append("".join(current_sequence))
            return

        for label in all_labels:
            if not current_sequence:
                backtrack([label])
                continue
            
            last = current_sequence[-1]
            
            # RÈGLE 1 : Pas de répétition immédiate
            if label == last:
                continue
            
            # RÈGLE 2 : Commutation (A_i B_j = B_j A_i)
            # Pour éviter les doublons, on interdit la séquence [B_j, A_i]
            # On impose que A vienne toujours AVANT B s'ils sont adjacents.
            if last.startswith('B') and label.startswith('A'):
                continue
                
            backtrack(current_sequence + [label])

    backtrack([])
    return [group(s) for s in results]


    
N, M, d = 2, 2, 2
moment_matrix = MomentMatrix(N, M, d)
print(moment_matrix)
print(moment_matrix.get_constraints())