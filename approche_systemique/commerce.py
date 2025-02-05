
################################################################################
###                                                                          ###
### Created by [Your Name] 2025-2026                                        ###
###                                                                          ###
################################################################################

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

class CommerceModel:
    def __init__(self, 
                 collecting_rate=100, 
                 not_retained_rate=0.2, 
                 business_move_rate=0.9,
                 no_response_rate=0.7, 
                 rejected_rate=0.2, 
                 accepted_rate=0.1,
                 fail_school_rate=0.3,
                 pass_school_rate=0.7,
                 first_chat_rejected_rate=0.5,
                 second_chat_rejected_rate=0.1,
                 third_chat_rejected_rate=0.9,
                 prize_rejected_rate=0.2,
                 time_span=(0, 100), 
                 time_steps=100):
        self.collecting_rate = collecting_rate
        self.time_span = time_span
        self.t_eval = np.linspace(time_span[0], time_span[1], time_steps)
        
        # Define the rates
        self.not_retained_rate = not_retained_rate
        self.business_move_rate = business_move_rate
        self.no_response_rate = no_response_rate
        self.rejected_rate = rejected_rate
        self.accepted_rate = accepted_rate
        self.fail_school_rate = fail_school_rate
        self.pass_school_rate = pass_school_rate
        self.first_chat_rejected_rate = first_chat_rejected_rate
        self.second_chat_rejected_rate = second_chat_rejected_rate
        self.third_chat_rejected_rate = third_chat_rejected_rate
        self.prize_rejected_rate = prize_rejected_rate

    def collecting_process(self, t):
        return self.collecting_rate

    def commerce_process(self, state, t):
        collecting, not_retained, business, no_response, rejected, accepted, school, first_chat, second_chat, third_chat, prize = state
        
        d_collecting_dt = self.collecting_process(t) - (self.not_retained_rate * collecting + self.business_move_rate * collecting)
        d_not_retained_dt = self.not_retained_rate * collecting
        d_business_dt = self.business_move_rate * collecting - (self.no_response_rate * business + self.rejected_rate * business + self.accepted_rate * business)
        d_no_response_dt = self.no_response_rate * business
        d_rejected_dt = self.rejected_rate * business
        d_accepted_dt = self.accepted_rate * business - (self.fail_school_rate * accepted + self.pass_school_rate * accepted)
        d_school_dt = self.pass_school_rate * accepted - (self.first_chat_rejected_rate * school + (1 - self.first_chat_rejected_rate) * school)
        d_first_chat_dt = self.pass_school_rate * accepted * (1 - self.first_chat_rejected_rate) - (self.second_chat_rejected_rate * first_chat + (1 - self.second_chat_rejected_rate) * first_chat)
        d_second_chat_dt = self.pass_school_rate * accepted * (1 - self.first_chat_rejected_rate) * (1 - self.second_chat_rejected_rate) - (self.third_chat_rejected_rate * second_chat + (1 - self.third_chat_rejected_rate) * second_chat)
        d_third_chat_dt = self.pass_school_rate * accepted * (1 - self.first_chat_rejected_rate) * (1 - self.second_chat_rejected_rate) * (1 - self.third_chat_rejected_rate) - (self.prize_rejected_rate * third_chat + (1 - self.prize_rejected_rate) * third_chat)
        d_prize_dt = self.pass_school_rate * accepted * (1 - self.first_chat_rejected_rate) * (1 - self.second_chat_rejected_rate) * (1 - self.third_chat_rejected_rate) * (1 - self.prize_rejected_rate)

        return [d_collecting_dt, d_not_retained_dt, d_business_dt, d_no_response_dt, d_rejected_dt, d_accepted_dt, d_school_dt, d_first_chat_dt, d_second_chat_dt, d_third_chat_dt, d_prize_dt]

    def run_simulation(self):
        initial_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        solution = solve_ivp(self.commerce_process, self.time_span, initial_state, t_eval=self.t_eval)
        return solution

    def plot_results(self, solution):
        plt.figure(figsize=(10,6))
        labels = ["Collecting", "Not Retained", "Business", "No Response", "Rejected", "Accepted", "School", "First Chat", "Second Chat", "Third Chat", "Prize"]
        for i in range(len(solution.y)):
            plt.plot(solution.t, solution.y[i], label=labels[i])
        plt.xlabel("Time")
        plt.ylabel("Number of candidates")
        plt.legend()
        plt.title("Commerce Process Simulation")
        plt.grid()
        plt.show()

if __name__ == "__main__":
    model = CommerceModel()
    solution = model.run_simulation()
    model.plot_results(solution)
