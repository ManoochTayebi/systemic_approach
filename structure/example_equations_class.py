################################################################################
###                                                                          ###
### Created by Mahdi Manoochertayebi 2025-2026                               ###
###                                                                          ###
################################################################################

import numpy as np
from scipy.integrate import solve_ivp


class RecruitmentModel:
    def __init__(self, sourcing_rate=60, time_span=(0, 53), time_steps=100):
        self.sourcing_rate = sourcing_rate
        self.time_span = time_span
        self.t_eval = np.linspace(time_span[0], time_span[1], time_steps)
        

        self.r_s = 0.2      # Non retenu
        self.r_m = 0.9     # Message envoyé
        self.r_nr = 0.8    # Pas de retour
        self.r_ref = 0.1  # Rejeté
        self.r_ak = 0.1    # Réponse acceptée
        self.r_akneg = 0.2  # AKLIF négatif
        self.r_k = 0.8      # KLIF positif
        self.r_kneg = 0.6  # RDV1 rejeté
        self.r_r1 = 0.4    # RDV1 positif
        self.r_r2neg = 0.1  # RDV2 négatif
        self.r_r2 = 0.9    # RDV2 positif
        self.r_r3neg = 0.5  # RDV3 négatif
        self.r_p = 0.5      # Passe en proposition
        self.r_pref = 0.2  # Proposition rejetée
        self.r_c = 0.8      # Accepté

    def sourcing_function(self, t):
        return self.sourcing_rate

    def recruitment_process(self, t, y):
        S, M, AK, K, R1, R2, P, C = y
        f_s = self.sourcing_function(t)
        
        dS_dt = f_s - self.r_s * S - self.r_m * S
        dM_dt = self.r_m * S - self.r_nr * M - self.r_ref * M - self.r_ak * M
        dAK_dt = self.r_ak * M - self.r_akneg * AK - self.r_k * AK
        dK_dt = self.r_k * AK - self.r_kneg * K - self.r_r1 * K
        dR1_dt = self.r_r1 * K - self.r_r2neg * R1 - self.r_r2 * R1
        dR2_dt = self.r_r2 * R1 - self.r_r3neg * R2 - self.r_p * R2
        dP_dt = self.r_p * R2 - self.r_pref * P - self.r_c * P
        dC_dt = self.r_c * P
        
        return [dS_dt, dM_dt, dAK_dt, dK_dt, dR1_dt, dR2_dt, dP_dt, dC_dt]
    
    def run_simulation(self):
        y0 = [10, 0, 0, 0, 0, 0, 0, 0]
        sol = solve_ivp(self.recruitment_process, self.time_span, y0, t_eval=self.t_eval)
        return sol