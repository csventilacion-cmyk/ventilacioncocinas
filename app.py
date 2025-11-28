import streamlit as st
import pandas as pd
import math
import urllib.parse # Librería vital para que el correo no falle

# --- 1. CONFIGURACIÓN ---
st.set_page_config(
    page_title="CS Ventilación - Calculadora V7.0",
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

# --- 3. INICIALIZACIÓN ---
if 'equipments' not in st.session_state: st.session_state['equipments'] = []
if 've_counter' not in st.session_state: st.session_state['ve_counter'] = 1
if 'cfm_actual' not in st.session_state: st.session_state['cfm_actual'] = 0
if 'vel_actual' not in st.session_state: st.session_state['vel_actual'] = 0
if 'pd_state' not in st.session_state: st.session_state['pd_state'] = 0
if 'de_state' not in st.session_state: st.session_state['de_state'] = 0
if 'current_app' not in st.session_state: st.session_state['current_app'] = "N/A"

# --- 4. BASE DE DATOS GEOGRÁFICA ---
db_geo = {}
# Bloques individuales para seguridad
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
    d_ideal = math.sqrt(target_area * 4 / math.pi) * 12
    d_final = round(d_ideal / 2) * 2
    if d_final < 4: d_final = 4
    s_ideal = math.sqrt(target_area) * 12
    s_final = round(s_ideal / 2) * 2
    if s_final < 4: s_final = 4
    return int(s_final), int(d_final)

# --- 6. SIDEBAR ---
with st.sidebar:
    try:
        st.image("logo.jpg", use_column_width=True) 
    except:
        st.header("CS VENTILACIÓN")
    
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
            st.session_state['equipments'] = []
            st.session_state['ve_counter'] = 1
            st.rerun()
    else:
        st.caption("Sin equipos.")

# --- 7. UI PRINCIPAL ---
st.markdown('<div class="main-header">CALCULADORA PARA COCINAS COMERCIALES</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">Partida Actual: <strong>VE-{st.session_state["ve_counter"]:02d}</strong></div>', unsafe_allow_html=True)
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["1️⃣ Caudal", "2️⃣ Ductos", "3️⃣ Presión"])

# --- TAB 1 ---
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        L = st.number_input("Largo (m)", 0.5, 10.0, 2.0, 0.1)
        A = st.number_input("Ancho (m)", 0.5, 5.0, 1.0, 0.1)
        H = st.number_input("Distancia (m)", 0.1, 2.0, 1.0, 0.05)
    with c2:
        inst = st.selectbox("Instalación", ["Adosada (3 lados)", "Isla (4 lados)", "Esquina (2 lados)"])
        apps = {
            "Light Duty": 0.25,
            "Medium Duty": 0.35,
            "Heavy Duty": 0.40,
            "Extra Heavy": 0.50
        }
        app = st.selectbox("Aplicación", list(apps.keys()))
        vc = apps[app]
        st.session_state['current_app'] = app

    if "Isla" in inst: P = (2*L) + (2*A)
    elif "Adosada" in inst: P = (2*A) + L
    else: P = A + L
    
    Q = ((P * H) * vc * 3600) / 1.699
    
    st.info(f"Velocidad Captación: **{vc} m/s**")
    cc1, cc2 = st.columns(2)
    with cc1: st.metric("Perímetro", f"{P:.2f} m")
    with cc2: st.metric("Caudal", f"{int(Q)} CFM")
    
    if st.button("✅ Confirmar Caudal"):
        st.session_state['cfm_actual'] = int(Q)
        st.success("Caudal fijado.")

# --- TAB 2 ---
with t2:
    cfm = st.number_input("Caudal (CFM)", value=st.session_state['cfm_actual'])
    
    if cfm > 0:
        ideal_s, ideal_d = get_auto_dims(cfm, 2000)
        cd1, cd2 = st.columns([2,1])
        
        with cd1:
            forma = st.radio("Forma", ["Rectangular", "Circular"], horizontal=True)
            if forma == "Rectangular":
                c1, c2 = st.columns(2)
                with c1: w = st.number_input("Ancho (in)", 4, 100, ideal_s, 2)
                with c2: h = st.number_input("Alto (in)", 4, 100, ideal_s, 2)
                area = (w*h)/144
                de = 1.3 * ((w*h)**0.625) / ((w+h)**0.25)
            else:
                d = st.number_input("Diámetro (in)", 4, 100, ideal_d, 2)
                area = (math.pi*(d/12)**2)/4
                de = d
        
        if area > 0:
            vel = cfm / area
            pd_val = (vel/4005)**2
        else:
            vel, pd_val = 0, 0
            
        with cd2:
            st.metric("Velocidad", f"{int(vel)} FPM")
            st.caption(f"De: {de:.1f}\" | Pd: {pd_val:.3f}")
            
        if vel < 1500: st.markdown('<div class="danger-box">⚠️ BAJA VELOCIDAD (< 1500)</div>', unsafe_allow_html=True)
        elif 1500 <= vel <= 2500: st.markdown('<div class="success-box">✅ VELOCIDAD ÓPTIMA</div>', unsafe_allow_html=True)
        elif 2500 < vel <= 4000: st.markdown('<div class="warning-box">⚠️ ALTA VELOCIDAD (> 2500)</div>', unsafe_allow_html=True)
        else: st.error("⛔ FUERA DE RANGO (> 4000)")
            
        st.session_state['vel_actual'] = vel
        st.session_state['pd_state'] = pd_val
        st.session_state['de_state'] = de
    else:
        st.info("Calcula caudal primero.")

# --- TAB 3 ---
with tab3:
    vel = st.session_state['vel_actual']
    
    if vel > 0 and vel <= 4000:
        pd_ref = st.session_state['pd_state']
        de_ref = st.session_state['de_state']
        
        st.markdown(f"**Pérdidas** (Pd: {pd_ref:.3f})")
        
        if 'losses' not in st.session_state:
            st.session_state['losses'] = []
        
        c_t, c_v, c_b = st.columns([3, 2, 1])
        with c_t:
            items = ["Tramo Recto (m)", "Codo", "Entrada Campana", "Filtro Bafle", "Ampliación", "Reducción", "Otro"]
            comp = st.selectbox("Item", items)
            
            c_ang, c_rad = None, None
            if comp == "Codo":
                c1, c2 = st.columns(2)
                with c1: c_ang = st.selectbox("Grados", ["90", "45", "30"])
                with c2: c_rad = st.selectbox("Radio", ["Largo", "Corto"])

        with c_v:
            if "Tramo" in comp: val = st.number_input("Longitud", 0.0, 500.0, 1.0, 0.5)
            elif "Otro" in comp: val = st.number_input("Pe (in)", 0.0, 5.0, 0.1, 0.1)
            else: val = st.number_input("Cant", 1, 100, 1)
            
        with c_b:
            st.write("")
            st.write("")
            if st.button("➕"):
                loss = 0
                desc = ""
                d_safe = de_ref if de_ref > 0 else 24
                
                if "Tramo" in comp:
                    ft = val * 3.281
                    loss = (0.018 * (ft/(d_safe/12))) * pd_ref
                    desc = f"Tramo {val}m"
                elif comp == "Codo":
                    n = 0.30
                    if c_ang == "90": n = 0.30 if c_rad == "Largo" else 0.50
                    elif c_ang == "45": n = 0.18
                    elif c_ang == "30": n = 0.12
                    loss = n * pd_ref * val
                    desc = f"Codo {c_ang}° ({val})"
                elif "Entrada" in comp:
                    loss = 0.50 * pd_ref * val
                    desc = f"Entrada ({val})"
                elif "Filtro" in comp:
                    loss = 0.50 * val
                    desc = f"Filtro Bafle ({val})"
                elif "Ampliación" in comp:
                    loss = 0.55 * pd_ref * val
                    desc = f"Ampliación ({val})"
                elif "Reducción" in comp:
                    loss = 0.05 * pd_ref * val
                    desc = f"Reducción ({val})"
                elif "Otro" in comp:
                    loss = val
                    desc = "Manual"
                
                st.session_state['losses'].append({"Desc": desc, "Pe": loss})

        if st.session_state['losses']:
            df = pd.DataFrame(st.session_state['losses'])
            st.dataframe(df, use_container_width=True)
            
            total = sum(item['Pe'] for item in st.session_state['losses'])
            st.metric("Caída Presión Total", f"{total:.3f} in wg")
            
            st.markdown("#### Selección")
            pri = st.multiselect("Prioridad (Max 2)", ["Costo", "Ruido", "Energía"], max_selections=2)
            tipo = st.radio("Tipo", ["Hongo", "Ventset", "Tuboaxial"], horizontal=True)
            
            c1, c2 = st.columns(2)
            with c1: v = st.radio("Voltaje", ["1F", "3F"], horizontal=True)
            with c2: u = st.radio("Ubicación", ["Int", "Ext"], horizontal=True)
            
            if st.button("💾 GUARDAR"):
                st.session_state['equipments'].append({
                    "tag": tag_label,
                    "cfm": int(st.session_state['cfm_actual']),
                    "sp": round(total, 3),
                    "volt": v,
                    "ubi": u,
                    "tipo": tipo,
                    "app": st.session_state['current_app'],
                    "pri": ", ".join(pri)
                })
                st.session_state['ve_counter'] += 1
                st.session_state['losses'] = []
                st.success("Guardado.")
        
        # --- SECCIÓN FINAL: CORREO ---
        if st.session_state['equipments']:
            st.markdown("---")
            st.markdown("### 📤 Enviar Proyecto")
            
            # Datos del proyecto
            p = st.session_state['project_data']
            
            # 1. Generar texto limpio para el cuerpo del correo
            # Usamos formato de lista con guiones para simular filas
            list_text = ""
            for e in st.session_state['equipments']:
                list_text += f"🔹 {e['tag']} | {e['cfm']} CFM @ {e['sp']}\" | {e['tipo']} | {e['app']} | {e['volt']}\n"
            
            # 2. Construir el mailto seguro
            subject_raw = f"Cotización: {p['nombre']}"
            body_raw = f"""Hola Ing. Sotelo,

Solicito cotización para el siguiente proyecto:

PROYECTO: {p['nombre']}
UBICACIÓN: {p['ubicacion']} (Alt: {p['alt']}m | Temp: {p['temp']}C)

LISTADO DE EQUIPOS:
--------------------------------------------------
{list_text}
--------------------------------------------------

Quedo atento a sus comentarios."""
            
            # 3. Codificar para URL (Esto evita que falle el botón)
            safe_subject = urllib.parse.quote(subject_raw)
            safe_body = urllib.parse.quote(body_raw)
            
            # 4. Renderizar botón
            mailto_link = f"mailto:ventas@csventilacion.mx?subject={safe_subject}&body={safe_body}"
            
            st.markdown(f"""
            <div style="text-align: center;">
                <a href="{mailto_link}" target="_blank" style="
                    display: inline-block;
                    background-color: #28a745;
                    color: white;
                    padding: 12px 24px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 16px;">
                    📧 GENERAR CORREO DE SOLICITUD
                </a>
                <p style="color: #666; font-size: 12px; margin-top: 5px;">
                    *Al dar clic se abrirá tu aplicación de correo con los datos precargados.
                </p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("Corrige velocidad (Pestaña 2).")
