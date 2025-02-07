import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class RecruitmentModel:
    def __init__(self, f_s, r_s, r_m, r_mr, r_ma, r_hw_r, r_hw_a, r_kl, r_kln, r_r1, r_r1n, r_r2, r_r2n, r_r3, r_r3n, r_p, r_pf, r_c):
        self.f_s = f_s
        self.r_s = r_s
        self.r_m = r_m
        self.r_mr = r_mr
        self.r_ma = r_ma
        self.r_hw_r = r_hw_r
        self.r_hw_a = r_hw_a
        self.r_kl = r_kl
        self.r_kln = r_kln
        self.r_r1 = r_r1
        self.r_r1n = r_r1n
        self.r_r2 = r_r2
        self.r_r2n = r_r2n
        self.r_r3 = r_r3
        self.r_r3n = r_r3n
        self.r_p = r_p
        self.r_pf = r_pf
        self.r_c = r_c

    def recruitment_process(self, y, t):
        S, M, AK, K, R1, R2, P, C = y
        
        dS_dt = self.f_s - self.r_s * S
        dM_dt = (self.r_mr + self.r_hw_r) * S - (self.r_m + self.r_ma + self.r_hw_a) * M
        dAK_dt = (self.r_ma + self.r_hw_a) * M - (self.r_kl + self.r_kln) * AK
        dK_dt = self.r_kl * AK - (self.r_r1 + self.r_r1n) * K
        dR1_dt = self.r_r1 * K - (self.r_r2 + self.r_r2n) * R1
        dR2_dt = self.r_r2 * R1 - (self.r_r3 + self.r_r3n) * R2
        dP_dt = self.r_r3 * R2 - (self.r_p + self.r_pf) * P
        dC_dt = self.r_c * P
        
        return [dS_dt, dM_dt, dAK_dt, dK_dt, dR1_dt, dR2_dt, dP_dt, dC_dt]

    def solve(self, y0, t):
        solution = odeint(self.recruitment_process, y0, t)
        return solution

# Define parameters
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

r_r2 = 1  # RDV2 transformation rate
r_r2n = 0  # RDV2 non-transformation rate

r_r3 = 1  # RDV3 transformation rate
r_r3n = 0  # RDV3 non-transformation rate

r_p = 1  # Proposal acceptance rate
r_pf = 0  # Proposal rejection rate
r_c = 1  # Contract signing rate

# Initial conditions
y0 = [f_s / r_s, 0, 0, 0, 0, 0, 0, 0]

# Time points
t = np.linspace(0, 10, 100)

# Solve the system of differential equations
model = RecruitmentModel(f_s, r_s, r_m, r_mr, r_ma, r_hw_r, r_hw_a, r_kl, r_kln, r_r1, r_r1n, r_r2, r_r2n, r_r3, r_r3n, r_p, r_pf, r_c)
solution = model.solve(y0, t)

# Plot the results
plt.plot(t, solution[:, 0], label='S')
plt.plot(t, solution[:, 1], label='M')
plt.plot(t, solution[:, 2], label='AK')
plt.plot(t, solution[:, 3], label='K')
plt.plot(t, solution[:, 4], label='R1')
plt.plot(t, solution[:, 5], label='R2')
plt.plot(t, solution[:, 6], label='P')
plt.plot(t, solution[:, 7], label='C')
plt.xlabel('Time')
plt.ylabel('Number of candidates')
plt.title('Recruitment process')
plt.legend()
plt.show()