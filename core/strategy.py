def recommend_strategy(total_equal, total_principal):
    diff = total_equal - total_principal

    if diff > 0:
        return "원금균등", diff
    else:
        return "원리금균등", abs(diff)
