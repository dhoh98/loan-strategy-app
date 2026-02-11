import streamlit as st

def kpi_card(title, value):
    st.markdown(
        f"<div class='kpi-card'>{title}<br>{value}</div>",
        unsafe_allow_html=True
    )
