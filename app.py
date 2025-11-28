import streamlit as st
import pandas as pd
import math

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="CS Ventilación - Calculadora Cocinas",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- ESTILOS VISUALES ---
st.markdown("""
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #0E4F8F; text-align: center; margin-bottom: 0px; }
    .sub-header { font-size: 18px; color: #666; text-align: center; margin-top: 5px; }
    .success-box { padding: 10px; background-color: #d4edda; color: #155724; border-radius: 5px; border: 1px solid #c3e6cb; }
    .warning-box { padding: 10px; background-color: #fff3cd; color: #856404; border-radius: 5px; border: 1px solid #ffeeba; }
    .danger-box { padding: 10px; background-color: #f8d7da; color: #721c24; border-radius: 5px; border: 1px solid #f5c6cb; }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE ESTADO ---
if 'equipments' not in st.session_state: st.session_state['equipments'] = []
if 've_counter' not in st.session_state: st.session_state['ve_counter'] = 1

# --- BASE DE DATOS GEOGRÁFICA (COMPACTA Y CORREGIDA) ---
db_geo = {
    "Aguascalientes": {"Aguascalientes": {"alt": 1888, "temp": 26}, "Jesús María": {"alt": 1890, "temp": 26}, "Calvillo": {"alt": 1640, "temp": 28}},
    "Baja California": {"Tijuana": {"alt": 20, "temp": 26}, "Mexicali": {"alt": 8, "temp": 42}, "Ensenada": {"alt": 10, "temp": 24}},
    "Baja California Sur": {"La Paz": {"alt": 27, "temp": 30}, "Cabo San Lucas": {"alt": 10, "temp": 29}, "San José del Cabo": {"alt": 10, "temp": 29}},
    "Campeche": {"Campeche": {"alt": 10, "temp": 34}, "Ciudad del Carmen": {"alt": 2, "temp": 35}, "Champotón": {"alt": 10, "temp": 34}},
    "Chiapas": {"Tuxtla Gutiérrez": {"alt": 522, "temp": 32}, "Tapachula": {"alt": 170, "temp": 34}, "San Cristóbal": {"alt": 2120, "temp": 20}},
    "Chihuahua": {"Chihuahua": {"alt
