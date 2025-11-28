import streamlit as st
import pandas as pd
import math

# ---------------------------------------------------------
# 1. CONFIGURACIÓN Y ESTILOS
# ---------------------------------------------------------
st.set_page_config(
    page_title="Calculadora Cocinas V8.0",
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
# 2. ESTADO DE LA APLICACIÓN
# ---------------------------------------------------------
if 'equipments' not in st.session_state: st.session_state['equipments'] = []
if 've_counter' not in st.session_state: st.session_state['ve_counter'] = 1

# Variables temporales de cálculo
if 'cfm_actual' not in st.session_state: st.session_state['cfm_actual'] = 0
if 'vel_actual' not in st.session_state: st.session_state['vel_actual'] = 0
if 'pd_state' not in st.session_state: st.session_state['pd_state'] = 0
if 'de_state' not in st.session_state: st.session_state['de_state'] = 0
if 'current_app' not in st.session_state: st.session_state['current_app'] = "N/A"

# ---------------------------------------------------------
# 3. BASE DE DATOS GEOGRÁFICA (FORMATO SEGURO)
# ---------------------------------------------------------
db_geo = {}

db_geo["Aguascalientes"] = {
    "Aguascalientes": {"alt": 1888, "temp": 26},
    "Jesus Maria": {"alt": 1890, "temp": 26},
    "Calvillo": {"alt": 1640, "temp": 28}
}

db_geo["Baja California"] = {
    "Tijuana": {"alt": 20, "temp": 26},
    "Mexicali": {"alt": 8, "temp": 42},
    "Ensenada": {"alt": 10, "temp": 24}
}

db_geo["Baja California Sur"] = {
    "La Paz": {"alt": 27, "temp": 30},
    "Cabo San Lucas": {"alt": 10, "temp": 29},
    "San Jose del Cabo": {"alt": 10, "temp": 29}
}

db_geo["Campeche"] = {
    "Campeche": {"alt": 10, "temp": 34},
    "Cd del Carmen": {"alt": 2, "temp": 35},
    "Champoton": {"alt": 10, "temp": 34}
}

db_geo["Chiapas"] = {
    "Tuxtla Gutierrez": {"alt": 522, "temp": 32},
    "Tapachula": {"alt": 170, "temp": 34},
    "San Cristobal": {"alt": 2120, "temp": 20}
}

db_geo["Chihuahua"] = {
    "Chihuahua": {"alt": 1435, "temp": 30},
    "Cd Juarez": {"alt": 1120, "temp": 32},
    "Delicias": {"alt": 1170, "temp": 31}
}

db_geo["Ciudad de Mexico"] = {
    "CDMX Centro": {"alt": 2240, "temp": 24},
    "Santa Fe": {"alt": 2500, "temp": 21},
    "Polanco": {"alt": 2250, "temp": 24}
}

db_geo["Coahuila"] = {
    "Saltillo": {"alt": 1600, "temp": 28},
    "Torreon": {"alt": 1120, "temp": 32},
    "Monclova": {"alt": 600, "temp": 34}
}

db_geo["Colima"] = {
    "Colima": {"alt": 490, "temp": 32},
    "Manzanillo": {"alt": 5, "temp": 32},
    "Tecoman": {"alt": 33, "temp": 33}
}

db_geo["Durango"] = {
    "Durango": {"alt": 1890, "temp": 26},
    "Gomez Palacio": {"alt": 1130, "temp": 32},
    "Lerdo": {"alt": 1140, "temp": 32}
}

db_geo["Guanajuato"] = {
    "Leon": {"alt": 1815, "temp": 29},
    "Irapuato": {"alt": 1724, "temp": 30},
    "Celaya": {"alt": 1750, "temp": 29}
}

db_geo["Guerrero"] = {
    "Acapulco": {"alt": 10, "temp": 33},
    "Chilpancingo": {"alt": 1260, "temp": 28},
    "Iguala": {"alt": 730, "temp": 32}
}

db_geo["Hidalgo"] = {
    "Pachuca": {"alt": 2400, "temp": 22},
    "Tulancingo": {"alt": 2150, "temp": 21},
    "Tula": {"alt": 2060, "temp": 24}
}

db_geo["Jalisco"] = {
    "Guadalajara": {"alt": 1566, "temp": 28},
    "Zapopan": {"alt": 1570, "temp": 28},
    "Puerto Vallarta": {"alt": 10, "temp": 32}
}

db_geo["Estado de Mexico"] = {
    "Toluca": {"alt": 2660, "temp": 20},
    "Ecatepec": {"alt": 2250, "temp": 24},
    "Naucalpan": {"alt": 2300, "temp": 23}
}

db_geo["Michoacan"] = {
    "Morelia": {"alt": 1920, "temp": 26},
    "Uruapan": {"alt": 1620, "temp": 27},
    "Zamora": {"alt": 1560, "temp": 28}
}

db_geo["Morelos"] = {
    "Cuernavaca": {"alt": 1510, "temp": 29},
    "Jiutepec": {"alt": 1350, "temp": 30},
    "Cuautla": {"alt": 1330, "temp": 31}
}

db_geo["Nayarit"] = {
    "Tepic": {"alt": 920, "temp": 29},
    "Xalisco": {"alt": 950, "temp": 29},
    "Bahia de Banderas": {"alt": 10, "temp": 32}
}

db_geo["Nuevo Leon"] = {
    "Monterrey": {"alt": 540, "temp": 35},
    "San Pedro": {"alt": 600, "temp": 34},
    "Apodaca": {"alt": 400, "temp": 36}
}

db_geo["Oaxaca"] = {
    "Oaxaca de Juarez": {"alt": 1550, "temp": 28},
    "Tuxtepec": {"alt": 20, "temp": 34},
    "Salina Cruz": {"alt": 10, "temp": 35}
}

db_geo["Puebla"] = {
    "Puebla": {"alt": 2135, "temp": 25},
    "Cholula": {"alt": 2150, "temp": 25},
    "Tehuacan": {"alt": 1600, "temp": 28}
}

db_geo["Queretaro"] = {
    "Queretaro": {"alt": 1820, "temp": 28},
    "San Juan del Rio": {"alt": 1920, "temp": 27},
    "El Marques": {"alt": 1900, "temp": 28}
}

db_geo["Quintana Roo"] = {
    "Cancun": {"alt": 10, "temp": 32},
    "Playa del Carmen": {"alt": 10, "temp": 32},
    "Tulum": {"alt": 10, "temp": 32}
}

db_geo["San Luis Potosi"] = {
    "San Luis Potosi": {"alt": 1860, "temp": 26},
    "Soledad": {"alt": 1850, "temp": 26},
    "Ciudad Valles": {"alt": 70, "temp": 34}
}

db_geo["Sinaloa"] = {
    "Culiacan": {"alt": 54, "temp": 36},
    "Mazatlan": {"alt": 10, "temp": 32},
    "Los Mochis": {"alt": 10, "temp": 35}
}

db_geo["Sonora"] = {
    "Hermosillo": {"alt": 210, "temp": 40},
    "Cd Obregon": {"alt": 40, "temp": 39},
    "Nogales": {"alt": 1200, "temp": 30}
}

db_geo["Tabasco"] = {
    "Villahermosa": {"alt": 10, "temp": 35},
    "Cardenas": {"alt": 10, "temp": 34},
    "Comalcalco": {"alt": 10, "temp": 34}
}

db_geo["Tamaulipas"] = {
    "Reynosa": {"alt": 38, "temp": 34},
    "Matamoros": {"alt": 10, "temp": 33},
    "Nuevo Laredo": {"alt": 150, "temp": 35}
}

db_geo["Tlaxcala"] = {
    "Tlaxcala": {"alt": 2230, "temp": 24},
    "Apizaco": {"alt": 2400, "temp": 23},
    "Huamantla": {"alt": 2500, "temp": 22}
}

db_geo["Veracruz"] = {
    "Veracruz": {"alt": 10, "temp": 30},
    "Xalapa": {"alt": 1400, "temp": 24},
    "Coatzacoalcos": {"alt": 10, "temp": 32}
}

db_geo["Yucatan"] = {
    "Merida": {"alt": 10, "temp": 36},
    "Valladolid": {"alt": 20, "temp": 34},
    "Progreso": {"alt": 0, "temp": 35}
}

db_geo["Zacatecas"] = {
    "Zacatecas": {"alt": 2440, "temp": 22},
    "Guadalupe": {"alt": 2300, "temp": 23},
    "Fresnillo": {"alt": 2190, "temp": 24}
}

# ---------------------------------------------------------
# 5. FUNCIONES AUXILIARES
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# 6. BARRA LATERAL
# ---------------------------------------------------------
with st.sidebar:
    try:
        st.image("logo.jpg", use_column_width=True) 
    except:
        st.header("CS VENTILACIÓN")
        st.caption("Nota: Sube 'logo.jpg' a GitHub.")
    
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
                ciudad_selec = st.selectbox("Ciudad", list(db_geo[estado_selec].keys()))
                
                if ciudad_selec:
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

# ---------------------------------------------------------
# 7. INTERFAZ PRINCIPAL
# ---------------------------------------------------------
st.markdown('<div class="main-header">CALCULADORA PARA COCINAS COMERCIALES</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">Partida Actual: <strong>VE-{st.session_state["ve_counter"]:02d}</strong></div>', unsafe_allow_html=True)
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["1️⃣ Caudal (Campana)", "2️⃣ Ductos (Velocidad)", "3️⃣ Presión y Cierre"])

# --- TAB 1: CAUDAL ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Dimensiones Campana (Metros)**")
        largo = st.number_input("Largo (m)", min_value=0.5, value=2.0, step=0.1)
        ancho = st.number_input("Ancho (m)", min_value=0.5, value=1.0, step=0.1)
        distancia = st.number_input("Distancia de Captación (m)", min_value=0.1, value=1.0, step=0.05)
        
    with col2:
        st.markdown("**Condiciones**")
        instalacion = st.selectbox("Instalación", ["Adosada a una pared (3 lados)", "Isla (4 lados)", "Esquina (2 lados)"])
        apps = {
            "Light Duty (Hornos, Vapor)": 0.25,
            "Medium Duty (Estufas, Planchas)": 0.35,
            "Heavy Duty (Parrillas, Carbón)": 0.40,
            "Extra Heavy Duty (Wok, Leña)": 0.50
        }
        app_key = st.selectbox("Aplicación", list(apps.keys()))
        vc_val = apps[app_key]
        st.session_state['current_app'] = app_key
    
    if "Isla" in instalacion: P = (2*largo) + (2*ancho)
    elif "Adosada" in instalacion: P = (2*ancho) + largo
    else: P = ancho + largo
    
    area_paso = P * distancia
    caudal_m3s = area_paso * vc_val
    caudal_m3hr = caudal_m3s * 3600
    caudal_cfm = caudal_m3hr / 1.699
    
    st.markdown("---")
    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1: st.metric("Velocidad Captación", f"{vc_val} m/s")
    with res_col2: st.metric("Perímetro Libre", f"{P:.2f} m")
    with res_col3:
        st.markdown(f"""
        <div style="background-color: #0E4F8F; color: white; padding: 10px; border-radius: 5px; text-align: center;">
            <small>Caudal Requerido</small><br>
            <strong style="font-size: 24px;">{int(caudal_cfm)} CFM</strong>
        </div>
        """, unsafe_allow_html=True)
        
    if st.button("✅ Confirmar Caudal"):
        st.session_state['cfm_actual'] = int(caudal_cfm)
        st.success("Caudal fijado.")

# --- TAB 2: DUCTOS ---
with tab2:
    cfm_val = st.number_input("Caudal (CFM)", value=st.session_state.get('cfm_actual', 0))
    
    if cfm_val > 0:
        ideal_side, ideal_diam = get_auto_dims(cfm_val, 2000)
        c_dim, c_res = st.columns([2,1])
        
        with c_dim:
            forma = st.radio("Forma", ["Rectangular", "Circular"], horizontal=True)
            if forma == "Rectangular":
                c1, c2 = st.columns(2)
                with c1: w = st.number_input("Ancho (in)", 4, 100, int(ideal_side), step=2)
                with c2: h = st.number_input("Alto (in)", 4, 100, int(ideal_side), step=2)
                area_ft2 = (w*h)/144
                de = 1.3 * ((w*h)**0.625) / ((w+h)**0.25)
            else:
                d = st.number_input("Diámetro (in)", 4, 100, int(ideal_diam), step=2)
                area_ft2 = (math.pi*(d/12)**2)/4
                de = d
        
        if area_ft2 > 0:
            vel = cfm_val / area_ft2 
            presion_dinamica = (vel/4005)**2 # Nombre seguro
        else:
            vel, presion_dinamica = 0, 0
            
        with c_res:
            st.metric("Velocidad", f"{int(vel)} FPM")
            st.caption(f"De: {de:.1f}\" | Pd: {presion_dinamica:.3f} in")
            
        # --- SEMÁFOROS DE VELOCIDAD ---
        if vel < 1500:
            st.markdown('<div class="danger-box">⚠️ <strong>VELOCIDAD BAJA (< 1500 FPM)</strong><br>Riesgo de acumulación de grasa.</div>', unsafe_allow_html=True)
        elif 1500 <= vel <= 2500:
            st.markdown('<div class="success-box">✅ <strong>VELOCIDAD IDEAL (1500-2500 FPM)</strong><br>Rango óptimo.</div>', unsafe_allow_html=True)
        elif 2500 < vel <= 4000:
            st.markdown('<div class="warning-box">⚠️ <strong>ALTA VELOCIDAD (> 2500 FPM)</strong><br>Nivel de ruido y presión excesiva.</div>', unsafe_allow_html=True)
        else:
            st.error("⛔ <strong>FUERA DE RANGO (> 4000 FPM)</strong><br>Velocidad no admisible.", icon="🚫")
            
        st.session_state['vel_actual'] = vel
        st.session_state['pd_state'] = presion_dinamica
        st.session_state['de_state'] = de
    else:
        st.info("Define el caudal en la Pestaña 1.")

# --- TAB 3: PRESIÓN Y CIERRE ---
with tab3:
    # Bloqueo si velocidad > 4000
    if st.session_state.get('vel_actual', 0) > 0 and st.session_state.get('vel_actual', 0) <= 4000:
        pd_ref = st.session_state['pd_state']
        de_ref = st.session_state['de_state']
        
        st.markdown(f"**Cálculo de Pérdidas** (Pd Ref: {pd_ref:.3f} in wg)")
        if 'lista_perdidas' not in st.session_state: st.session_state['lista_perdidas'] = []
        
        c_type, c_val, c_btn = st.columns([3, 2, 1])
        with c_type:
            comp = st.selectbox("Accesorio", 
                ["Tramos Rectos (Metros)", "Codo", "Dispositivo de Captación", 
                 "Filtro Inercial de Grasa Tipo Bafle", "Ampliación", "Reducción", "Otras Pérdidas"])
            
            codo_ang, codo_rad = None, None
            if comp == "Codo":
                c1, c2 = st.columns(2)
                with c1: codo_ang = st.selectbox("Ángulo", ["90°", "45°", "30°"])
                with c2: codo_rad = st.selectbox("Radio", ["Largo", "Corto"])

        with c_val:
            if "Tramos" in comp: val = st.number_input("Longitud (m)", 0.0, 500.0, 1.0, step=0.5)
            elif "Otras" in comp: val = st.number_input("Presión (in wg)", 0.0, 5.0, 0.1, step=0.1)
            else: val = st.number_input("Cantidad", 1, 100, 1)
            
        with c_btn:
            st.write("")
            st.write("")
            if st.button("➕ Agregar"):
                loss = 0
                desc = ""
                d_safe = de_ref if de_ref > 0 else 24
                
                if "Tramos" in comp:
                    feet = val * 3.281
                    loss = (0.018 * (feet/(d_safe/12))) * pd_ref
                    desc = f"Tramo Recto ({val}m)"
                elif comp == "Codo":
                    n = 0.30
                    if codo_ang == "90°": n = 0.30 if codo_rad == "Largo" else 0.50
                    elif codo_ang == "45°": n = 0.18
                    elif codo_ang == "30°": n = 0.12
                    loss = n * pd_ref * val
                    desc = f"Codo {codo_ang}° {codo_rad} ({val} pzas)"
                elif "Captación" in comp:
                    loss = 0.50 * pd_ref * val
                    desc = f"Entrada Campana ({val} pzas)"
                elif "Filtro" in comp:
                    loss = 0.50 * val
                    desc = f"Filtro Inercial ({val} pzas)"
                elif "Ampliación" in comp:
                    loss = 0.55 * pd_ref * val
                    desc = f"Ampliación ({val} pzas)"
                elif "Reducción" in comp:
                    loss = 0.05 * pd_ref * val
                    desc = f"Reducción ({val} pzas)"
                elif "Otras" in comp:
                    loss = val
                    desc = "Pérdida Manual"
                
                st.session_state['lista_perdidas'].append({"Concepto": desc, "Pe (in wg)": loss})

        if st.session_state['lista_perdidas']:
            df = pd.DataFrame(st.session_state['lista_perdidas'])
            st.dataframe(df, use_container_width=True)
            
            total_sp = sum(item['Pe (in wg)'] for item in st.session_state['lista_perdidas'])
            st.metric("Presión Estática Total", f"{total_sp:.3f} in wg")
            
            st.markdown("#### Selección de Equipo")
            
            # Prioridades (Max 2)
            prioridades = st.multiselect("Prioridades (Máx 2)", 
                                         ["Costo Inicial", "Nivel Sonoro", "Consumo Energético"], 
                                         max_selections=2)
            
            # Tipo Ventilador
            tipo_vent = st.radio("Características Ventilador", 
                                 ["Tipo Hongo (Tejado)", "Tipo Ventset", "Tuboaxial"], 
                                 horizontal=True)
            
            c1, c2 = st.columns(2)
            with c1: volt = st.radio("Voltaje", ["Monofásico", "Trifásico"], horizontal=True)
            with c2: ubi = st.radio("Ubicación", ["Interior", "Exterior"], horizontal=True)
            
            if st.button("💾 GUARDAR PARTIDA"):
                tag = f"VE-{st.session_state['ve_counter']:02d}"
                st.session_state['equipments'].append({
                    "tag": tag,
                    "cfm": int(st.session_state['cfm_actual']),
                    "sp": round(total_sp, 3),
                    "voltaje": volt,
                    "ubicacion": ubi,
                    "tipo_vent": tipo_vent,
                    "app_type": st.session_state.get('current_app', 'N/A'),
                    "prioridades": ", ".join(prioridades)
                })
                st.session_state['ve_counter'] += 1
                st.session_state['lista_perdidas'] = []
                st.success("Guardado.")
        
        if st.session_state['equipments']:
            st.markdown("---")
            loc = st.session_state['project_data']
            
            body = f"Hola Ing. Sotelo,%0D%0A%0D%0AProyecto: {loc.get('nombre')}%0D%0AUbicación: {loc.get('ubicacion')} (Alt: {loc.get('altitud')}m | Temp: {loc.get('temp')}C)%0D%0A%0D%0A"
            for eq in st.session_state['equipments']:
                body += f"[{eq['tag']}] {eq['cfm']} CFM @ {eq['sp']}\" | {eq['tipo_vent']} | App: {eq['app_type']} | {eq['voltaje']}%0D%0A"
            
            st.markdown(f'<a href="mailto:ventas@csventilacion.mx?subject=Cotización {loc.get("nombre")}&body={body}" style="display: inline-block; background-color: #28a745; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; width: 100%; text-align: center;">📧 ENVIAR POR CORREO</a>', unsafe_allow_html=True)
            
            with st.expander("📄 Ver Resumen para Imprimir (Ctrl+P)", expanded=False):
                st.markdown(f"### CS SISTEMAS DE AIRE - RESUMEN: {st.session_state.get('project_data', {}).get('nombre')}")
                st.markdown(f"**Ubicación:** {loc.get('ubicacion')} | **Alt:** {loc.get('altitud')}m")
                st.table(pd.DataFrame(st.session_state['equipments']))
                st.caption("Presiona Ctrl + P en tu navegador para imprimir.")

    else:
        if st.session_state.get('vel_actual', 0) > 4000:
            st.error("Velocidad excesiva (> 4000 FPM). Corrige el ducto.")
        else:
            st.info("Completa los pasos anteriores.")
