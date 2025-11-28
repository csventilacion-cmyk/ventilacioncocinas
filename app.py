import streamlit as st
import pandas as pd
import math

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="CS Ventilación - Calculadora V5.0",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILOS CSS ---
st.markdown("""
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #0E4F8F; text-align: center; margin-bottom: 0px; }
    .sub-header { font-size: 18px; color: #666; text-align: center; margin-top: 5px; }
    .success-box { padding: 10px; background-color: #d4edda; color: #155724; border-radius: 5px; border: 1px solid #c3e6cb; }
    .warning-box { padding: 10px; background-color: #fff3cd; color: #856404; border-radius: 5px; border: 1px solid #ffeeba; }
    .danger-box { padding: 10px; background-color: #f8d7da; color: #721c24; border-radius: 5px; border: 1px solid #f5c6cb; }
    </style>
""", unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN DE VARIABLES DE SESIÓN ---
if 'equipments' not in st.session_state: st.session_state['equipments'] = []
if 've_counter' not in st.session_state: st.session_state['ve_counter'] = 1
# Variables de cálculo temporal
if 'cfm_actual' not in st.session_state: st.session_state['cfm_actual'] = 0
if 'vel_actual' not in st.session_state: st.session_state['vel_actual'] = 0
if 'pd_actual' not in st.session_state: st.session_state['pd_actual'] = 0
if 'de_actual' not in st.session_state: st.session_state['de_actual'] = 0
if 'current_app_type' not in st.session_state: st.session_state['current_app_type'] = "N/A"

# --- 4. BASE DE DATOS GEOGRÁFICA ---
# Definida bloque por bloque para evitar errores de sintaxis al copiar
db_geo = {}
db_geo["Aguascalientes"] = {"Aguascalientes": {"alt": 1888, "temp": 26}, "Jesus Maria": {"alt": 1890, "temp": 26}, "Calvillo": {"alt": 1640, "temp": 28}}
db_geo["Baja California"] = {"Tijuana": {"alt": 20, "temp": 26}, "Mexicali": {"alt": 8, "temp": 42}, "Ensenada": {"alt": 10, "temp": 24}}
db_geo["Baja California Sur"] = {"La Paz": {"alt": 27, "temp": 30}, "Cabo San Lucas": {"alt": 10, "temp": 29}, "San Jose del Cabo": {"alt": 10, "temp": 29}}
db_geo["Campeche"] = {"Campeche": {"alt": 10, "temp": 34}, "Cd del Carmen": {"alt": 2, "temp": 35}, "Champoton": {"alt": 10, "temp": 34}}
db_geo["Chiapas"] = {"Tuxtla Gutierrez": {"alt": 522, "temp": 32}, "Tapachula": {"alt": 170, "temp": 34}, "San Cristobal": {"alt": 2120, "temp": 20}}
db_geo["Chihuahua"] = {"Chihuahua": {"alt": 1435, "temp": 30}, "Cd Juarez": {"alt": 1120, "temp": 32}, "Delicias": {"alt": 1170, "temp": 31}}
db_geo["Ciudad de Mexico"] = {"CDMX Centro": {"alt": 224
