def recommend_strategy_advanced(df_equal, df_principal):
    """
    AI 전략 추천 로직
    - 총 이자, 초기 부담, 안정성 기준 점수화
    """
    total_equal = df_equal["이자"].sum()
    total_principal = df_principal["이자"].sum()

    # 단순 점수화 예제 (총 이자: 낮을수록 점수 높음)
    score_equal = 100 - total_equal/1000000
    score_principal = 100 - total_principal/1000000

    recommended = "원금균등" if score_principal > score_equal else "원리금균등"

    return recommended, score_equal, score_principal
