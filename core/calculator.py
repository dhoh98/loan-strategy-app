import pandas as pd

def calculate_equal_payment(loan, rate, years):
    """원리금균등 상환 스케줄 계산"""
    monthly_rate = rate / 100 / 12
    months = years * 12
    monthly_payment = loan * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
    balance = loan
    schedule = []

    for month in range(1, months + 1):
        interest = balance * monthly_rate
        principal = monthly_payment - interest
        balance -= principal
        schedule.append([month, principal, interest, max(balance,0)])

    return pd.DataFrame(schedule, columns=["월", "원금상환", "이자", "잔액"])


def calculate_equal_principal(loan, rate, years):
    """원금균등 상환 스케줄 계산"""
    monthly_rate = rate / 100 / 12
    months = years * 12
    principal_payment = loan / months
    balance = loan
    schedule = []

    for month in range(1, months + 1):
        interest = balance * monthly_rate
        balance -= principal_payment
        schedule.append([month, principal_payment, interest, max(balance,0)])

    return pd.DataFrame(schedule, columns=["월", "원금상환", "이자", "잔액"])
