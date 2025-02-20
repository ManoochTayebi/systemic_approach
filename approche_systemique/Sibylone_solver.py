################################################################################
###                                                                          ###
### Created by Mahdi Manoochertayebi 2025-2026                               ###
###                                                                          ###
################################################################################

import numpy as np
from scipy.integrate import solve_ivp
from example_equations_class import RecruitmentModel

class SibyloneSolver(RecruitmentModel):
    def __init__(self, r_s=0.1, r_m=0.9, r_nr=0.8, r_ref=0.1, r_ak=0.1, r_akneg=0.2, r_k=0.8,
                 r_kneg=0.6, r_r1=0.4, r_r2neg=0.5, r_r2=0.3, r_p=0.2, r_pref=0.1, r_c=0.9,
                 f_s=10, depart_rate=0.1, retour_mission_rate=0.2, stock_ao_rate=5,
                 selection_rate=0.4, opportunites_generated_rate=3, candidats_positionnes_rate=0.8,
                 presentation_clients_rate=0.3, depart_en_mission_rate=0.3):
        self.r_s = r_s
        self.r_m = r_m
        self.r_nr = r_nr
        self.r_ref = r_ref
        self.r_ak = r_ak
        self.r_akneg = r_akneg
        self.r_k = r_k
        self.r_kneg = r_kneg
        self.r_r1 = r_r1
        self.r_r2neg = r_r2neg
        self.r_r2 = r_r2
        self.r_p = r_p
        self.r_pref = r_pref
        self.r_c = r_c
        self.f_s = f_s
        self.depart_rate = depart_rate
        self.retour_mission_rate = retour_mission_rate
        self.stock_ao_rate = stock_ao_rate
        self.selection_rate = selection_rate
        self.opportunites_generated_rate = opportunites_generated_rate
        self.candidats_positionnes_rate = candidats_positionnes_rate
        self.presentation_clients_rate = presentation_clients_rate
        self.depart_en_mission_rate = depart_en_mission_rate

    def sibylone_process(self, t, y):
        S, M, AK, K, R1, R2, P, C, INTER_CONTRAT, MISSION, STOCK_AO, OPPORTUNITES, CANDIDATS_POSITIONNES, PRESENTATION_CLIENTS = y

        dS_dt = self.f_s - self.r_s * S - self.r_m * S
        dM_dt = self.r_m * S - self.r_nr * M - self.r_ref * M - self.r_ak * M
        dAK_dt = self.r_ak * M - self.r_akneg * AK - self.r_k * AK
        dK_dt = self.r_k * AK - self.r_kneg * K - self.r_r1 * K
        dR1_dt = self.r_r1 * K - self.r_r2neg * R1 - self.r_r2 * R1
        dR2_dt = self.r_r2 * R1 - self.r_p * R2 - self.r_pref * P
        dP_dt = self.r_p * R2 - self.r_c * P
        dC_dt = self.r_c * P

        dINTER_CONTRAT_dt = self.depart_rate * INTER_CONTRAT + self.retour_mission_rate * MISSION + self.r_c * P
        dMISSION_dt = self.retour_mission_rate * MISSION - self.depart_en_mission_rate * PRESENTATION_CLIENTS

        dSTOCK_AO_dt = self.stock_ao_rate - self.selection_rate * STOCK_AO
        dOPPORTUNITES_dt = self.selection_rate * STOCK_AO + self.opportunites_generated_rate - self.candidats_positionnes_rate * OPPORTUNITES
        dCANDIDATS_POSITIONNES_dt = self.candidats_positionnes_rate * OPPORTUNITES - self.presentation_clients_rate * CANDIDATS_POSITIONNES
        dPRESENTATION_CLIENTS_dt = self.presentation_clients_rate * CANDIDATS_POSITIONNES - self.depart_en_mission_rate * PRESENTATION_CLIENTS

        return [dS_dt, dM_dt, dAK_dt, dK_dt, dR1_dt, dR2_dt, dP_dt, dC_dt,
                dINTER_CONTRAT_dt, dMISSION_dt, dSTOCK_AO_dt, dOPPORTUNITES_dt,
                dCANDIDATS_POSITIONNES_dt, dPRESENTATION_CLIENTS_dt]

    def run_simulation(self, t):
        initial_conditions = [0, 0, 0, 0, 0, 0, 0, 0, 100, 50, 20, 15, 10, 8]
        sol = solve_ivp(self.sibylone_process, (t[0], t[-1]), initial_conditions, t_eval=t)
        return sol.y

# Example usage:
model = SibyloneProcess()
t = np.linspace(0, 100, 500)
sol = model.run_simulation(t)

import matplotlib.pyplot as plt
plt.plot(t, sol[8], label='INTER_CONTRAT')
plt.plot(t, sol[9], label='MISSION')
plt.legend()
plt.show()