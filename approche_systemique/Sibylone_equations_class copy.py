import numpy as np
from scipy.integrate import odeint

class SibyloneModel:
    def __init__(self):
        self.f_s = 60  # Sourcing rate

        self.r_s = 0.1  # Non retenu
        self.r_m = 0.9  # Message envoyé
        self.r_nr = 0.8  # Pas de retour
        self.r_ref = 0.1  # Rejeté
        self.r_ak = 0.1  # Reponse accepté
        self.r_akneg = 0.2  # KLIF negatif
        self.r_k = 0.8  # KLIF positif
        self.r_kneg = 0.6  # RDV1 rejected
        self.r_r1 = 0.4  # RDV1 positif
        self.r_r2neg = 0.1  # RDV2 negatif
        self.r_r2 = 0.9  # RDV2 positif
        self.r_r3neg = 0.5  # RDV3 negatif
        self.r_p = 0.5  # Moves to Proposal
        self.r_pref = 0.2  # Proposal rejected
        self.r_c = 0.8  # Accepted

        # Initial values for recruitment process
        self.S_0 = 0
        self.M_0 = 0
        self.AK_0 = 0
        self.K_0 = 0
        self.R1_0 = 0
        self.R2_0 = 0
        self.P_0 = 0
        self.C_0 = 0

        # Initial values for INTER-CONTRAT department
        self.INTER_CONTRAT_0 = 17
        self.MISSION_0 = 140

        # Rates for INTER-CONTRAT department
        self.retour_mission_rate = 1/140
        self.depart_rate = 0.05

        # Rates for COMMERCE department
        self.stock_ao_rate = 13
        self.selection_rate = 10/13
        self.opportunites_generated_rate = 2.5
        self.candidats_positionnes_rate = 0.85
        self.presentation_clients_rate = 0.3
        self.depart_en_mission_rate = 0.33

    def sibylone_process(self, t, y):
        S, M, AK, K, R1, R2, P, C, INTER_CONTRAT, MISSION, STOCK_AO, OPPORTUNITES, CANDIDATS_POSITIONNES, PRESENTATION_CLIENTS = y

        dS_dt = self.f_s - self.r_s * S - self.r_m * S
        dM_dt = self.r_m * S - self.r_nr * M - self.r_ref * M - self.r_ak * M
        dAK_dt = self.r_ak * M - self.r_akneg * AK - self.r_k * AK
        dK_dt = self.r_k * AK - self.r_kneg * K - self.r_r1 * K
        dR1_dt = self.r_r1 * K - self.r_r2neg * R1 - self.r_r2 * R1
        dR2_dt = self.r_r2 * R1 - self.r_r3neg * R2 - self.r_p * R2
        dP_dt = self.r_p * R2 - self.r_pref * P - self.r_c * P
        dC_dt = self.r_c * P

        dINTER_CONTRAT_dt = self.depart_rate * INTER_CONTRAT - self.retour_mission_rate * MISSION + self.r_c * P
        dMISSION_dt = self.retour_mission_rate * MISSION - self.depart_en_mission_rate * PRESENTATION_CLIENTS + self.depart_en_mission_rate * PRESENTATION_CLIENTS

        dSTOCK_AO_dt = self.stock_ao_rate - self.selection_rate * STOCK_AO
        dOPPORTUNITES_dt = self.selection_rate * STOCK_AO + self.opportunites_generated_rate - self.candidats_positionnes_rate * OPPORTUNITES
        dCANDIDATS_POSITIONNES_dt = self.candidats_positionnes_rate * OPPORTUNITES - self.presentation_clients_rate * CANDIDATS_POSITIONNES
        dPRESENTATION_CLIENTS_dt = self.presentation_clients_rate * CANDIDATS_POSITIONNES - self.depart_en_mission_rate * PRESENTATION_CLIENTS

        return [dS_dt, dM_dt, dAK_dt, dK_dt, dR1_dt, dR2_dt, dP_dt, dC_dt, dINTER_CONTRAT_dt, dMISSION_dt, dSTOCK_AO_dt, dOPPORTUNITES_dt, dCANDIDATS_POSITIONNES_dt, dPRESENTATION_CLIENTS_dt]

    def run_simulation(self, t):
        y0 = [self.S_0, self.M_0, self.AK_0, self.K_0, self.R1_0, self.R2_0, self.P_0, self.C_0, self.INTER_CONTRAT_0, self.MISSION_0, 0, 0, 0, 0]
        solution = odeint(self.sibylone_process, y0, t)
        return solution