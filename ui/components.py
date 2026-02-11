import streamlit as st

def kpi_card(title, value):
    st.markdown(f"""
        <div class="kpi-card">
            <div style="text-align:center; font-size:22px; font-weight:bold;">{title}</div>
            <div style="text-align:center; font-size:28px; margin-top:10px;">{value}</div>
        </div>
    """, unsafe_allow_html=True)
