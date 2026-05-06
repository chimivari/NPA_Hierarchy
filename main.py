import numpy as np
from moment_matrix import MomentMatrix
from sdp import *
from chsh import solve_chsh_bounds

if __name__ == '__main__':
    # Tester la faisabilité avec des corrélations données
    mm = MomentMatrix(2, 2, 1)
    
    # Corrélations optimales pour le CHSH game (proba marginales = 0)
    c = 1 / np.sqrt(2)
    known_correlations = {
        '<A0>': 0.0, '<A1>': 0.0,
        '<B0>': 0.0, '<B1>': 0.0,
        '<A0B0>': c, '<A0B1>': c,
        '<A1B0>': c, '<A1B1>': -c,
    }
    print('='*60 + '\nFaisabilité du SDP pour les corrélations choisies\n' + '='*60)
    Gamma, problem = build_sdp(mm, known_correlations)
    print(f'statut : {problem.status}')
    if Gamma is not None:
        print_filled_moment_matrix(mm, Gamma)
    
    print('\n' + '='*60 + '\nLimite suppérieure de la CHSH value (devrait approcher 2√2 ≈ 2.8284)\n' + "="*60)
    tsirelson = 2 * np.sqrt(2)
    for d in [1, 2]:
        val, Gamma_chsh, mm_chsh, p = solve_chsh_bounds(d)
        if d == 1:
            print("\nMoment matrix (d=1):")
            print_filled_moment_matrix(mm_chsh, Gamma_chsh)
            print()
        print(f"NPA degree d={d}: CHSH ≤ {val:.6f}  (Tsirelson = {tsirelson:.6f},  statut={p.status})")

    
