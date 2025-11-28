import streamlit as st
import pandas as pd
import math

# --- 1. CONFIGURACIÓN ---
st.set_page_config(
    page_title="Calculadora Cocinas V6.0",
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

# --- 3. ESTADO ---
if 'equipments' not in st.session_state: st.session_state['equipments'] = []
if 've_counter' not in st.session_state: st.session_state['ve_counter'] = 1
# Variables temporales para evitar errores de referencia
if 'cfm_actual' not in st.session_state: st.session_state['cfm_actual'] = 0
if 'vel_actual' not in st.session_state: st.session_state['vel_actual'] = 0
if 'pd_val_state' not in st.session_state: st.session_state['pd_val_state'] = 0
if 'de_val_state' not in st.session_state: st.session_state['de_val_state'] = 0
if 'current_app_type' not in st.session_state: st.session_state['current_app_type'] = "N/A"

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
db_geo["Quintana Roo"] = {"Cancun": {"alt": 10, "temp": 32}, "Playa del Carmen": {"alt": 10, "temp": 32}, "Tulum": {"alt": 10, "temp": 32}}
db_geo["San Luis Potosi"] = {"San Luis Potosi": {"alt": 1860, "temp": 26}, "Soledad": {"alt": 1850, "temp": 26}, "Ciudad Valles": {"alt": 70, "temp": 34}}
db_geo["Sinaloa"] = {"Culiacan": {"alt": 54, "temp": 36}, "Mazatlan": {"alt": 10, "temp": 32}, "Los Mochis": {"alt": 10, "temp": 35}}
db_geo["Sonora"] = {"Hermosillo": {"alt": 210, "temp": 40}, "Cd Obregon": {"alt": 40, "temp": 39}, "Nogales": {"alt": 1200, "temp": 30}}
db_geo["Tabasco"] = {"Villahermosa": {"alt": 10, "temp": 35}, "Cardenas": {"alt": 10, "temp": 34}, "Comalcalco": {"alt": 10, "temp": 34}}
db_geo["Tamaulipas"] = {"Reynosa": {"alt": 38, "temp": 34}, "Matamoros": {"alt": 10, "temp": 33}, "Nuevo Laredo": {"alt": 150, "temp": 35}}
db_geo["Tlaxcala"] = {"Tlaxcala": {"alt": 2230, "temp": 24}, "Apizaco": {"alt": 2400, "temp": 23}, "Huamantla": {"alt": 2500, "temp": 22}}
db_geo["Veracruz"] = {"Veracruz": {"alt": 10, "temp": 30}, "Xalapa": {"alt": 1400, "temp": 24}, "Coatzacoalcos": {"alt": 10, "temp": 32}}
db_geo["Yucatan"] = {"Merida": {"alt": 10, "temp": 36}, "Valladolid": {"alt": 20, "temp": 34}, "Progreso": {"alt": 0, "temp": 35}}
db_geo["Zacatecas"] = {"Zacatecas": {"alt": 2440, "temp": 22}, "Guadalupe": {"alt": 2300, "temp": 23}, "Fresnillo": {"alt": 2190, "temp": 24}}

# --- 5. FUNCIONES ---
def get_auto_dims(cfm_target, velocity_target=2000):
    if cfm_target <= 0: return 6, 6
    target_area = cfm_target / velocity_target
    
    # Circular
    diam_ideal = math.sqrt(target_area * 4 / math.pi) * 12
    diam_final = round(diam_ideal / 2) * 2
    if diam_final < 4: diam_final = 4
    
    # Rectangular
    side_ideal = math.sqrt(target_area) * 12
    side_final = round(side_ideal / 2) * 2
    if side_final < 4: side_final = 4
    return int(side_final), int(diam_final)

# --- 6. SIDEBAR ---
with st.sidebar:
    try:
        st.image("logo.jpg", use_column_width=True)
    except:
        st.header("CS VENTILACIÓN")
        st.caption("Nota: Sube 'logo.jpg' a GitHub")
    
    st.markdown("---")
    
    with st.expander("📍 Datos del Proyecto", expanded=True):
        nombre_proyecto = st.text_input("Nombre del Proyecto", placeholder="Ej. Restaurante Centro")
        pais = st.selectbox("País", ["México", "Otro"])
        
        ciudad_selec = ""
        estado_selec = ""
        alt_val = 0
        temp_val = 25
        
        if pais == "México":
            estado_selec = st.selectbox("Estado", sorted(list(db_geo.keys())))
            if estado_selec:
                lista_ciudades = list(db_geo[estado_selec].keys())
                ciudad_selec = st.selectbox("Ciudad", lista_ciudades)
                
                if ciudad_selec:
                    datos = db_geo[estado_selec][ciudad_selec]
                    alt_val = datos['alt']
                    temp_val = datos['temp']
                    
                    c1, c2 = st.columns(2)
                    with c1: st.metric("Altitud", f"{alt_val} m")
                    with c2: st.metric("Temp", f"{temp_val}°C")
        else:
            ciudad_selec = st.text_input("Ciudad / Ubicación", "Ciudad Generica")
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
            st.session_
