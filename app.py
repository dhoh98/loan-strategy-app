import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

from core.calculator import calculate_equal_payment, calculate_equal_principal
from ui.components import kpi_card
from ui.styles import load_css

# ==================================================
# 🔹 기본 설정
# ==================================================
st.set_page_config(
    page_title="Loan Repayment Analysis",
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
st.markdown("<h1 style='text-align:center;'>💰 대출 상환 방식 비교 분석기</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>원리금균등 vs 원금균등 비교 대시보드</p>", unsafe_allow_html=True)

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

analyze_btn = st.sidebar.button("📊 분석 시작")

# ==================================================
# 🔹 분석 실행
# ==================================================
if analyze_btn:

    df_equal = calculate_equal_payment(loan_amount, interest_rate, loan_term)
    df_principal = calculate_equal_principal(loan_amount, interest_rate, loan_term)

    total_equal = df_equal["이자"].sum()
    total_principal = df_principal["이자"].sum()

    # =========================
    # KPI 카드
    # =========================
    st.subheader("📊 핵심 지표 비교")

    col1, col2, col3 = st.columns(3)

    with col1:
        kpi_card("원리금균등 총 이자", f"{int(total_equal):,} 원")

    with col2:
        kpi_card("원금균등 총 이자", f"{int(total_principal):,} 원")

    if total_equal < total_principal:
        better = "원리금균등"
    else:
        better = "원금균등"

    with col3:
        kpi_card("이자 기준 유리한 방식", better)

    # =========================
    # 그래프 비교
    # =========================
    st.subheader("📈 상환 흐름 비교")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 📉 잔액 추이 비교")
        fig1, ax1 = plt.subplots(figsize=(6,4))
        ax1.plot(df_equal["월"], df_equal["잔액"], label="원리금균등", linewidth=2)
        ax1.plot(df_principal["월"], df_principal["잔액"], label="원금균등", linewidth=2)
        ax1.set_xlabel("개월")
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
        ax2.set_xlabel("개월")
        ax2.set_ylabel("월 상환액")
        ax2.legend()
        plt.tight_layout()
        st.pyplot(fig2)

    # =========================
    # 결론 안내
    # =========================
    st.subheader("📌 분석 요약")

    if better == "원금균등":
        st.success("원금균등 방식은 총 이자 비용이 더 낮습니다.")
        st.info("초기 상환 부담은 크지만, 장기적으로 비용 절감 효과가 있습니다.")
    else:
        st.success("원리금균등 방식은 총 이자 비용 측면에서 유리합니다.")
        st.info("매월 일정한 금액을 상환하여 자금 계획 수립이 용이합니다.")

    # =========================
    # 상세 스케줄
    # =========================
    with st.expander("📂 상세 상환 스케줄 보기"):

        # 복사본 생성
        df_equal_display = df_equal.copy()
        df_principal_display = df_principal.copy()

        for df in [df_equal_display, df_principal_display]:
            numeric_cols = df.select_dtypes(include=["float", "int"]).columns
            
            # 십의 자리 반올림 후 정수 변환
            df[numeric_cols] = df[numeric_cols].round(-1).astype(int)
            
            # 천 단위 콤마 적용
            for col in numeric_cols:
                df[col] = df[col].apply(lambda x: f"{x:,}")

        st.write("원리금균등 상환 스케줄")
        st.dataframe(df_equal_display, use_container_width=True)

        st.write("원금균등 상환 스케줄")
        st.dataframe(df_principal_display, use_container_width=True)


