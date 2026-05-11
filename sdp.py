import numpy as np
import cvxpy as cp
from moment_matrix import MomentMatrix

def build_sdp(moment_matrix: MomentMatrix, correlations: dict):
    """
    Construit et résout le SDP pour la moment matrix

    Le SDP est:
        trouver   Γ  (moment matrix)
        s.t.   Γ[i,i] = 1                        (diagonale = 1)
               Γ[i,j] = Γ[k,l]  pour tout (i,j),(k,l) partageant le même label
               Γ[i,j] = p       si on connait la corrélation p
    
    Parameters
    ----------
    moment_matrix : MomentMatrix
    correlations : dict
        Valeurs connues pour les labels, e.g.:
            {
              '<A0>': 0.0,          # <A_x> proba marginales
              '<B0>': 0.0,          # <B_y> proba marginales
              '<A0B0>': 0.7071,     # corrélations jointes
              ...
            }
        Les labels doivent correspondre parfaitement au résultat de la méthode __repr__ de la classe MomentMatrixElement.
 
    Returns
    -------
    Gamma_val : matrice numpy ou None
        La moment matrice remplie en cas de faisabilité, None sinon
    problem : cp.Problem
        L'objet de type Problem du package CVXPY

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



    
