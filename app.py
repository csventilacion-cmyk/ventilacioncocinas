import streamlit as st
import pandas as pd
import math

# --- 1. CONFIGURACIÓN ---
st.set_page_config(
    page_title="CS Ventilación - Calculadora Pro",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILOS ---
st.markdown("""
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #0E4F8F; text-align: center; margin-bottom: 0px; }
    .sub-header { font-size: 18px; color: #666; text-align: center; margin-top: 5px; }
    .success-box { padding: 10px; background-color: #d4edda; color: #155724; border-radius: 5px; border: 1px solid #c3e6cb; }
    .warning-box { padding: 10px; background-color: #fff3cd; color: #856404; border-radius: 5px; border: 1px solid #ffeeba; }
    .danger-box { padding: 10px; background-color: #f8d7da; color: #721c24; border-radius: 5px; border: 1px solid #f5c6cb; }
    </style>
""", unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN DE VARIABLES ---
if 'equipments' not in st.session_state: st.session_state['equipments'] = []
if 've_counter' not in st.session_state: st.session_state['ve_counter'] = 1
if 'cfm_actual' not in st.session_state: st.session_state['cfm_actual'] = 0
if 'vel_actual' not in st.session_state: st.session_state['vel_actual'] = 0
if 'pd_state' not in st.session_state: st.session_state['pd_state'] = 0
if 'de_state' not in st.session_state: st.session_state['de_state'] = 0
if 'current_app' not in st.session_state: st.session_state['current_app'] = "N/A"

# --- 4. BASE DE DATOS GEOGRÁFICA (SEGURA) ---
db_geo = {}
db_geo["Aguascalientes"] = {"Aguascalientes": {"alt": 1888, "temp": 26}, "Jesus Maria": {"alt": 1890, "temp": 26}, "Calvillo": {"alt": 1640, "temp": 28}}
db_geo["Baja California"] = {"Tijuana": {"alt": 20, "temp": 26}, "Mexicali": {"alt": 8, "temp": 42}, "Ensenada": {"alt": 10, "temp": 24}}
db_geo["Baja California Sur"] = {"La Paz": {"alt": 27, "temp": 30}, "Cabo San Lucas": {"alt": 10, "temp": 29}, "San Jose del Cabo": {"alt": 10, "temp": 29}}
db_geo["Campeche"] = {"Campeche": {"alt": 10, "temp": 34}, "Cd del Carmen": {"alt": 2, "temp": 35}, "Champoton": {"alt": 10, "temp": 34}}
db_geo["Chiapas"] = {"Tuxtla Gutierrez": {"alt": 522, "temp": 32}, "Tapachula": {"alt": 170, "temp": 34}, "San Cristobal": {"alt": 2120, "temp": 20}}
db_geo["Chihuahua"] = {"Chihuahua": {"alt": 1435, "temp": 30}, "Cd Juarez": {"alt": 1120, "temp": 32}, "Delicias": {"alt": 1170, "temp": 31}}
db_geo["Ciudad de Mexico"] = {"CDMX Centro": {"alt": 2240, "temp": 24}, "Santa Fe": {"alt": 2500, "temp": 21}, "Polanco": {"alt": 2250, "temp": 24}}
db_geo["Coahuila"] = {"Saltillo": {"alt": 1600, "temp": 28}, "Torreon": {"alt": 1120, "temp": 32}, "Monclova": {"alt": 600, "temp": 34}}
db_geo["Colima"] = {"Colima": {"alt": 490, "temp": 32}, "Manzanillo": {"alt": 5, "temp": 32}, "Tecoman": {"alt": 33, "temp": 33}}
db_geo["Durango"] = {"Durango": {"alt": 1890, "temp": 26}, "Gomez Palacio": {"alt": 1130, "temp": 32}, "Lerdo": {"alt": 1140, "temp": 32}}
db_geo["Guanajuato"] = {"Leon": {"alt": 1815, "temp": 29}, "Irapuato": {"alt": 1724, "temp": 30}, "Celaya": {"alt": 1750, "temp": 29}}
db_geo["Guerrero"] = {"Acapulco": {"alt": 10, "temp": 33}, "Chilpancingo": {"alt": 1260, "temp": 28}, "Iguala": {"alt": 730, "temp": 32}}
db_geo["Hidalgo"] = {"Pachuca": {"alt": 2400, "temp": 22}, "Tulancingo": {"alt": 2150, "temp": 21}, "Tula": {"alt": 2060, "temp": 24}}
db_geo["Jalisco"] = {"Guadalajara": {"alt": 1566, "temp": 28}, "Zapopan": {"alt": 1570, "temp": 28}, "Puerto Vallarta": {"alt": 10, "temp": 32}}
db_geo["Estado de Mexico"] = {"Toluca": {"alt": 2660, "temp": 20}, "Ecatepec": {"alt": 2250, "temp": 24}, "Naucalpan": {"alt": 2300, "temp": 23}}
db_geo["Michoacan"] = {"Morelia": {"alt": 1920, "temp": 26}, "Uruapan": {"alt": 1620, "temp": 27}, "Zamora": {"alt": 1560, "temp": 28}}
db_geo["Morelos"] = {"Cuernavaca": {"alt": 1510, "temp": 29}, "Jiutepec": {"alt": 1350, "temp": 30}, "Cuautla": {"alt": 1330, "temp": 31}}
db_geo["Nayarit"] = {"Tepic": {"alt": 920, "temp": 29}, "Xalisco": {"alt": 950, "temp": 29}, "Bahia de Banderas": {"alt": 10, "temp": 32}}
db_geo["Nuevo Leon"] = {"Monterrey": {"alt": 540, "temp": 35}, "San Pedro": {"alt": 600, "temp": 34}, "Apodaca": {"alt": 400, "temp": 36}}
db_geo["Oaxaca"] = {"Oaxaca de Juarez": {"alt": 1550, "temp": 28}, "Tuxtepec": {"alt": 20, "temp": 34}, "Salina Cruz": {"alt": 10, "temp": 35}}
db_geo["Puebla"] = {"Puebla": {"alt": 2135, "temp": 25}, "Cholula": {"alt": 2150, "temp": 25}, "Tehuacan": {"alt": 1600, "temp": 28}}
db_geo["Queretaro"] = {"Queretaro": {"alt": 1820, "temp": 28}, "San Juan del Rio": {"alt": 1920, "temp": 27}, "El Marques": {"alt": 1900, "temp": 28}}
db_geo["Quintana Roo"] = {"Cancun": {"alt": 10, "temp": 32}, "Playa del Carmen": {"alt
