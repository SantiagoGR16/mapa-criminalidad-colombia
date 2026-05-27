"""
Mapa de Criminalidad Municipal — Colombia
Dashboard interactivo con Streamlit.
"""

import streamlit as st

st.set_page_config(
    page_title="Mapa de Criminalidad — Colombia",
    page_icon="🗺️",
    layout="wide",
)

st.title("🗺️ Mapa de Criminalidad Municipal — Colombia")
st.markdown("Dashboard interactivo de tasas de criminalidad por municipio.")

# TODO: Implementar dashboard después de tener el pipeline de datos listo
st.info(
    "🚧 Dashboard en construcción. "
    "Ejecuta primero el pipeline de datos (`make pipeline`) para generar los datos procesados."
)
