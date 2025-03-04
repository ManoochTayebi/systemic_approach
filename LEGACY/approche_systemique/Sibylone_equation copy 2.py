# RECRUTEMENT REPORTS
sourcing_rate = 60  # Sourcing rate
non_retained_rate = 0.1  # Non retenu
message_sent_rate = 0.9  # Message envoyé
no_response_rate = 0.8  # Pas de retour
rejected_rate = 0.1  # Rejeté
response_accepted_rate = 0.1  # Reponse accepté
klif_failed_rate = 0.2  # KLIF negatif
klif_passed_rate = 0.8  # KLIF positif
rdv1_rejected_rate = 0.6  # RDV1 rejected
rdv1_passed_rate = 0.4  # RDV1 positif
rdv2_rejected_rate = 0.1  # RDV2 negatif
rdv2_passed_rate = 0.9  # RDV2 positif
rdv3_rejected_rate = 0.5  # RDV3 negatif
proposal_moved_rate = 0.5  # Moves to Proposal
proposal_rejected_rate = 0.2  # Proposal rejected
proposal_accepted_rate = 0.8  # Accepted

# INTER-CONTRAT REPORTS
initial_inter_contrat_consultants = 17
initial_mission_consultants = 140
mission_return_rate = 1/140
resignation_rate = 0.05

# COMMERCE REPORTS
stock_ao_per_week = 13
selection_rate_stock_ao = 10/13
opportunities_per_week = 2.5
opportunities_selection_rate = 0.85
candidates_positioned_presentation_rate = 0.3
presentation_clients_departure_mission_rate = 0.33

def sibylone_process(t, y):
    sourcing, messaging, aklife, klif, rdv1, rdv2, proposal, consultants_inter_contrat, consultants_mission, stock_ao, opportunities, candidates_positioned, presentation_clients = y
    
    d_sourcing_dt = sourcing_rate - non_retained_rate * sourcing - message_sent_rate * sourcing
    d_messaging_dt = message_sent_rate * sourcing - no_response_rate * messaging - rejected_rate * messaging - response_accepted_rate * messaging
    d_aklife_dt = response_accepted_rate * messaging - klif_failed_rate * aklife - klif_passed_rate * aklife
    d_klif_dt = klif_passed_rate * aklife - rdv1_rejected_rate * klif - rdv1_passed_rate * klif
    d_rdv1_dt = rdv1_passed_rate * klif - rdv2_rejected_rate * rdv1 - rdv2_passed_rate * rdv1
    d_rdv2_dt = rdv2_passed_rate * rdv1 - rdv3_rejected_rate * rdv2 - proposal_moved_rate * rdv2
    d_proposal_dt = proposal_moved_rate * rdv2 - proposal_rejected_rate * proposal - proposal_accepted_rate * proposal
    d_consultants_inter_contrat_dt = proposal_accepted_rate * proposal - resignation_rate * consultants_inter_contrat + mission_return_rate * consultants_mission - presentation_clients_departure_mission_rate * presentation_clients
    d_consultants_mission_dt = presentation_clients_departure_mission_rate * presentation_clients - mission_return_rate * consultants_mission
    d_stock_ao_dt = stock_ao_per_week - selection_rate_stock_ao * stock_ao
    d_opportunities_dt = selection_rate_stock_ao * stock_ao + opportunities_per_week - opportunities_selection_rate * opportunities
    d_candidates_positioned_dt = opportunities_selection_rate * opportunities - candidates_positioned_presentation_rate * candidates_positioned
    d_presentation_clients_dt = candidates_positioned_presentation_rate * candidates_positioned - presentation_clients_departure_mission_rate * presentation_clients
    
    return [d_sourcing_dt, d_messaging_dt, d_aklife_dt, d_klif_dt, d_rdv1_dt, d_rdv2_dt, d_proposal_dt, d_consultants_inter_contrat_dt, d_consultants_mission_dt, d_stock_ao_dt, d_opportunities_dt, d_candidates_positioned_dt, d_presentation_clients_dt]
