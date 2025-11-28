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

# --- BASE DE DATOS GEOGRÁFICA (SIMPLIFICADA: SOLO NOMBRES) ---
db_geo = {
    "Aguascalientes": ["Aguascalientes", "Jesús María", "Calvillo"],
    "Baja California": ["Tijuana", "Mexicali", "Ensenada"],
    "Baja California Sur": ["La Paz", "Cabo San Lucas", "San José del Cabo"],
    "Campeche": ["Campeche", "Ciudad del Carmen", "Champotón"],
    "Chiapas": ["Tuxtla Gutiérrez", "Tapachula", "San Cristóbal de las Casas"],
    "Chihuahua": ["Ciudad Juárez", "Chihuahua", "Delicias"],
    "Ciudad de México": ["CDMX (Centro)", "Santa Fe", "Polanco"],
    "Coahuila": ["Saltillo", "Torreón", "Monclova"],
    "Colima": ["Colima", "Manzanillo", "Tecomán"],
    "Durango": ["Durango", "Gómez Palacio", "Lerdo"],
    "Guanajuato": ["León", "Irapuato", "Celaya"],
    "Guerrero": ["Acapulco", "Chilpancingo", "Iguala"],
    "Hidalgo": ["Pachuca", "Tulancingo", "Tula"],
    "Jalisco": ["Guadalajara", "Zapopan", "Puerto Vallarta"],
    "Estado de México": ["Toluca", "Ecatepec", "Naucalpan"],
    "Michoacán": ["Morelia", "Uruapan", "Zamora"],
    "Morelos": ["Cuernavaca", "Jiutepec", "Cuautla"],
    "Nayarit": ["Tepic", "Xalisco", "Bahía de Banderas"],
    "Nuevo León": ["Monterrey", "San Pedro Garza García", "Apodaca"],
    "Oaxaca": ["Oaxaca de Juárez", "Tuxtepec", "Salina Cruz"],
    "Puebla": ["Puebla", "Tehuacán", "Cholula"],
    "Querétaro": ["
