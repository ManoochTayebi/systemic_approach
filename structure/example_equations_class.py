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

        # Coefficients
        self.r_s = 0.2      # Non retenu
        self.r_m = 0.9      # Message envoyé
        self.r_nr = 0.8     # Pas de retour
        self.r_ref = 0.1    # Rejeté
        self.r_ak = 0.1     # Réponse acceptée
        self.r_akneg = 0.2  # AKLIF négatif
        self.r_k = 0.8      # KLIF positif
        self.r_kneg = 0.6   # RDV1 rejeté
        self.r_r1 = 0.4     # RDV1 positif
        self.r_r2neg = 0.1  # RDV2 négatif
        self.r_r2 = 0.9     # RDV2 positif
        self.r_r3neg = 0.5  # RDV3 négatif
        self.r_p = 0.5      # Passe en proposition
        self.r_pref = 0.2   # Proposition rejetée
        self.r_c = 0.8      # Accepté

        # Store the variable names
        self.state_variables = ["Sourcé", "Massage", "AKLIF", "KLIF", "RDV1", "RDV2", "Proposal", "Consultant"]

    def sourcing_function(self, t):
        return self.sourcing_rate

    def recruitment_process(self, t, y):
        Source, Massage, AKLIF, KLIF, RDV1, RDV2, Proposal, Consultant = y
        f_s = self.sourcing_function(t)

        dSourcé_dt = f_s - self.r_s * Source - self.r_m * Source
        dMassage_dt = self.r_m * Source - self.r_nr * Massage - self.r_ref * Massage - self.r_ak * Massage
        dAKLIF_dt = self.r_ak * Massage - self.r_akneg * AKLIF - self.r_k * AKLIF
        dKLIF_dt = self.r_k * AKLIF - self.r_kneg * KLIF - self.r_r1 * KLIF
        dRDV1_dt = self.r_r1 * KLIF - self.r_r2neg * RDV1 - self.r_r2 * RDV1
        dRDV2_dt = self.r_r2 * RDV1 - self.r_r3neg * RDV2 - self.r_p * RDV2
        dProposal_dt = self.r_p * RDV2 - self.r_pref * Proposal - self.r_c * Proposal
        dConsultant_dt = self.r_c * Proposal

        return [dSourcé_dt, dMassage_dt, dAKLIF_dt, dKLIF_dt, dRDV1_dt, dRDV2_dt, dProposal_dt, dConsultant_dt]

    def run_simulation(self):
        y0 = [10, 0, 0, 0, 0, 0, 0, 0]
        sol = solve_ivp(self.recruitment_process, self.time_span, y0, t_eval=self.t_eval)
        return sol

    def get_variable_names(self):
        return self.state_variables
