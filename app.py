import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI 대출 전략 분석기", layout="wide")

# ==============================
# 🔹 스타일 개선 (카드 UI)
# ==============================
st.markdown("""
    <style>
    .kpi-card {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💰 AI 대출 상환 전략 대시보드")

# ==============================
# 🔹 사이드바 입력 패널
# ==============================
st.sidebar.header("📌 대출 정보 입력")

loan_amount = st.sidebar.number_input("대출 원금 (원)", value=10000000)
interest_rate = st.sidebar.number_input("연 이자율 (%)", value=5.0)
loan_term = st.sidebar.number_input("상환 기간 (년)", value=3)

st.sidebar.header("🔄 대환대출 비교")
refinance_rate = st.sidebar.number_input("대환 시 금리 (%)", value=0.0)

st.sidebar.header("⚡ 조기상환 설정")
early_payment_month = st.sidebar.number_input("조기상환 월", value=0)
early_payment_amount = st.sidebar.number_input("조기상환 금액", value=0)

# ==============================
# 🔹 계산 함수
# ==============================
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

# ==============================
# 🔹 분석 버튼
# ==============================
if st.button("📊 전략 분석 시작"):

    df_equal = calculate_equal_payment(loan_amount, interest_rate, loan_term)
    df_principal = calculate_equal_principal(loan_amount, interest_rate, loan_term)

    total_interest_equal = df_equal["이자"].sum()
    total_interest_principal = df_principal["이자"].sum()

    diff = total_interest_equal - total_interest_principal

    # ==============================
    # 🔹 KPI 카드 영역
    # ==============================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div class='kpi-card'>원리금 총 이자<br>{int(total_interest_equal):,} 원</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div class='kpi-card'>원금균등 총 이자<br>{int(total_interest_principal):,} 원</div>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<div class='kpi-card'>전략 차이<br>{int(abs(diff)):,} 원</div>", unsafe_allow_html=True)

    # ==============================
    # 🔹 잔액 비교 그래프
    # ==============================
    st.subheader("📉 잔액 비교")

    plt.figure()
    plt.plot(df_equal["월"], df_equal["잔액"], label="원리금균등")
    plt.plot(df_principal["월"], df_principal["잔액"], label="원금균등")
    plt.legend()
    plt.xlabel("월")
    plt.ylabel("잔액")
    st.pyplot(plt)

    # ==============================
    # 🔹 월 상환액 비교
    # ==============================
    st.subheader("💸 월 상환액 비교")

    df_equal["월상환액"] = df_equal["원금상환"] + df_equal["이자"]
    df_principal["월상환액"] = df_principal["원금상환"] + df_principal["이자"]

    plt.figure()
    plt.plot(df_equal["월"], df_equal["월상환액"], label="원리금균등")
    plt.plot(df_principal["월"], df_principal["월상환액"], label="원금균등")
    plt.legend()
    plt.xlabel("월")
    plt.ylabel("월 상환액")
    st.pyplot(plt)

    # ==============================
    # 🔹 AI 전략 추천 카드
    # ==============================
    st.subheader("🤖 AI 전략 추천")

    if diff > 0:
        st.success("📌 총 이자 기준으로는 원금균등이 유리합니다.")
    else:
        st.info("📌 현금흐름 안정성 측면에서 원리금균등이 적합합니다.")
