################################################################################
###                                                                          ###
### Created by Mahdi Manoochertayebi 2025-2026                               ###
###                                                                          ###
################################################################################

import approche_systemique as AS

################################################################################

# Define process rates
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

if __name__ == "__main__":
    model = AS.RecruitmentModel(
        r_s = r_s, 
        r_m = r_m, 
        r_nr = r_nr,  
        r_ref = r_ref,  
        r_ak = r_ak,  
        r_akneg = r_akneg, 
        r_k = r_k,  
        r_kneg = r_kneg, 
        r_r1 = r_r1,  
        r_r2neg = r_r2neg,
        r_r2 = r_r2,
        r_r3neg = r_r3neg,
        r_p = r_p,  
        r_pref = r_pref,  
        r_c = r_c  
    )
    solution = model.run_simulation()
    model.plot_results(solution)