
import numpy as np
from scipy.integrate import solve_ivp

def monod_rhs(t, y, params):
    # params: dict with mu_max, Ks, Yxs, S_feed, F_in, V
    X, S = y
    mu_max = params.get('mu_max', 0.6)
    Ks = params.get('Ks', 0.5)
    Yxs = params.get('Yxs', 0.5)
    F_in = params.get('F_in', 0.0)
    V = params.get('V', 1.0)
    S_feed = params.get('S_feed', 0.0)
    mu = mu_max * S / (Ks + S) if (Ks + S) > 0 else 0.0
    dXdt = mu * X - (F_in / V) * X
    dSdt = - (1.0 / Yxs) * mu * X + (F_in / V) * (S_feed - S)
    return [dXdt, dSdt]

class Simulator:
    def __init__(self, rhs, params=None):
        self.rhs = rhs
        self.params = params or {}

    def simulate(self, y0, t_span, t_eval=None):
        sol = solve_ivp(self.rhs, t_span, y0, args=(self.params,), t_eval=t_eval, dense_output=True)
        return sol
