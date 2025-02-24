class SibyloneModel:
    def __init__(self):
        self.variable_names = [
            'Sourcing', 'Messaging', 'AKLIFE', 'KLIF', 'RDV1',
            'RDV2', 'Proposal', 'Consultants_Inter_Contrat',
            'Consultants_Mission', 'Stock_AO', 'Opportunites',
            'Candidats_Positionnes', 'Presentation_Clients'
        ]
        
        # RECRUTEMENT REPORTS
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

        # INTER-CONTRAT REPORTS
        self.initial_inter_contrat_consultants = 17
        self.initial_mission_consultants = 140
        self.retour_mission_rate = 1/140
        self.resignation_rate = 0.05

        # COMMERCE REPORTS
        self.stock_ao_per_week = 13
        self.selection_rate_stock_ao = 10/13
        self.opportunites_per_week = 2.5
        self.opportunites_selection_rate = 0.85
        self.candidats_positionnes_presentation_rate = 0.3
        self.presentation_clients_depart_mission_rate = 0.33

    def get_variable_names(self):
        return self.variable_names

    def sibylone_process(self, t, y):
        Sourcing, Messaging, AKLIFE, KLIF, RDV1, RDV2, Proposal, Consultants_Inter_Contrat, Consultants_Mission, Stock_AO, Opportunites, Candidats_Positionnes, Presentation_Clients = y

        dSourcing_dt = self.f_s - self.r_s * Sourcing - self.r_m * Sourcing
        dMessaging_dt = self.r_m * Sourcing - self.r_nr * Messaging - self.r_ref * Messaging - self.r_ak * Messaging
        dAKLIFE_dt = self.r_ak * Messaging - self.r_akneg * AKLIFE - self.r_k * AKLIFE
        dKLIF_dt = self.r_k * AKLIFE - self.r_kneg * KLIF - self.r_r1 * KLIF
        dRDV1_dt = self.r_r1 * KLIF - self.r_r2neg * RDV1 - self.r_r2 * RDV1
        dRDV2_dt = self.r_r2 * RDV1 - self.r_r3neg * RDV2 - self.r_p * RDV2
        dProposal_dt = self.r_p * RDV2 - self.r_pref * Proposal - self.r_c * Proposal
        dConsultants_Inter_Contrat_dt = self.r_c * Proposal - self.resignation_rate * Consultants_Inter_Contrat + self.retour_mission_rate * Consultants_Mission - self.presentation_clients_depart_mission_rate * Presentation_Clients
        dConsultants_Mission_dt = self.presentation_clients_depart_mission_rate * Presentation_Clients - self.retour_mission_rate * Consultants_Mission
        dStock_AO_dt = self.stock_ao_per_week - self.selection_rate_stock_ao * Stock_AO
        dOpportunites_dt = self.opportunites_per_week - self.opportunites_selection_rate * Opportunites
        dCandidats_Positionnes_dt = self.opportunites_selection_rate * Opportunites - self.candidats_positionnes_presentation_rate * Candidats_Positionnes
        dPresentation_Clients_dt = self.candidats_positionnes_presentation_rate * Candidats_Positionnes - self.presentation_clients_depart_mission_rate * Presentation_Clients

        return [
            dSourcing_dt, dMessaging_dt, dAKLIFE_dt, dKLIF_dt,
            dRDV1_dt, dRDV2_dt, dProposal_dt, dConsultants_Inter_Contrat_dt,
            dConsultants_Mission_dt, dStock_AO_dt, dOpportunites_dt,
            dCandidats_Positionnes_dt, dPresentation_Clients_dt
        ]