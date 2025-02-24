```python
# RECRUTEMENT REPORTS
f_s = 60  # Sourcing rate
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

# INTER-CONTRAT REPORTS
initial_inter_contrat_consultants = 17
retour_mission_rate = 1/140
resignation_rate = 0.05

# COMMERCE REPORTS
stock_ao_per_week = 13
selection_rate_stock_ao = 10/13
opportunites_per_week = 2.5
opportunites_selection_rate = 0.85
candidats_positionnes_presentation_rate = 0.3
presentation_clients_depart_mission_rate = 0.33

def sibylone_process(self, t, y):
    Sourcing, Messaging, AKLIFE, KLIF, RDV1, RDV2, Proposal, Consultants_Inter_Contrat, Consultants_Mission, Stock_AO, Opportunites, Candidats_Positionnes, Presentation_Clients = y
    
    dSourcing_dt = f_s - r_s * Sourcing - r_m * Sourcing
    dMessaging_dt = r_m * Sourcing - r_nr * Messaging - r_ref * Messaging - r_ak * Messaging
    dAKLIFE_dt = r_ak * Messaging - r_akneg * AKLIFE - r_k * AKLIFE
    dKLIF_dt = r_k * AKLIFE - r_kneg * KLIF - r_r1 * KLIF
    dRDV1_dt = r_r1 * KLIF - r_r2neg * RDV1 - r_r2 * RDV1
    dRDV2_dt = r_r2 * RDV1 - r_r3neg * RDV2 - r_p * RDV2
    dProposal_dt = r_p * RDV2 - r_pref * Proposal - r_c * Proposal
    dConsultants_Inter_Contrat_dt = r_c * Proposal - resignation_rate * Consultants_Inter_Contrat + retour_mission_rate * Consultants_Mission - presentation_clients_depart_mission_rate * Presentation_Clients
    dConsultants_Mission_dt = presentation_clients_depart_mission_rate * Presentation_Clients - retour_mission_rate * Consultants_Mission
    dStock_AO_dt = stock_ao_per_week - selection_rate_stock_ao * Stock_AO
    dOpportunites_dt = selection_rate_stock_ao * Stock_AO + opportunites_per_week - opportunites_selection_rate * Opportunites
    dCandidats_Positionnes_dt = opportunites_selection_rate * Opportunites - candidats_positionnes_presentation_rate * Candidats_Positionnes
    dPresentation_Clients_dt = candidats_positionnes_presentation_rate * Candidats_Positionnes - presentation_clients_depart_mission_rate * Presentation_Clients

```