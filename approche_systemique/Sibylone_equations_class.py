def get_variable_names():
    return [
        'sourcing', 'messaging', 'aklife', 'klif', 'rdv1', 'rdv2',
        'proposal', 'inter_contrat', 'mission', 'stock_ao',
        'opportunities', 'candidats_positionnes', 'presentation_clients'
    ]

def sibylone_model(state, t, parameters):
    sourcing, messaging, aklife, klif, rdv1, rdv2, proposal, inter_contrat, mission, stock_ao, opportunities, candidats_positionnes, presentation_clients = state

    f_s, r_s, r_m, r_nr, r_ref, r_ak, r_akneg, r_k, r_kneg, r_r1, r_r2, r_r2neg, r_r3neg, r_p, r_pref, r_c, r_inter_contrat_out, r_mission_back, r_resign, f_ao, r_ao_sel, r_opp_gen, r_opp_to_cand, r_cand_pres, r_pres_dep = parameters

    d_sourcing_dt = f_s - r_s * sourcing - r_m * sourcing
    d_messaging_dt = r_m * sourcing - r_nr * messaging - r_ref * messaging - r_ak * messaging
    d_aklife_dt = r_ak * messaging - r_akneg * aklife - r_k * aklife
    d_klif_dt = r_k * aklife - r_kneg * klif - r_r1 * klif
    d_rdv1_dt = r_r1 * klif - r_r2neg * rdv1 - r_r2 * rdv1
    d_rdv2_dt = r_r2 * rdv1 - r_r3neg * rdv2 - r_p * rdv2
    d_proposal_dt = r_p * rdv2 - r_pref * proposal - r_c * proposal
    d_inter_contrat_dt = r_c * proposal - r_inter_contrat_out * inter_contrat + r_mission_back * mission - r_resign * inter_contrat
    d_mission_dt = r_inter_contrat_out * inter_contrat - r_mission_back * mission

    d_stock_ao_dt = f_ao - r_ao_sel * stock_ao
    d_opportunities_dt = r_ao_sel * stock_ao + r_opp_gen - r_opp_to_cand * opportunities
    d_candidats_positionnes_dt = r_opp_to_cand * opportunities - r_cand_pres * candidats_positionnes
    d_presentation_clients_dt = r_cand_pres * candidats_positionnes - r_pres_dep * presentation_clients

    return [d_sourcing_dt, d_messaging_dt, d_aklife_dt, d_klif_dt, d_rdv1_dt, d_rdv2_dt, d_proposal_dt, d_inter_contrat_dt, d_mission_dt, d_stock_ao_dt, d_opportunities_dt, d_candidats_positionnes_dt, d_presentation_clients_dt]

def main():
    variable_names = get_variable_names()
    parameters = [
        10.0,  # f_s
        0.1,   # r_s
        0.2,   # r_m
        0.05,  # r_nr
        0.01,  # r_ref
        0.03,  # r_ak
        0.02,  # r_akneg
        0.04,  # r_k
        0.005, # r_kneg
        0.06,  # r_r1
        0.07,  # r_r2
        0.008, # r_r2neg
        0.009, # r_r3neg
        0.08,  # r_p
        0.01,  # r_pref
        0.09,  # r_c
        0.1,   # r_inter_contrat_out
        0.11,  # r_mission_back
        0.012, # r_resign
        15.0,  # f_ao
        0.13,  # r_ao_sel
        20.0,  # r_opp_gen
        0.14,  # r_opp_to_cand
        0.15,  # r_cand_pres
        0.016, # r_pres_dep
    ]
    state = [1.0] * len(variable_names)
    t = 0

    derivatives = sibylone_model(state, t, parameters)
    print(derivatives)

if __name__ == "__main__":
    main()