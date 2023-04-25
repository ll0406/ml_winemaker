import numpy as np
import pandas as pd
import streamlit as st


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

    return val_d, payout_d

def calculate_nhar_payout_storm(botrytis_prob):
    return (1-botrytis_prob) * 35000 + botrytis_prob * 275000

def calculate_nhar_payout_nstorm(no_prob, typical_prob, high_prob):
    return no_prob * 80000 + typical_prob * 117500 + high_prob * 125000


st.title('Winemaker Dilemma III')

botrytis = st.number_input('Chance of botrytis')
no_sugar = st.number_input('Chance of no sugar increase')
typical_sugar = st.number_input('Chance of typical sugar increase')
high_sugar = st.number_input('Chance of high sugar increase')


# Calculate payout
nhar_payout_nstorm = calculate_nhar_payout_nstorm(no_sugar, typical_sugar, high_sugar)
nhar_payout_storm = calculate_nhar_payout_storm(botrytis)
dv, ev = detector_value(.5, 0.39, 0.69, 80000.0, nhar_payout_storm, nhar_payout_nstorm)

st.write('The E-Value of Not Buying Detector is: $', 80000)
st.write('The E-Value of Buying Detector is: $', ev)

rec = "Buy Detector" if dv > 0 else "Do Not Buy Detector"

st.write('Recommendation: ', rec)


    # session = True
    # while session:
    #     print("Welcome to E-Value Calculator")
    # dv = detector_value(.5, 0.39, 0.69, 80000.0, 59000.0, 95750.0)
    # print(f"The detector value is {dv}")