import numpy as np
from scipy.integrate import solve_ivp

class SibModel:
    def __init__(self):
        self.sourcing_input_flow_rate = 84
        self.messaging_transition_rate = 55
        self.rdv1_transition_rate = 9.8
        self.rdv2_transition_rate = 5.72
        self.rdv3_transition_rate = 3.21
        self.proposition_transition_rate = 1.88
        self.hiring_rate = 1.78
        self.initial_inter_contrat_consultants = 17
        self.initial_mission_consultants = 172
        self.retour_mission_rate = 6.8
        self.resignation_rate = 0.8
        self.opportunities_creation_rate = 33
        self.presentation_clients_transition_rate = 13.5
        self.depart_en_mission_transition_rate = 4.5

    def recruitment_model(self, t, y):
        sourcing_candidates = y[0]
        messaging_candidates = y[1]
        rdv1_candidates = y[2]
        rdv2_candidates = y[3]
        rdv3_candidates = y[4]
        proposition_candidates = y[5]
        inter_contrat_consultants = y[6]
        mission_consultants = y[7]
        opportunities = y[8]
        presentation_clients = y[9]
        depart_en_mission = y[10]

        d_sourcing_candidates_dt = self.sourcing_input_flow_rate - self.messaging_transition_rate
        d_messaging_candidates_dt = self.messaging_transition_rate - self.rdv1_transition_rate
        d_rdv1_candidates_dt = self.rdv1_transition_rate - self.rdv2_transition_rate
        d_rdv2_candidates_dt = self.rdv2_transition_rate - self.rdv3_transition_rate
        d_rdv3_candidates_dt = self.rdv3_transition_rate - self.proposition_transition_rate
        d_proposition_candidates_dt = self.proposition_transition_rate - self.hiring_rate
        d_inter_contrat_consultants_dt = self.hiring_rate + self.retour_mission_rate - self.depart_en_mission_transition_rate - self.resignation_rate
        d_mission_consultants_dt = self.depart_en_mission_transition_rate - self.retour_mission_rate
        d_opportunities_dt = self.opportunities_creation_rate - self.presentation_clients_transition_rate
        d_presentation_clients_dt = self.presentation_clients_transition_rate - self.depart_en_mission_transition_rate
        d_depart_en_mission_dt = self.depart_en_mission_transition_rate

        return [d_sourcing_candidates_dt, d_messaging_candidates_dt, d_rdv1_candidates_dt,
                d_rdv2_candidates_dt, d_rdv3_candidates_dt, d_proposition_candidates_dt,
                d_inter_contrat_consultants_dt, d_mission_consultants_dt, d_opportunities_dt,
                d_presentation_clients_dt, d_depart_en_mission_dt]

    def get_initial_conditions(self):
        return [0, 0, 0, 0, 0, 0, self.initial_inter_contrat_consultants,
                self.initial_mission_consultants, 0, 0, 0]

    def get_state_variable_names(self):
        return ['sourcing_candidates', 'messaging_candidates', 'rdv1_candidates',
                'rdv2_candidates', 'rdv3_candidates', 'proposition_candidates',
                'inter_contrat_consultants', 'mission_consultants', 'opportunities',
                'presentation_clients', 'depart_en_mission']

    def run_simulation(self, t_span, t_eval):
        sol = solve_ivp(self.recruitment_model, t_span, self.get_initial_conditions(), t_eval=t_eval)
        return sol