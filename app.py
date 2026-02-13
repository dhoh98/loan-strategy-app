import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import pandas as pd

from core.calculator import calculate_equal_payment, calculate_equal_principal
from core.strategy import recommend_strategy_advanced
from ui.components import kpi_card
from ui.styles import load_css

# ==================================================
# 🔹 기본 설정
# ==================================================
st.set_page_config(
    page_title="AI Loan Strategy PRO",
    layout="wide"
)

# 한글 폰트 적용
font_path = "NanumGothic.otf"
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rcParams["font.family"] = font_name

plt.rcParams["axes.unicode_minus"] = False

# CSS 적용
st.markdown(load_css(), unsafe_allow_html=True)

# 제목
st.markdown("<h1 style='text-align:center;'>💰 AI 대출 상환 전략 분석기 PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>전략 점수화 기반 의사결정 지원 시스템</p>", unsafe_allow_html=True)

# ==================================================
# 🔹 사이드바 입력
# ==================================================
st.sidebar.header("📌 대출 정보 입력")

loan_amount_man = st.sidebar.number_input(
    "대출 원금 (만원)",
    value=1000,
    step=100
)

loan_amount = loan_amount_man * 10000
st.sidebar.markdown(f"💰 실제 대출 원금: **{loan_amount:,.0f} 원**")

interest_rate = st.sidebar.number_input(
    "연 이자율 (%)",
    value=5.0,
    step=0.1
)

loan_term = st.sidebar.number_input(
    "상환 기간 (년)",
    value=3,
    step=1
)

analyze_btn = st.sidebar.button("🚀 전략 분석 시작")

# ==================================================
# 🔹 분석 실행
# ==================================================
if analyze_btn:

    df_equal = calculate_equal_payment(loan_amount, interest_rate, loan_term)
    df_principal = calculate_equal_principal(loan_amount, interest_rate, loan_term)

    total_equal = df_equal["이자"].sum()
    total_principal = df_principal["이자"].sum()

    recommended, score_equal, score_principal = recommend_strategy_advanced(
        df_equal, df_principal
    )

    # =========================
    # KPI 카드
    # =========================
    st.subheader("📊 핵심 지표 요약")
    col1, col2, col3 = st.columns(3)

    with col1:
        kpi_card("원리금 총 이자", f"{int(total_equal):,} 원")
    with col2:
        kpi_card("원금균등 총 이자", f"{int(total_principal):,} 원")
    with col3:
        kpi_card("AI 추천 전략", f"{recommended}")

    # =========================
    # 상환 비교 그래프
    # =========================
    st.subheader("📊 상환 비교 분석")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 📉 잔액 추이 비교")
        fig1, ax1 = plt.subplots(figsize=(6,4))
        ax1.plot(df_equal["월"], df_equal["잔액"], label="원리금균등", linewidth=2)
        ax1.plot(df_principal["월"], df_principal["잔액"], label="원금균등", linewidth=2)
        ax1.set_xlabel("월")
        ax1.set_ylabel("잔액")
        ax1.legend()
        plt.tight_layout()
        st.pyplot(fig1)

    with col_right:
        st.markdown("### 💸 월 상환액 비교")

        df_equal["월상환액"] = df_equal["원금상환"] + df_equal["이자"]
        df_principal["월상환액"] = df_principal["원금상환"] + df_principal["이자"]

        fig2, ax2 = plt.subplots(figsize=(6,4))
        ax2.plot(df_equal["월"], df_equal["월상환액"], label="원리금균등", linewidth=2)
        ax2.plot(df_principal["월"], df_principal["월상환액"], label="원금균등", linewidth=2)
        ax2.set_xlabel("월")
        ax2.set_ylabel("월 상환액")
        ax2.legend()
        plt.tight_layout()
        st.pyplot(fig2)

    # =========================
    # 전략 점수 테이블 (레이더 대신)
    # =========================
    st.subheader("📈 전략 점수 비교")

    score_df = pd.DataFrame({
        "전략": ["원리금균등", "원금균등"],
        "이자비용 점수": [score_equal["이자비용"], score_principal["이자비용"]],
        "초기부담 점수": [score_equal["초기부담"], score_principal["초기부담"]],
        "안정성 점수": [score_equal["안정성"], score_principal["안정성"]],
    })

    score_df["총점"] = score_df[
        ["이자비용 점수", "초기부담 점수", "안정성 점수"]
    ].sum(axis=1)

    st.dataframe(score_df, use_container_width=True)

    # =========================
    # AI 전략 설명
    # =========================
    st.subheader("🤖 AI 전략 해설")

    if recommended == "원금균등":
        st.success("총 이자 비용 절감 측면에서 원금균등 방식이 우수합니다.")
        st.info("초기 상환 부담은 높지만, 장기적으로 비용 효율이 좋습니다.")
    else:
        st.success("현금 흐름 안정성 측면에서 원리금균등 방식이 우수합니다.")
        st.info("매월 일정한 상환액으로 재무 계획 수립이 용이합니다.")

    # =========================
    # 상세 스케줄
    # =========================
    with st.expander("📂 상세 상환 스케줄 보기"):
        st.write("원리금균등 상환 스케줄")
        st.dataframe(df_equal)
        st.write("원금균등 상환 스케줄")
        st.dataframe(df_principal)
