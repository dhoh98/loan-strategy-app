import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("💰 AI 대출 상환 전략 분석기 (Advanced Version)")

st.header("📌 기본 대출 정보 입력")

loan_amount = st.number_input("대출 원금 (원)", value=10000000)
interest_rate = st.number_input("현재 연 이자율 (%)", value=5.0)
loan_term = st.number_input("상환 기간 (년)", value=3)

st.header("📌 대환대출 비교 (선택)")
refinance_rate = st.number_input("대환 시 연 이자율 (%)", value=0.0)

st.header("📌 조기상환 설정 (선택)")
early_payment_month = st.number_input("조기상환 월 (없으면 0)", value=0)
early_payment_amount = st.number_input("조기상환 금액 (원)", value=0)

def calculate_equal_payment(loan, rate, years):
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

if st.button("📊 전략 분석 시작"):

    df_equal = calculate_equal_payment(loan_amount, interest_rate, loan_term)
    df_principal = calculate_equal_principal(loan_amount, interest_rate, loan_term)

    total_interest_equal = df_equal["이자"].sum()
    total_interest_principal = df_principal["이자"].sum()

    st.subheader("📊 전략 비교 결과")

    st.write(f"원리금균등 총 이자: {int(total_interest_equal):,} 원")
    st.write(f"원금균등 총 이자: {int(total_interest_principal):,} 원")

    diff = total_interest_equal - total_interest_principal

    if diff > 0:
        st.success(f"👉 원금균등이 {int(diff):,} 원 더 유리합니다.")
    else:
        st.success(f"👉 원리금균등이 {int(abs(diff)):,} 원 더 유리합니다.")

    # 그래프
    st.subheader("📉 잔액 비교 그래프")
    plt.figure()
    plt.plot(df_equal["월"], df_equal["잔액"], label="원리금균등")
    plt.plot(df_principal["월"], df_principal["잔액"], label="원금균등")
    plt.legend()
    plt.xlabel("월")
    plt.ylabel("잔액")
    st.pyplot(plt)

    # 대환 비교
    if refinance_rate > 0:
        df_refinance = calculate_equal_payment(loan_amount, refinance_rate, loan_term)
        refinance_interest = df_refinance["이자"].sum()
        saving = total_interest_equal - refinance_interest

        st.subheader("🔄 대환대출 효과")
        st.write(f"대환 시 총 이자: {int(refinance_interest):,} 원")

        if saving > 0:
            st.success(f"👉 대환 시 {int(saving):,} 원 절감 가능합니다.")
        else:
            st.warning("👉 대환 효과가 없습니다.")

    # AI 추천 문구
    st.subheader("🤖 AI 전략 추천")

    if loan_term <= 3:
        st.info("단기 상환이라면 총 이자 절감 효과가 큰 원금균등 방식이 유리합니다.")
    else:
        st.info("현금흐름 안정성을 원한다면 원리금균등 방식이 적합합니다.")
