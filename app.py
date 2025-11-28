import streamlit as st
import pandas as pd
import math

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Calculadora Cocinas V4.1",
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

# --- BASE DE DATOS GEOGRÁFICA ---
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
    "Veracruz": {"Veracruz": {"alt": 10, "temp": 30}, "Xalapa": {"alt": 1400, "temp": 24}, "Coatzacoalcos": {"alt": 10, "temp": 32}}
}

# --- FUNCIONES DE CÁLCULO ---
def get_auto_dims(cfm_target, velocity_target=2000):
    if cfm_target <= 0: return 6, 6
    target_area = cfm_target / velocity_target
    diam_ideal = math.sqrt(target_area * 4 / math.pi) * 12
    diam_final = round(diam_ideal / 2) * 2
    if diam_final < 6: diam_final = 6
    
    side_ideal = math.sqrt(target_area) * 12
    side_final = round(side_ideal / 2) * 2
    if side_final < 6: side_final = 6
    return int(side_final), int(diam_final)

# --- SIDEBAR ---
with st.sidebar:
    # Intento de cargar logo con manejo de errores para que no falle
    try:
        st.image("LOGO ONLINE.jpg", use_column_width=True)
    except:
        st.header("CS VENTILACIÓN")
        st.caption("Nota: Sube 'LOGO ONLINE.jpg' a GitHub para ver el logo.")
    
    st.markdown("---")
    
    with st.expander("📍 Detalles del Proyecto", expanded=True):
        nombre_proyecto = st.text_input("Nombre Proyecto", placeholder="Ej. Restaurante Centro")
        pais = st.selectbox("País", ["México", "Otro"])
        
        alt_res = 0
        temp_res = 25
        ciudad_str = ""
        
        if pais == "México":
            estado = st.selectbox("Estado", list(db_geo.keys()))
            ciudad = st.selectbox("Ciudad", list(db_geo[estado].keys()))
            datos = db_geo[estado][ciudad]
            alt_res = datos['alt']
            temp_res = datos['temp']
            ciudad_str = f"{ciudad}, {estado}"
            
            c1, c2 = st.columns(2)
            with c1: st.metric("Altitud", f"{alt_res} m")
            with c2: st.metric("Temp", f"{temp_res}°C")
        else:
            ciudad_str = st.text_input("Ciudad / Ubicación")
            alt_res = st.number_input("Altitud (msnm)", 0)
            temp_res = st.number_input("Temperatura (°C)", 25)
            
        st.session_state['loc_data'] = {"ciudad_full": ciudad_str, "alt": alt_res, "temp": temp_res}
        st.session_state['proj_name'] = nombre_proyecto

    st.markdown("---")
    st.markdown("**Partidas Guardadas:**")
    if len(st.session_state['equipments']) > 0:
        for item in st.session_state['equipments']:
            st.caption(f"🔹 {item['tag']} | {item['cfm']} CFM")
        if st.button("🗑️ Reiniciar Lista"):
            st.session_state['equipments'] = []
            st.session_state['ve_counter'] = 1
            st.rerun()

# --- HEADER ---
st.markdown('<div class="main-header">CALCULADORA PARA COCINAS COMERCIALES</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">Partida Actual: <strong>VE-{st.session_state["ve_counter"]:02d}</strong></div>', unsafe_allow_html=True)
st.markdown("---")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["1️⃣ Caudal", "2️⃣ Ductos", "3️⃣ Cierre"])

# --- TAB 1: CAUDAL ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        largo = st.number_input("Largo Campana (m)", 0.5, 10.0, 2.0, step=0.1)
        ancho = st.number_input("Ancho Campana (m)", 0.5, 5.0, 1.0, step=0.1)
        distancia = st.number_input("Distancia Captación (m)", 0.1, 2.0, 1.0, step=0.05)
        
    with col2:
        instalacion = st.selectbox("Instalación", 
                                   ["Adosada a una pared (3 lados abiertos)", 
                                    "Isla (4 lados abiertos)", 
                                    "Esquina (2 lados abiertos)"])
        
        apps = {
            "Light Duty (Hornos, Vapor, Marmitas, Lavaplatos)": 0.25,
            "Medium Duty (Estufas, Planchas, Freidoras pequeñas)": 0.35,
            "Heavy Duty (Parrillas gas, Carbón, Freidoras alto volumen)": 0.40,
            "Extra Heavy Duty (Wok, Leña sólida, Espadas, Mesquite)": 0.50
        }
        app_key = st.selectbox("Aplicación", list(apps.keys()))
        vc_val = apps[app_key]
        st.session_state['current_app_type'] = app_key
        
    if "Isla" in instalacion: P = (2*largo) + (2*ancho)
    elif "Adosada" in instalacion: P = (2*ancho) + largo
    else: P = ancho + largo
    
    Q_m3s = (P * distancia) * vc_val
    Q_cfm = (Q_m3s * 3600) / 1.699
    
    st.info(f"Velocidad de Captación seleccionada: **{vc_val} m/s**")
    
    col_res1, col_res2 = st.columns([1,2])
    with col_res1: st.metric("Perímetro Libre", f"{P:.2f} m")
    with col_res2:
        st.markdown(f"""
        <div style="background-color: #0E4F8F; color: white; padding: 10px; border-radius: 5px; text-align: center;">
            <small>Caudal Requerido</small><br>
            <strong style="font-size: 24px;">{int(Q_cfm)} CFM</strong>
        </div>
        """, unsafe_allow_html=True)
        
    if st.button("✅ Usar este Caudal"):
        st.session_state['cfm_actual'] = int(Q_cfm)
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
                
        vel = cfm_val / area_ft2 if area_ft2 > 0 else 0
        pd = (vel/4005)**2
        
        with c_res:
            st.metric("Velocidad", f"{int(vel)} FPM")
            st.caption(f"De: {de:.1f}\" | Pd: {pd:.3f} in")
            
        if vel < 1500:
            st.markdown('<div class="danger-box">⚠️ <strong>VELOCIDAD BAJA (< 1500 FPM)</strong><br>Peligro crítico de acumulación de grasa e incendio. Reduzca dimensiones.</div>', unsafe_allow_html=True)
        elif 1500 <= vel <= 2500:
            st.markdown('<div class="success-box">✅ <strong>VELOCIDAD IDEAL (1500-2500 FPM)</strong><br>Rango óptimo para transporte de vapores de grasa.</div>', unsafe_allow_html=True)
        elif 2500 < vel <= 4000:
            st.markdown('<div class="warning-box">⚠️ <strong>ALTA VELOCIDAD (> 2500 FPM)</strong><br>Nivel de ruido y de presión estática excesiva, alto consumo energético.</div>', unsafe_allow_html=True)
        else:
            st.error("⛔ VELOCIDAD NO ADMISIBLE (> 4000 FPM). Cálculo fuera de norma.")
            
        st.session_state['vel_actual'] = vel
        st.session_state['pd_ref'] = pd
        st.session_state['de_ref'] = de
    else:
        st.info("Calcula el caudal primero.")

# --- TAB 3: CIERRE ---
with tab3:
    if st.session_state.get('vel_actual', 0) > 0 and st.session_state.get('vel_actual', 0) <= 4000:
        pd_ref = st.session_state['pd_ref']
        de_ref = st.session_state['de_ref']
        
        st.markdown(f"**Cálculo de Pérdidas** (Pd: {pd_ref:.3f})")
        if 'losses' not in st.session_state: st.session_state['losses'] = []
        
        c_in1, c_in2, c_btn = st.columns([3, 2, 1])
        with c_in1:
            comp = st.selectbox("Accesorio", ["Tramos Rectos (Metros)", "Codo", "Dispositivo de Captación", "Filtro Inercial de Grasa Tipo Bafle", "Ampliación", "Reducción", "Otras Pérdidas"])
            ang, rad = None, None
            if comp == "Codo":
                c1, c2 = st.columns(2)
                with c1: ang = st.selectbox("Ángulo", ["90°", "45°", "30°"])
                with c2: rad = st.selectbox("Radio", ["Largo", "Corto"])
        
        with c_in2:
            if "Tramos" in comp: val = st.number_input("Longitud (m)", 0.0, 500.0, 1.0, step=0.5)
            elif "Otras" in comp: val = st.number_input("Presión (in wg)", 0.0, 5.0, 0.1, step=0.1)
            else: val = st.number_input("Cantidad", 1, 100, 1)
                
        with c_btn:
            st.write("")
            st.write("")
            if st.button("➕"):
                loss = 0
                desc = ""
                if "Tramos" in comp:
                    ft = val * 3.281
                    loss = (0.018 * (ft/(de_ref/12))) * pd_ref
                    desc = f"Tramo Recto ({val}m)"
                elif comp == "Codo":
                    n = 0.30
                    if ang == "90°": n = 0.30 if rad == "Largo" else 0.50
                    elif ang == "45°": n = 0.18
                    elif ang == "30°": n = 0.12
                    loss = n * pd_ref * val
                    desc = f"Codo {ang} {rad} ({val})"
                elif "Captación" in comp:
                    loss = 0.50 * pd_ref * val
                    desc = f"Entrada Campana ({val})"
                elif "Filtro" in comp:
                    loss = 0.50 * val
                    desc = f"Filtro Inercial Bafle ({val})"
                elif "Ampliación" in comp:
                    loss = 0.55 * pd_ref * val
                    desc = f"Ampliación ({val})"
                elif "Reducción" in comp:
                    loss = 0.05 * pd_ref * val
                    desc = f"Reducción ({val})"
                elif "Otras" in comp:
                    loss = val
                    desc = "Pérdida Manual"
                st.session_state['losses'].append({"Item": desc, "Pe": loss})
        
        if st.session_state['losses']:
            st.table(pd.DataFrame(st.session_state['losses']))
            total_sp = sum(item['Pe'] for item in st.session_state['losses'])
            st.metric("Presión Estática Total", f"{total_sp:.3f} in wg")
            
            st.markdown("---")
            st.markdown("#### Selección de Equipo")
            
            prioridades = st.multiselect("Prioridades (Máx 2)", ["Costo Inicial", "Nivel Sonoro", "Consumo Energético"], max_selections=2)
            tipo_vent = st.radio("Tipo de Ventilador", ["Hongo (Tejado)", "Ventset (Centrífugo)", "Tuboaxial"], horizontal=True)
            c_elec, c_ubi = st.columns(2)
            with c_elec: volt = st.radio("Voltaje", ["Monofásico", "Trifásico"])
            with c_ubi: ubi = st.radio("Ubicación", ["Interior", "Exterior"])
            
            if st.button("💾 GUARDAR PARTIDA"):
                tag = f"VE-{st.session_state['ve_counter']:02d}"
                st.session_state['equipments'].append({
                    "tag": tag,
                    "cfm": int(st.session_state['cfm_actual']),
                    "sp": round(total_sp, 3),
                    "tipo_vent": tipo_vent,
                    "voltaje": volt,
                    "ubicacion": ubi,
                    "app_type": st.session_state.get('current_app_type', 'N/A'),
                    "prioridades": ", ".join(prioridades)
                })
                st.session_state['ve_counter'] += 1
                st.session_state['losses'] = []
                st.success("Partida Guardada.")
                
        if st.session_state['equipments']:
            st.markdown("---")
            st.markdown("### 📤 Finalizar")
            
            # Resumen visual para imprimir
            with st.expander("📄 Ver Resumen para Imprimir", expanded=False):
                st.markdown("### CS SISTEMAS DE AIRE - RESUMEN DE PROYECTO")
                st.markdown(f"**Proyecto:** {st.session_state.get('proj_name')} | **Ubicación:** {st.session_state['loc_data']['ciudad_full']}")
                st.markdown(f"**Condiciones:** Alt {st.session_state['loc_data']['alt']}m | Temp {st.session_state['loc_data']['temp']}C")
                st.table(pd.DataFrame(st.session_state['equipments']))
                st.caption("Presiona Ctrl + P para imprimir esta vista o guardarla como PDF.")
            
            loc = st.session_state['loc_data']
            body = f"Hola Ing. Sotelo,%0D%0A%0D%0AAdjunto resumen para el proyecto {st.session_state.get('proj_name', '')}.%0D%0A"
            body += f"Ubicación: {loc.get('ciudad_full')} (Alt: {loc.get('alt')}m | Temp: {loc.get('temp')}C).%0D%0A%0D%0A"
            for eq in st.session_state['equipments']:
                body += f"[{eq['tag']}] {eq['cfm']} CFM @ {eq['sp']}\" | {eq['tipo_vent']} | App: {eq['app_type']} | {eq['voltaje']}%0D%0A"
            
            st.markdown(f'<a href="mailto:ventas@csventilacion.mx?subject=Cotización {st.session_state.get("proj_name")}&body={body}" style="display: inline-block; background-color: #28a745; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; width: 100%; text-align: center;">📧 ENVIAR POR CORREO</a>', unsafe_allow_html=True)

    else:
        st.info("Corrige la velocidad o calcula el caudal primero.")
