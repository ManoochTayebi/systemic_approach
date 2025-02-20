f_s = 60 # Sourcing rate

r_s = 0.1  # Non retenu
r_m = 0.9  # Message envoyé
r_nr = 0.8  # Pas de retour
r_ref = 0.1  # Rejeté
r_ak = 0.1  # Reponse accepté
r_akneg = 0.2  # KLIF negatif
r_k = 0.8  # KLIF positif
r_kneg = 0.6  # RDV1 rejected
r_r1 = 0.4  # RDV1 positif
r_r2neg = 0.1  # RDV2 negatif
r_r2 = 0.9  # RDV2 positif
r_r3neg = 0.5  # RDV3 negatif
r_p = 0.5  # Moves to Proposal
r_pref = 0.2  # Proposal rejected
r_c = 0.8  # Accepted

def recruitment_process(self, t, y):
        S, M, AK, K, R1, R2, P, C = y
        
        dS_dt = f_s - r_s * S - r_m * S
        dM_dt = r_m * S - r_nr * M - r_ref * M - r_ak * M
        dAK_dt = r_ak * M - r_akneg * AK - r_k * AK
        dK_dt = r_k * AK - r_kneg * K - r_r1 * K
        dR1_dt = r_r1 * K - r_r2neg * R1 - r_r2 * R1
        dR2_dt = r_r2 * R1 - r_r3neg * R2 - r_p * R2
        dP_dt = r_p * R2 - r_pref * P - r_c * P
        dC_dt = r_c * P


