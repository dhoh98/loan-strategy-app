import numpy as np

def calculate_strategy_score(df, total_interest):
    monthly_payment = df["원금상환"] + df["이자"]

    stability_score = 100 - np.std(monthly_payment)
    cost_score = 1000000000 / total_interest  # 비용 낮을수록 점수 ↑
    early_burden_score = 100 - monthly_payment.iloc[0] / 10000

    total_score = stability_score * 0.3 + cost_score * 0.5 + early_burden_score * 0.2

    return total_score


def recommend_strategy_advanced(df_equal, df_principal):
    total_equal = df_equal["이자"].sum()
    total_principal = df_principal["이자"].sum()

    score_equal = calculate_strategy_score(df_equal, total_equal)
    score_principal = calculate_strategy_score(df_principal, total_principal)

    if score_equal > score_principal:
        return "원리금균등", score_equal, score_principal
    else:
        return "원금균등", score_equal, score_principal
