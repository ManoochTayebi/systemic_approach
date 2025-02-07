```python
f_s = 10  # Sourcing rate (candidats sélectionnés)
r_s = 0.1  # Rejection rate at sourcing stage
r_m = 0.8  # No response rate at message stage
r_mr = 0.208  # Response rate at message stage (LinkedIn)
r_ma = 0.097  # Acceptance rate at message stage (LinkedIn)
r_hw_r = 1  # Response rate at message stage (HelloWork) - assuming better than LinkedIn
r_hw_a = 1  # Acceptance rate at message stage (HelloWork) - assuming better than LinkedIn

r_kl = 0.84  # KLIF validation rate
r_kln = 0.16  # KLIF non-validation rate

r_r1 = 0.4  # RDV1 transformation rate
r_r1n = 0.6  # RDV1 non-transformation rate

r_r2 = 1  # RDV2 success rate
r_r2n = 0  # RDV2 failure rate

r_r3 = 0.5  # RDV3 success rate
r_r3n = 0.5  # RDV3 failure rate

r_p = 0.5  # Proposal move rate
r_pf = 0.2  # Proposal rejection rate
r_c = 0.8  # Candidate acceptance rate

def recruitment_process(self, t, y):
    S, M, AK, K, R1, R2, P, C = y
    
    dS_dt = f_s - r_s * S
    dM_dt = r_mr * S + r_hw_r * S - r_m * M - r_ma * M - r_hw_a * M
    dAK_dt = r_ma * M + r_hw_a * M - r_kl * AK - r_kln * AK
    dK_dt = r_kl * AK - r_r1 * K - r_r1n * K
    dR1_dt = r_r1 * K - r_r2 * R1 - r_r2n * R1
    dR2_dt = r_r2 * R1 - r_r3 * R2 - r_r3n * R2
    dP_dt = r_r3 * R2 - r_p * P - r_pf * P
    dC_dt = r_c * P
```