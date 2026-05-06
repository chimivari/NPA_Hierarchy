from moment_matrix import MomentMatrix
import cvxpy as cp

def solve_chsh_bounds(d):
    """
    Exemple : Jeu CHSH, degré de NPA = 1

    Inputs :
    Alice choisi l'input x et Bob l'input y
    x, y ∈ {0,1}

    Ouputs :
    Alice a l'output a et Bob l'output b
    a, b ∈ {-1,1}

    Equation :
    CHSH avec normalization : w = (1-/ 4) * <A0B0> + <A0B1> + <A1B0> - <A1B1>
    Borne de Tsirelson : w ≤ 1 / 2 + 1 / (2 √2)  ≈  0.8536

    Objectif :
    Maximiser <A0B0> + <A0B1> + <A1B0> - <A1B1>
    """
    N, M = 2, 2
    mm = MomentMatrix(N, M, d)
    n = mm.mat_width - 1
    Gamma = cp.Variable((n, n), symmetric=True)
    constraints = [Gamma >> 0]

    for i in range(n):
        constraints.append(Gamma[i, i] == 1)

    # Diagonal = 1
    for i in range(n):
        constraints.append(Gamma[i, i] == 1)
 
    # Moment equality constraints
    for label, positions in mm.get_constraints().items():
        ref_x, ref_y = positions[0]
        for (x, y) in positions[1:]:
            constraints.append(
                Gamma[ref_y - 1, ref_x - 1] == Gamma[y - 1, x - 1]
            )
 
    # Helper: get the cvxpy expression for a given moment label
    def moment_expr(label):
        """Return Gamma[i,j] corresponding to a moment label string."""
        for y in range(1, mm.mat_height):
            for x in range(y, mm.mat_width):
                elt = mm.matrix[y * mm.mat_width + x]
                if elt is not None and repr(elt) == label:
                    return Gamma[y - 1, x - 1]
        return None
 
    # Zero marginals
    for lbl in ['<A0>', '<A1>', '<B0>', '<B1>']:
        expr = moment_expr(lbl)
        if expr is not None:
            constraints.append(expr == 0)
 
    # CHSH objective:  maximise  <A0B0> + <A0B1> + <A1B0> - <A1B1>
    chsh_terms = {
        '<A0B0>': +1,
        '<A0B1>': +1,
        '<A1B0>': +1,
        '<A1B1>': -1,
    }
    obj_expr = 0
    for lbl, coeff in chsh_terms.items():
        expr = moment_expr(lbl)
        if expr is not None:
            obj_expr = obj_expr + coeff * expr
 
    problem = cp.Problem(cp.Maximize(obj_expr), constraints)
    problem.solve(solver=cp.SCS, verbose=False)
 
    return problem.value, Gamma.value, mm, problem
