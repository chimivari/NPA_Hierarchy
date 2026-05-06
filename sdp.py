import numpy as np
import cvxpy as cp
from moment_matrix import MomentMatrix

def build_sdp(moment_matrix: MomentMatrix, correlations: dict):
    """
    Construit et résout le SDP pour la moment matrix

    Le SDP est:
        trouver   Γ  (moment matrix, real symmetric PSD)
        s.t.   Γ[i,i] = 1                        (diagonal from identity products)
               Γ[i,j] = Γ[k,l]  for all (i,j),(k,l) sharing the same moment label
               Γ[i,j] = p       if the label matches a known correlation value p
    
    Parameters
    ----------
    moment_matrix : MomentMatrix
        The symbolic moment matrix produced by your existing code.
    correlations : dict
        Known numerical values for moment labels, e.g.:
            {
              '<A0>': 0.0,          # <A_x> marginals
              '<B0>': 0.0,          # <B_y> marginals
              '<A0B0>': 0.7071,     # joint correlations
              ...
            }
        Labels must match the __repr__ of MomentMatrixElement exactly.
 
    Returns
    -------
    Gamma_val : np.ndarray or None
        The filled moment matrix if the SDP is feasible, None otherwise.
    problem : cp.Problem
        The cvxpy problem object (inspect .status, .value, etc.)

    """
    # Largeur de la moment_matrix
    n = moment_matrix.mat_width - 1

    Gamma = cp.Variable((n, n), symmetric=True)
    constraints = [Gamma >> 0]      # Matrice semie définie
    
    # Diagonale == 1
    for i in range(n):
        constraints.append(Gamma[i, i] == 1)
    
    # Toutes les positions ayant le même label doivent avoir la même valeur
    for label, positions in moment_matrix.get_constraints().items():
        ref_x, ref_y = positions[0]
        for x, y in positions[1:]:
            constraints.append(Gamma[ref_y - 1, ref_x - 1] == Gamma[y - 1, x - 1])
    
    # Ajouter les corrélations connues
    for label, value in correlations.items():
        # Si la corrélation est partagée entre plusieurs entrées de la matrice
        if label in moment_matrix.get_constraints():
            ref_x, ref_y = moment_matrix.get_constraints()[label][0]
            constraints.append(Gamma[ref_y - 1, ref_x - 1] == value)
        # Si la valeur de la corrélation ne correspond qu'à une seule entrée de la matrice
        else:
            for y in range(1, moment_matrix.mat_height):
                for x in range(y, moment_matrix.mat_width):
                    elt = moment_matrix.matrix[y * moment_matrix.mat_width + x]
                    if elt is not None and repr(elt) == label:
                        constraints.append(Gamma[y - 1, x - 1] == value)
    
    # Résolution
    objective = cp.Minimize(0)
    problem = cp.Problem(objective, constraints)
    problem.solve(solver=cp.SCS, verbose=False)

    if problem.status in ("optimal", "optimal_inaccurate"):
        return Gamma.value, problem
    else:
        return None, problem

def print_filled_moment_matrix(moment_matrix: MomentMatrix, Gamma: np.ndarray):
    n = moment_matrix.mat_width - 1
    # Récupérer les labels des lignes et colonnes
    col_labels = [moment_matrix.matrix[x] for x in range(1, moment_matrix.mat_width)]
    row_labels = [moment_matrix.matrix[y * moment_matrix.mat_width] for y in range(1, moment_matrix.mat_height)]
    
    label_w = max(len(repr(l)) for l in row_labels) + 2
    cell_w = 8

    # Header row
    header = ' ' * label_w
    for cl in col_labels:
        header += repr(cl).center(cell_w)
    print(header)
    print('─' * len(header))
 
    for i in range(n):
        row_str = repr(row_labels[i]).ljust(label_w)
        for j in range(n):
            if j >= i:
                val = Gamma[i, j]
            else:
                val = Gamma[j, i]   # symmetric
            row_str += f'{val:+.4f}'.center(cell_w)
        print(row_str)



    
