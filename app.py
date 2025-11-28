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

# --- BASE DE DATOS GEOGRÁFICA ---
ciudades_db = {
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
    "Querétaro": ["Santiago de Querétaro", "San Juan del Río", "El Marqués"],
    "Quintana Roo": ["Cancún", "Playa del Carmen", "Chetumal"],
    "San Luis Potosí": ["San Luis Potosí", "Soledad de Graciano Sánchez", "Ciudad Valles"],
    "Sinaloa": ["Culiacán", "Mazatlán", "Los Mochis"],
    "Sonora": ["Hermosillo", "Ciudad Obregón", "Nogales"],
    "Tabasco": ["Villahermosa", "Cárdenas", "Comalcalco"],
    "Tamaulipas": ["Reynosa", "Matamoros", "Nuevo Laredo"],
    "Tlaxcala": ["Tlaxcala", "Apizaco", "Huamantla"],
    "Veracruz": ["Veracruz", "Xalapa", "Coatzacoalcos"],
    "Yucatán": ["Mérida", "Kanasín", "Valladolid"],
    "Zacatecas": ["Zacatecas", "Guadalupe", "Fresnillo"]
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
    
    with st.expander("📍 Datos del Proyecto", expanded=True):
        nombre_proyecto = st.text_input("Nombre del Proyecto", placeholder="Ej. Restaurante La Plaza")
        pais = st.selectbox("País", ["México", "Otro"])
        
        ciudad_selec = ""
        estado_selec = ""
        
        if pais == "México":
            estado_selec = st.selectbox("Estado", list(ciudades_db.keys()))
            ciudad_selec = st.selectbox("Ciudad", ciudades_db[estado_selec])
        else:
            ciudad_selec = st.text_input("Ciudad / Ubicación")
        
        st.session_state['project_data'] = {
            "nombre": nombre_proyecto,
            "ubicacion": f"{ciudad_selec}, {estado_selec}" if pais == "México" else ciudad_selec
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

# --- TÍTULO PRINCIPAL ---
st.markdown('<div class="main-header">CALCULADORA PARA COCINAS COMERCIALES</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">Partida Actual: <strong>VE-{st.session_state["ve_counter"]:02d}</strong></div>', unsafe_allow_html=True)
st.markdown("---")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["1️⃣ Caudal", "2️⃣ Ductos", "3️⃣ Cierre"])

# --- TAB 1: CAUDAL ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Dimensiones Campana (Metros)**")
        largo = st.number_input("Largo (m)", 0.5, 10.0, 2.0, step=0.1)
        ancho = st.number_input("Ancho (m)", 0.5, 5.0, 1.0, step=0.1)
        distancia = st.number_input("Distancia Captación (m)", 0.1, 2.0, 1.0, step=0.05)
        
    with col2:
        st.markdown("**Condiciones**")
        instalacion = st.selectbox("Instalación", ["Adosada a una pared", "Isla", "Esquina"])
        
        apps = {
            "Light Duty (Hornos, Vapor)": 0.25,
            "Medium Duty (Estufas, Planchas)": 0.35,
            "Heavy Duty (Parrillas, Carbón)": 0.40,
            "Extra Heavy Duty (Wok, Leña)": 0.50
        }
        app_key = st.selectbox("Aplicación", list(apps.keys()))
        vc_val = apps[app_key]
        st.session_state['current_app_type'] = app_key
        
    if "Isla" in instalacion: P = (2*largo) + (2*ancho)
    elif "Adosada" in instalacion: P = (2*ancho) + largo
    else: P = ancho + largo
    
    Q_cfm = ((P * distancia) * vc_val * 3600) / 1.699
    
    st.info(f"Velocidad de Captación: **{vc_val} m/s**")
    
    c1, c2 = st.columns(2)
    with c1: st.metric("Perímetro Libre", f"{P:.2f} m")
    with c2: st.metric("Caudal Requerido", f"{int(Q_cfm)} CFM")
        
    if st.button("✅ Confirmar Caudal"):
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
        
        if area_ft2 > 0:
            vel = cfm_val / area_ft2
            pd_val = (vel/4005)**2
        else:
            vel = 0
            pd_val = 0
        
        with c_res:
            st.metric("Velocidad", f"{int(vel)} FPM")
            st.caption(f"De: {de:.1f}\" | Pd: {pd_val:.3f} in")
            
        if vel < 1500:
            st.markdown('<div class="danger-box">⚠️ VELOCIDAD BAJA (< 1500 FPM)</div>', unsafe_allow_html=True)
        elif 1500 <= vel <= 3000:
            st.markdown('<div class="success-box">✅ VELOCIDAD ÓPTIMA</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box">⚠️ VELOCIDAD ALTA (> 3000 FPM)</div>', unsafe_allow_html=True)
            
        st.session_state['vel_actual'] = vel
        st.session_state['pd_ref'] = pd_val
        st.session_state['de_ref'] = de
    else:
        st.info("Calcula el caudal primero.")

# --- TAB 3: CIERRE ---
with tab3:
    if st.session_state.get('vel_actual', 0) > 0:
        pd_ref = st.session_state['pd_ref']
        de_ref = st.session_state['de_ref']
        
        st.markdown(f"**Cálculo de Pérdidas** (Pd: {pd_ref:.3f})")
        if 'losses' not in st.session_state: st.session_state['losses'] = []
        
        c1, c2, c3 = st.columns([3, 2, 1])
        with c1:
            comp = st.selectbox("Accesorio", ["Tramos Rectos", "Codo", "Entrada Campana", "Filtros", "Ampliación", "Reducción", "Otras"])
        with c2:
            val = st.number_input("Cant/Longitud", 0.0, 500.0, 1.0, step=0.5)
        with c3:
            st.write("")
            st.write("")
            if st.button("➕"):
                loss = 0
                desc = ""
                # Protección div/0
                d_safe = de_ref if de_ref > 0 else 24
                
                if comp == "Tramos Rectos":
                    ft = val * 3.281
                    loss = (0.018 * (ft/(d_safe/12))) * pd_ref
                    desc = f"Tramo Recto ({val}m)"
                elif comp == "Codo":
                    loss = 0.30 * pd_ref * val
                    desc = f"Codos ({val})"
                elif comp == "Entrada Campana":
                    loss = 0.50 * pd_ref * val
                    desc = f"Entrada Campana ({val})"
                elif comp == "Filtros":
                    loss = 0.50 * val
                    desc = f"Banco Filtros ({val})"
                elif comp == "Ampliación":
                    loss = 0.55 * pd_ref * val
                    desc = f"Ampliación ({val})"
                elif comp == "Reducción":
                    loss = 0.05 * pd_ref * val
                    desc = f"Reducción ({val})"
                elif comp == "Otras":
                    loss = val
                    desc = "Manual"
                
                st.session_state['losses'].append({"Item": desc, "Pe": loss})
        
        if st.session_state['losses']:
            # Uso de dataframe para evitar errores de tabla
            df = pd.DataFrame(st.session_state['losses'])
            st.dataframe(df, use_container_width=True)
            
            total_sp = sum(item['Pe'] for item in st.session_state['losses'])
            st.metric("Presión Estática Total", f"{total_sp:.3f} in wg")
            
            st.markdown("---")
            st.markdown("#### Selección")
            
            prioridades = st.multiselect("Prioridades", ["Costo", "Sonido", "Energía"])
            volt = st.radio("Voltaje", ["Monofásico", "Trifásico"], horizontal=True)
            ubi = st.radio("Ubicación", ["Interior", "Exterior"], horizontal=True)
            
            if st.button("💾 GUARDAR PARTIDA"):
                tag = f"VE-{st.session_state['ve_counter']:02d}"
                st.session_state['equipments'].append({
                    "tag": tag,
                    "cfm": int(st.session_state['cfm_actual']),
                    "sp": round(total_sp, 3),
                    "voltaje": volt,
                    "ubicacion": ubi,
                    "app_type": st.session_state.get('current_app_type', 'N/A'),
                    "prioridades": ", ".join(prioridades)
                })
                st.session_state['ve_counter'] += 1
                st.session_state['losses'] = []
                st.success("Guardado.")
        
        if st.session_state['equipments']:
