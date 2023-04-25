import numpy as np
import pandas as pd

def detector_value(prob_storm, model_sense, model_spec, har_payout, nhar_payout_storm, nhar_payout_nstorm):
    p_dns = (model_spec * (1 - prob_storm)) + ((1 - model_sense) * prob_storm)
    p_ns_given_dns = (model_spec * (1 - prob_storm)) / p_dns
    p_s_given_dns = 1 - p_ns_given_dns

    # print(f"p_ns_given_dns {p_ns_given_dns}")
    # print(f"p_s_given_dns {p_s_given_dns}")

    p_ds = 1 - p_dns
    p_s_given_ds = (model_sense * prob_storm) / p_ds
    p_ns_given_ds = 1 - p_s_given_ds

    # print(f"p_s_given_ds {p_s_given_ds}")
    # print(f"p_ns_given_ds {p_ns_given_ds}")

    payout_dns = p_dns * max(har_payout, ((nhar_payout_nstorm * p_ns_given_dns) + (nhar_payout_storm * p_s_given_dns)))
    payout_ds = p_ds * max(har_payout, ((nhar_payout_storm * p_s_given_ds) + (nhar_payout_nstorm * p_ns_given_ds)))

    # print(f"payout_dns: {payout_dns}")
    # print(f"payout_ds: {payout_ds}")

    payout_d = payout_dns + payout_ds
    val_d = payout_d - har_payout

    # print(f"payout_d: {payout_d}")

    return val_d

if __name__ == '__main__':
    dv = detector_value(.5, 0.39, 0.69, 80000.0, 59000.0, 95750.0)
    print(f"The detector value is {dv}")