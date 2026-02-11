import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import os

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

font_path = "NanumGothic.otf"

if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rcParams["font.family"] = font_name

plt.rcParams["axes.unicode_minus"] = False


st.markdown(load_css(), unsafe_allow_html=True)

st.title("💰 AI 대출 상환 전략 분석기 PRO")
st.markdown("전략 점수화 기반 의사결정 지원 시스템")

# ==================================================
# 🔹 사이드바 입력
# ==================================================
st.sidebar.header("📌 대출 정보 입력")

loan_amount = st.sidebar.number_input("대출 원금 (원)", value=10000000, step=1000000)
interest_rate = st.sidebar.number_input("연 이자율 (%)", value=5.0, step=0.1)
loan_term = st.sidebar.number_input("상환 기간 (년)", value=3, step=1)

analyze_btn = st.sidebar.button("🚀 전략 분석 시작")

# ==================================================
# 🔹 레이더 차트 함수
# ==================================================
def plot_radar(score_equal, score_principal):
    categories = ["총비용", "안정성", "초기부담"]

    values_equal = [
        score_equal * 0.5,
        score_equal * 0.3,
        score_equal * 0.2
    ]

    values_principal = [
        score_principal * 0.5,
        score_principal * 0.3,
        score_principal * 0.2
    ]

    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))

    values_equal += values_equal[:1]
    values_principal += values_principal[:1]

    plt.figure()
    plt.polar(angles, values_equal, label="원리금균등")
    plt.polar(angles, values_principal, label="원금균등")
    plt.xticks(angles[:-1], categories)
    plt.legend()
    st.pyplot(plt)


# ==================================================
# 🔹 분석 실행
# ==================================================
if analyze_btn:

    # 계산
    df_equal = calculate_equal_payment(loan_amount, interest_rate, loan_term)
    df_principal = calculate_equal_principal(loan_amount, interest_rate, loan_term)

    total_equal = df_equal["이자"].sum()
    total_principal = df_principal["이자"].sum()

    recommended, score_equal, score_principal = recommend_strategy_advanced(
        df_equal, df_principal
    )

    # ==================================================
    # KPI 카드 영역
    # ==================================================
    st.subheader("📊 핵심 지표 요약")

    col1, col2, col3 = st.columns(3)

    with col1:
        kpi_card("원리금 총 이자", f"{int(total_equal):,} 원")

    with col2:
        kpi_card("원금균등 총 이자", f"{int(total_principal):,} 원")

    with col3:
        kpi_card("AI 추천 전략", f"{recommended}")

    # ==================================================
    # 잔액 비교 차트
    # ==================================================
    st.subheader("📉 잔액 추이 비교")

    plt.figure()
    plt.plot(df_equal["월"], df_equal["잔액"], label="원리금균등")
    plt.plot(df_principal["월"], df_principal["잔액"], label="원금균등")
    plt.xlabel("월")
    plt.ylabel("잔액")
    plt.legend()
    st.pyplot(plt)

    # ==================================================
    # 월 상환액 비교
    # ==================================================
    st.subheader("💸 월 상환액 비교")

    df_equal["월상환액"] = df_equal["원금상환"] + df_equal["이자"]
    df_principal["월상환액"] = df_principal["원금상환"] + df_principal["이자"]

    plt.figure()
    plt.plot(df_equal["월"], df_equal["월상환액"], label="원리금균등")
    plt.plot(df_principal["월"], df_principal["월상환액"], label="원금균등")
    plt.xlabel("월")
    plt.ylabel("월 상환액")
    plt.legend()
    st.pyplot(plt)

    # ==================================================
    # 전략 점수 비교 (레이더)
    # ==================================================
    st.subheader("📈 전략 점수 비교 (AI 다중 기준 평가)")
    plot_radar(score_equal, score_principal)

    # ==================================================
    # AI 전략 설명
    # ==================================================
    st.subheader("🤖 AI 전략 해설")

    if recommended == "원금균등":
        st.success("총 이자 비용 절감 측면에서 원금균등 방식이 우수합니다.")
        st.info("초기 상환 부담은 높지만, 장기적으로 비용 효율이 좋습니다.")
    else:
        st.success("현금 흐름 안정성 측면에서 원리금균등 방식이 우수합니다.")
        st.info("매월 일정한 상환액으로 재무 계획 수립이 용이합니다.")

    # ==================================================
    # 데이터 테이블 보기 (고급 사용자용)
    # ==================================================
    with st.expander("📂 상세 상환 스케줄 보기"):
        st.write("원리금균등 상환 스케줄")
        st.dataframe(df_equal)

        st.write("원금균등 상환 스케줄")
        st.dataframe(df_principal)
