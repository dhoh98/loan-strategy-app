def recommend_strategy_advanced(df_equal, df_principal):
    """
    AI 전략 추천 로직 (다중 지표 점수화)
    평가 기준:
    - 총 이자 비용 (낮을수록 좋음)
    - 초기 상환 부담 (첫 달 상환액 기준)
    - 현금흐름 안정성 (월 상환액 변동성)
    """

    # =========================
    # 1️⃣ 총 이자
    # =========================
    total_equal = df_equal["이자"].sum()
    total_principal = df_principal["이자"].sum()

    max_interest = max(total_equal, total_principal)

    interest_score_equal = 100 * (1 - total_equal / max_interest)
    interest_score_principal = 100 * (1 - total_principal / max_interest)

    # =========================
    # 2️⃣ 초기 부담 (첫 달 상환액)
    # =========================
    first_equal = df_equal.iloc[0]["원금상환"] + df_equal.iloc[0]["이자"]
    first_principal = df_principal.iloc[0]["원금상환"] + df_principal.iloc[0]["이자"]

    max_first = max(first_equal, first_principal)

    burden_score_equal = 100 * (1 - first_equal / max_first)
    burden_score_principal = 100 * (1 - first_principal / max_first)

    # =========================
    # 3️⃣ 안정성 (월 상환액 변동성)
    # =========================
    df_equal["월상환액"] = df_equal["원금상환"] + df_equal["이자"]
    df_principal["월상환액"] = df_principal["원금상환"] + df_principal["이자"]

    std_equal = df_equal["월상환액"].std()
    std_principal = df_principal["월상환액"].std()

    max_std = max(std_equal, std_principal)

    stability_score_equal = 100 * (1 - std_equal / max_std)
    stability_score_principal = 100 * (1 - std_principal / max_std)

    # =========================
    # 점수 dict 생성 (레이더용)
    # =========================
    score_equal = {
        "이자비용": round(interest_score_equal, 1),
        "초기부담": round(burden_score_equal, 1),
        "안정성": round(stability_score_equal, 1),
    }

    score_principal = {
        "이자비용": round(interest_score_principal, 1),
        "초기부담": round(burden_score_principal, 1),
        "안정성": round(stability_score_principal, 1),
    }

    total_score_equal = sum(score_equal.values())
    total_score_principal = sum(score_principal.values())

    recommended = (
        "원금균등"
        if total_score_principal > total_score_equal
        else "원리금균등"
    )

    return recommended, score_equal, score_principal
