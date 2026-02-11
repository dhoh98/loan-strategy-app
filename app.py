import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("💰 AI 대출 상환 전략 분석기")

st.header("📌 대출 정보 입력")

loan_amount = st.number_input("대출 원금 (원)", value=10000000)
interest_rate = st.number_input("연 이자율 (%)", value=5.0)
loan_term = st.number_input("상환 기간 (년)", value=3)

strategy = st.selectbox(
    "상환 전략 선택",
    ["원리금균등상환", "원금균등상환"]
)

if st.button("📊 계산하기"):

    monthly_rate = interest_rate / 100 / 12
    months = loan_term * 12

    schedule = []

    if strategy == "원리금균등상환":
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
        balance = loan_amount

        for month in range(1, months + 1):
            interest = balance * monthly_rate
            principal = monthly_payment - interest
            balance -= principal
            schedule.append([month, principal, interest, balance])

    else:  # 원금균등상환
        principal_payment = loan_amount / months
        balance = loan_amount

        for month in range(1, months + 1):
            interest = balance * monthly_rate
            payment = principal_payment + interest
            balance -= principal_payment
            schedule.append([month, principal_payment, interest, balance])

    df = pd.DataFrame(schedule, columns=["월", "원금상환", "이자", "잔액"])

    st.subheader("📄 상환 스케줄")
    st.dataframe(df)

    st.subheader("📉 잔액 변화 그래프")
    plt.figure()
    plt.plot(df["월"], df["잔액"])
    plt.xlabel("월")
    plt.ylabel("잔액")
    st.pyplot(plt)

    total_interest = df["이자"].sum()
    st.success(f"총 이자 부담: {int(total_interest):,} 원")
