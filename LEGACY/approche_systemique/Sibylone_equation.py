```python
# Import necessary libraries
import numpy as np
from scipy.integrate import odeint

# Define model parameters and state variables
sourcing_rate = 84
messaging_transition_rate = 55
rdv1_transition_rate = 9.8
rdv2_transition_rate = 5.72
rdv3_transition_rate = 3.21
proposition_transition_rate = 1.88
hiring_rate = 1.78
opportunities_creation_rate = 33
presentation_clients_transition_rate = 13.5
depart_en_mission_transition_rate = 4.5
retour_mission_rate = 6.8
resignation_rate = 0.8

# Define the model
def sibylone_model(state, time):
    candidates_sourced, candidates_in_messaging, candidates_in_rdv1, candidates_in_rdv2, candidates_in_rdv3, candidates_in_proposition, consultants_in_inter_contrat, consultants_in_mission, opportunities, presentation_clients, depart_en_mission = state
    
    d_candidates_sourced_dt = sourcing_rate - messaging_transition_rate
    d_candidates_in_messaging_dt = messaging_transition_rate - rdv1_transition_rate
    d_candidates_in_rdv1_dt = rdv1_transition_rate - rdv2_transition_rate
    d_candidates_in_rdv2_dt = rdv2_transition_rate - rdv3_transition_rate
    d_candidates_in_rdv3_dt = rdv3_transition_rate - proposition_transition_rate
    d_candidates_in_proposition_dt = proposition_transition_rate - hiring_rate
    d_consultants_in_inter_contrat_dt = hiring_rate + retour_mission_rate - depart_en_mission_transition_rate - resignation_rate
    d_consultants_in_mission_dt = depart_en_mission_transition_rate - retour_mission_rate
    d_opportunities_dt = opportunities_creation_rate - presentation_clients_transition_rate
    d_presentation_clients_dt = presentation_clients_transition_rate - depart_en_mission_transition_rate
    d_depart_en_mission_dt = depart_en_mission_transition_rate
    
    return [d_candidates_sourced_dt, d_candidates_in_messaging_dt, d_candidates_in_rdv1_dt, d_candidates_in_rdv2_dt, d_candidates_in_rdv3_dt, d_candidates_in_proposition_dt, d_consultants_in_inter_contrat_dt, d_consultants_in_mission_dt, d_opportunities_dt, d_presentation_clients_dt, d_depart_en_mission_dt]

# Initial conditions
initial_conditions = [
    0,  # candidates_sourced
    0,  # candidates_in_messaging
    0,  # candidates_in_rdv1
    0,  # candidates_in_rdv2
    0,  # candidates_in_rdv3
    0,  # candidates_in_proposition
    17,  # consultants_in_inter_contrat
    172,  # consultants_in_mission
    0,  # opportunities
    0,  # presentation_clients
    0  # depart_en_mission
]

# Time points
time = np.linspace(0, 100)

# Solve ODE
state = odeint(sibylone_model, initial_conditions, time)
```