import streamlit as st
import matplotlib.pyplot as plt

from core.calculator import calculate_equal_payment, calculate_equal_principal
from core.strategy import recommend_strategy
from ui.components import kpi_card
from ui.styles import load_css

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform

# 한글 폰트 설정
if platform.system() == "Windows":
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == "Darwin":  # Mac
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="AI Loan Strategy", layout="wide")

st.markdown(load_css(), unsafe_allow_html=True)

st.title("💰 AI 대출 전략 분석기 PRO")

# =============================
# 사이드바 입력
# =============================
st.sidebar.header("대출 정보 입력")

loan_amount = st.sidebar.number_input("대출 원금", value=10000000)
interest_rate = st.sidebar.number_input("이자율 (%)", value=5.0)
loan_term = st.sidebar.number_input("상환 기간 (년)", value=3)

if st.sidebar.button("전략 분석 시작"):

    df_equal = calculate_equal_payment(loan_amount, interest_rate, loan_term)
    df_principal = calculate_equal_principal(loan_amount, interest_rate, loan_term)

    total_equal = df_equal["이자"].sum()
    total_principal = df_principal["이자"].sum()

    recommended, diff = recommend_strategy(total_equal, total_principal)

    col1, col2, col3 = st.columns(3)

    with col1:
        kpi_card("원리금 총 이자", f"{int(total_equal):,} 원")

    with col2:
        kpi_card("원금균등 총 이자", f"{int(total_principal):,} 원")

    with col3:
        kpi_card("추천 전략", f"{recommended} (+{int(diff):,}원 차이)")

    st.subheader("잔액 비교")

    plt.figure()
    plt.plot(df_equal["월"], df_equal["잔액"], label="원리금균등")
    plt.plot(df_principal["월"], df_principal["잔액"], label="원금균등")
    plt.legend()
    st.pyplot(plt)
