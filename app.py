import streamlit as st
import pandas as pd
import math

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="CS Ventilación - Calculadora Cocinas",
    page_icon="🔥",
    layout="centered"
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

# --- BASE DE DATOS GEOGRÁFICA (Actualizada con Altitud/Temp) ---
db_geo = {
    "Sinaloa": {"Culiacán": {"alt": 54, "temp": 36}, "Mazatlán": {"alt": 10, "temp": 32}, "Los Mochis": {"alt": 10, "temp": 35}},
    "Ciudad de México": {"CDMX (Centro)": {"alt": 2240, "temp": 24}, "Santa Fe": {"alt": 2500, "temp": 21}, "Polanco": {"alt": 2250, "temp": 24}},
    "Nuevo León": {"Monterrey": {"alt": 540, "temp": 35}, "San Pedro": {"alt": 600, "temp": 34}, "Apodaca": {"alt": 400, "temp": 36}},
    "Jalisco": {"Guadalajara": {"alt": 1566, "temp": 28}, "Zapopan": {"alt": 1570, "temp": 28}, "Puerto Vallarta": {"alt": 10, "temp": 32}},
    "Sonora": {"Hermosillo": {"alt": 210, "temp": 40}, "Cd. Obregón": {"alt": 40, "temp": 39}, "Nogales": {"alt": 1200, "temp": 30}},
    "Querétaro": {"Querétaro": {"alt": 1820, "temp": 28}, "San Juan del Río": {"alt": 1920, "temp": 27}, "El Marqués": {"alt": 1900, "temp": 28}},
    "Puebla": {"Puebla": {"alt": 2135, "temp": 25}, "Cholula": {"alt": 2150, "temp": 25}, "Tehuacán": {"alt": 1600, "temp": 28}},
    "Yucatán": {"Mérida": {"alt": 10, "temp": 36}, "Valladolid": {"alt": 20, "temp": 34}, "Progreso": {"alt": 0, "temp": 35}},
    "Baja California": {"Tijuana": {"alt": 20, "temp": 26}, "Mexicali": {"alt": 8, "temp": 42}, "Ensenada": {"alt": 10, "temp": 24}},
    "Quintana Roo": {"Cancún": {"alt": 10, "temp": 32}, "Playa del Carmen": {"alt": 10, "temp": 32}, "Tulum": {"alt": 10, "temp": 32}},
    "Guanajuato": {"León": {"alt": 1815, "temp": 29}, "Irapuato": {"alt": 1724, "temp": 30}, "Celaya": {"alt": 1750, "temp": 29}},
    "Veracruz": {"Veracruz": {"alt": 10, "temp": 30}, "Xalapa": {"alt": 1400, "temp": 24}, "Coatzacoalcos": {"alt": 10, "temp": 32}},
    "Aguascalientes": {"Aguascalientes": {"alt": 1888, "temp": 26}, "Jesús María": {"alt": 1890, "temp": 26}, "Calvillo": {"alt": 1640, "temp": 28}},
    "Chihuahua": {"Chihuahua": {"alt": 1435, "temp": 30}, "Cd. Juárez": {"alt": 1120, "temp": 32}, "Delicias": {"alt": 1170, "temp": 31}}
}

# --- FUNCIONES DE CÁLCULO ---
def get_auto_dims(cfm_target, velocity_target=2000):
    if cfm_target <= 0: return 6, 6
    target_area = cfm_target / velocity_target
    diam_ideal = math.sqrt(target_area * 4 / math.pi) * 12
    diam_final = round(diam_ideal / 2) * 2
    if diam_final < 4: diam_final = 4
    side_ideal = math.sqrt(target_area) * 12
    side_final = round(side_ideal / 2) * 2
    if side_final < 4: side_final = 4
    return int(side_final), int(diam_final)

# --- SIDEBAR ---
with st.sidebar:
    try:
        st.image("logo.jpg", use_column_width=True)
    except:
        st.header("CS VENTILACIÓN")
        st.caption("Nota: Sube 'logo.jpg' a GitHub.")
    
    st.markdown("---")
    
    # MOD 1: Menú abierto por default
    with st.expander("📍 Datos del Proyecto", expanded=True):
        nombre_proyecto = st.text_input("Nombre del Proyecto", placeholder="Ej. Restaurante La Plaza")
        pais = st.selectbox("País", ["México", "Otro"])
        
        ciudad_selec = ""
        estado_selec = ""
        alt_val = 0
        temp_val = 25
        
        if pais == "México":
            estado_selec = st.selectbox("Estado", list(db_geo.keys()))
            ciudad_selec = st.selectbox("Ciudad", list(db_geo[estado_selec].keys()))
            
            # MOD 1: Mostrar Altitud y Temperatura
            datos = db_geo[estado_selec][ciudad_selec]
            alt_val = datos['alt']
            temp_val = datos['temp']
            
            c1, c2 = st.columns(2)
            with c1: st.metric("Altitud", f"{alt_val} m")
            with c2: st.metric("Temp", f"{temp_val}°C")
            
        else:
            ciudad_selec = st.text_input("Ciudad / Ubicación")
            alt_val = st.number_input("Altitud (msnm)", 0)
            temp_val = st.number_input("Temperatura (°C)", 25)
        
        st.session_state['project_data'] = {
            "nombre": nombre_proyecto,
            "ubicacion": f"{ciudad_selec}, {estado_selec}" if pais == "México" else ciudad_selec,
            "altitud": alt_val,
            "temp": temp_val
        }
    
    st.markdown("---")
    st.markdown("**Equipos Guardados:**")
    if len(st.session_state['equipments']) > 0:
        for item in st.session_state['equipments']:
            st.caption(f"🔹 {item['tag']} | {item['cfm']} CFM")
        if st.button("🗑️ Borrar Lista"):
            st.session_state['equipments'] = []
            st.session_state['ve_counter'] = 1
            st.rerun()
    else:
        st.caption("Sin equipos.")

# --- TÍTULO PRINCIPAL ---
st.markdown('<div class="main-header">CALCULADORA PARA COCINAS COMERCIALES</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">Partida Actual: <strong>VE-{st.session_state["ve_counter"]:02d}</strong></div>', unsafe_allow_html=True)
st.markdown("---")

# --- TABS DE TRABAJO ---
tab1, tab2, tab3 = st.tabs(["1️⃣ Caudal (Campana)", "2️⃣ Ductos (Velocidad)", "3️⃣ Presión y Cierre"])

# --- TAB 1: CÁLCULO DE CAUDAL ---
with
