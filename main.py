import copy

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
    
    def same_who(self, who):
        return self.who == who

class identity:
    def __init__(self):
        self.who = 'I'
    
    def __repr__(self):
        return 'I'

class group:
    def __init__(self, s):
        if isinstance(s, identity) or isinstance(s, symbol):
            self.symbols = [s]
            return
        self.symbols = []
        last_who = ''
        start = 0
        for i in range(len(s)):
            c = s[i]
            if c == 'A' or c == 'B':
                if last_who != '':
                    self.symbols.append(symbol(last_who, int(s[start:i])))
                start = i + 1
                last_who = c
        if last_who != '':
            self.symbols.append(symbol(last_who, int(s[start:len(s)])))
    
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
        self.symbols.append(s)

    def dagger(self):
        if len(self) <= 1:
            return self
        A_symb = []
        B_symb = []
        for s in self:
            if s.same_who('A'):
                A_symb.append(s)
            else:
                B_symb.append(s)
        A_symb.reverse()
        B_symb.reverse()
        self.symbols = A_symb + B_symb
        return self

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


def make_moment_matrix(N, M, d):
    """
    :param N: Nombre d'input pour Alice
    :param M: Nombre d'input pour Bob
    :param d: Degré du NPA (défaut = 1)
    :return: La moment matrix et ses contraints
    """
    col_labels = [group(identity())] 
    for i in range(1, d + 1):
        col_labels += generate_combinations(N, M, i)
    row_labels = copy.deepcopy(col_labels)
    row_labels = [l.dagger() for l in row_labels]
    return col_labels, row_labels
    
N, M, d = 2, 2, 2
moment_matrix = make_moment_matrix(N, M, d)
print(moment_matrix)