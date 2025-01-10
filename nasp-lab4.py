import numpy as np
from typing import Tuple

class SimpleLP:

    def __init__(self, A, b, c):
        c = np.array(c)
        b = np.array(b)
        A = np.array(A)
        m = A.shape[0]
        n = c.shape[0]

        zeroth_row = np.hstack([c, [0]*(m+1)])
        bottom_pack = np.hstack((A, np.identity(m), b.reshape(m, 1)))

        self.tableau = np.vstack((zeroth_row, bottom_pack))
        self.basis = np.arange(n, n+m)  

    def readSolution(self) -> Tuple[np.float32, np.array]:
        
        obj = -self.tableau[0, -1]  
        decisions = np.zeros(self.tableau.shape[1] - 1)
        decisions[self.basis] = self.tableau[1:, -1]  

        return obj, decisions

class NaiveSimplex:

    @staticmethod
    def pivot(lp_problem: SimpleLP, row: int, col: int) -> SimpleLP:
        
        if row == 0:
            raise ValueError("Pivot cannot be in the zeroth row.")

        pivot_value = lp_problem.tableau[row, col]
        lp_problem.tableau[row] /= pivot_value  

        for i in range(lp_problem.tableau.shape[0]):
            if i != row:
                lp_problem.tableau[i] -= lp_problem.tableau[i, col] * lp_problem.tableau[row]

        lp_problem.basis[np.where(lp_problem.basis == lp_problem.basis[row-1])] = col  

        return lp_problem

    @staticmethod
    def solve(lp_problem: SimpleLP) -> SimpleLP:
        
        while True:
            pivot_col = np.argmin(lp_problem.tableau[0, :-1])
            if lp_problem.tableau[0, pivot_col] >= 0:
                break

            ratios = []
            for i in range(1, lp_problem.tableau.shape[0]):
                if lp_problem.tableau[i, pivot_col] > 0:
                    ratios.append(lp_problem.tableau[i, -1] / lp_problem.tableau[i, pivot_col])
                else:
                    ratios.append(np.inf)

            pivot_row = np.argmin(ratios) + 1
            if ratios[pivot_row - 1] == np.inf:
                return None

            NaiveSimplex.pivot(lp_problem, pivot_row, pivot_col)

        return lp_problem
