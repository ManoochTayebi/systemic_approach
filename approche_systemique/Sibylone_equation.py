### Sibylone Process Model

#### Variable Definitions

- `f_s`: Sourcing rate
- `r_s`: Non-retention rate from Sourcing
- `r_m`: Messaging rate from Sourcing
- `r_nr`: No response rate from Messaging
- `r_ref`: Rejection rate from Messaging
- `r_ak`: Acceptance rate to AKLIFé from Messaging
- `r_akneg`: Failure rate in AKLIFé
- `r_k`: Success rate in AKLIFé moving to KLIF
- `r_kneg`: Rejection rate in KLIF
- `r_r1`: Positive rate from KLIF to First Interview (RDV1)
- `r_r2neg`: Rejection rate from RDV1
- `r_r2`: Positive rate from RDV1 to Second Interview (RDV2)
- `r_r3neg`: Rejection rate from RDV2
- `r_p`: Proposal rate from RDV2
- `r_pref`: Proposal rejection rate
- `r_c`: Proposal acceptance rate

#### Initial Values and Rates

```python
f_s = 60  # Sourcing rate
r_s = 0.1  # Non-retention rate from Sourcing
r_m = 0.9  # Messaging rate from Sourcing
r_nr = 0.8  # No response rate from Messaging
r_ref = 0.1  # Rejection rate from Messaging
r_ak = 0.1  # Acceptance rate to AKLIFé from Messaging
r_akneg = 0.2  # Failure rate in AKLIFé
r_k = 0.8  # Success rate in AKLIFé moving to KLIF
r_kneg = 0.6  # Rejection rate in KLIF
r_r1 = 0.4  # Positive rate from KLIF to First Interview (RDV1)
r_r2neg = 0.1  # Rejection rate from RDV1
r_r2 = 0.9  # Positive rate from RDV1 to Second Interview (RDV2)
r_r3neg = 0.5  # Rejection rate from RDV2
r_p = 0.5  # Proposal rate from RDV2
r_pref = 0.2  # Proposal rejection rate
r_c = 0.8  # Proposal acceptance rate

# Stock AO (Appele d'Offre) rates
stock_ao_rate = 13  # Appeles d'offre per week
selection_rate = 10 / 13  # Selection rate for Opportunités

# Opportunités rates
opportunities_per_week = 2.5  # Additional opportunities generated per week
opportunity_success_rate = 0.85  # Rate moving to Candidats positionnés

# Candidats positionnés rates
presentation_client_rate = 0.3  # Rate presented to clients

# Presentation clients rates
depart_en_mission_rate = 0.33  # Rate of Départ en mission

# INTER-CONTRAT and MISSION rates
inter_contrat_initial = 17  # Initial number of consultants in INTER-CONTRAT
mission_initial = 3  # Initial number of consultants in MISSION
retention_inter_contrat_rate = 0.05  # Rate of retention in INTER-CONTRAT
```

#### Differential Equations

```python
# Sourcing (S)
dS_dt = f_s - r_s * S - r_m * S

# Messaging (M)
dM_dt = r_m * S - r_nr * M - r_ref * M - r_ak * M

# AKLIFé (A)
dA_dt = r_ak * M - r_akneg * A - r_k * A

# KLIF (K)
dK_dt = r_k * A - r_kneg * K - r_r1 * K

# First Interview (RDV1) (R1)
dR1_dt = r_r1 * K - r_r2neg * R1 - r_r2 * R1

# Second Interview (RDV2) (R2)
dR2_dt = r_r2 * R1 - r_r3neg * R2 - r_p * R2

# Proposal (P)
dP_dt = r_p * R2 - r_pref * P - r_c * P

# INTER-CONTRAT (IC)
dIC_dt = r_c * P - depart_en_mission_rate * IC + retention_inter_contrat_rate * M

# MISSION (MIS)
dMIS_dt = depart_en_mission_rate * IC - retention_inter_contrat_rate * MIS

# Stock AO
dStockAO_dt = stock_ao_rate - selection_rate * stock_ao_rate

# Opportunités
dOpportunities_dt = selection_rate * stock_ao_rate + opportunities_per_week - opportunity_success_rate * opportunities

# Candidats positionnés
dCandidatsPositionnes_dt = opportunity_success_rate * opportunities - presentation_client_rate * candidats_positionnes

# Presentation clients
dPresentationClients_dt = presentation_client_rate * candidats_positionnes - depart_en_mission_rate * presentation_clients
```