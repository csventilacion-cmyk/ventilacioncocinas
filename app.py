import streamlit as st
import pandas as pd
import math

# ---------------------------------------------------------
# 1. CONFIGURACIÓN Y ESTILOS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Calculadora Cocinas V5.0",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #0E4F8F; text-align: center; margin-bottom: 0px; }
    .sub-header { font-size: 18px; color: #666; text-align: center; margin-top: 5px; }
    .success-box { padding: 10px; background-color: #d4edda; color: #155724; border-radius: 5px; border: 1px solid #c3e6cb; }
    .warning-box { padding: 10px; background-color: #fff3cd; color: #856404; border-radius: 5px; border: 1px solid #ffeeba; }
    .danger-box { padding: 10px; background-color: #f8d7da; color: #721c24; border-radius: 5px; border: 1px solid #f5c6cb; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. FUNCIONES DE CÁLCULO (Movidas al inicio para evitar errores)
# ---------------------------------------------------------
def get_auto_dims(cfm_target, velocity_target=2000):
    if cfm_target <= 0:
        return 6, 6
    
    target_area = cfm_target / velocity_target
    
    # Rectangular
    side_ideal = math.sqrt(target_area) * 12
    side_final = round(side_ideal / 2) * 2
    if side_final < 6:
        side_final = 6
        
    # Circular
    diam_ideal = math.sqrt(target_area * 4 / math.pi) * 12
    diam_final = round(diam_ideal / 2) * 2
    if diam_final < 6:
        diam_final = 6
        
    return int(side_final), int(diam_final)

# ---------------------------------------------------------
# 3. BASE DE DATOS GEOGRÁFICA (Estructura segura)
# ---------------------------------------------------------
db_geo = {}
# Asignamos uno por uno para que no se rompa la linea al copiar
db_geo["Aguascalientes"] = {"Aguascalientes": {"alt": 1888, "temp": 26}, "Jesus Maria": {"alt": 1890, "temp": 26}}
db_geo["Baja California"] = {"Tijuana": {"alt": 20, "temp": 26}, "Mexicali": {"alt": 8, "temp": 42}}
db_geo["CDMX"] = {"Centro": {"alt": 2240, "temp": 24}, "Santa Fe": {"alt": 2500, "temp": 21}}
db_
