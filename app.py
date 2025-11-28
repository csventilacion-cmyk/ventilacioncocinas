import streamlit as st
import pandas as pd
import math

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="CS Ventilación - Calculadora Cocinas",
    page_icon="❄️",
    layout="centered"
)

# --- ESTILOS VISUALES ---
st.markdown("""
    <style>
    .main-header {
        font-size: 28px;
        font-weight: bold;
        color: #0E4F8F; 
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 18px;
        color: #666;
        text-align: center;
        margin-top: 5px;
    }
    .metric-box {
        padding: 10px;
        background-color: #f0f2f6;
        border-radius: 5px;
        margin-bottom: 10px;
        text-align: center;
    }
    .success-box {
        padding: 10px;
        background-color: #d4edda;
        color: #155724;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .warning-box {
        padding: 10px;
        background-color: #fff3cd;
        color: #856404;
        border-radius: 5px;
        border: 1px solid #ffeeba;
    }
    .danger-box {
        padding: 10px;
        background-color: #f8d7da;
        color: #721c24;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE ESTADO ---
if 'equipments' not in st.session_state:
    st.session_state['equipments'] = []
if 've_counter' not in st.session_state:
    st.session_state['ve_counter'] = 1

# --- BASE DE DATOS GEOGRÁFICA (PRINCIPALES CIUDADES POR ESTADO) ---
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
    """Calcula dimensiones óptimas (múltiplos de 2) para acercarse a 2000 FPM"""
    target_area = cfm_target / velocity_target # ft2
    
    # Circular
    diam_ideal = math.sqrt(target_area * 4 / math.pi) * 12 # inches
    diam_final = round(diam_ideal / 2) * 2 # Redondear al par más cercano
    if diam_final < 4: diam_final = 4
    
    # Rectangular (Cuadrado por defecto)
    side_ideal = math.sqrt(target_area) * 12 # inches
    side_final = round(side_ideal / 2) * 2
    if side_final < 4: side_final = 4
    
    return int(side_final), int(diam_final)

# --- SIDEBAR ---
with st.sidebar:
    try:
        st.image("logo.jpg", use_column_width=True) 
    except:
        st.header("CS VENTILACIÓN")
    
    st.markdown("---")
    st.header("📍 Datos del Proyecto")
    
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
    else:
        st.caption("Sin equipos.")

# --- TÍTULO PRINCIPAL ---
st.markdown('<div class="main-header">CALCULADORA PARA COCINAS COMERCIALES</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">Partida Actual: <strong>VE-{st.session_state["ve_counter"]:02d}</strong></div>', unsafe_allow_html=True)
st.markdown("---")

# --- TABS DE TRABAJO ---
tab1, tab2, tab3 = st.tabs(["1️⃣ Caudal (Campana)", "2️⃣ Ductos (Velocidad)", "3️⃣ Presión y Cierre"])

# --- TAB 1: CÁLCULO DE CAUDAL ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Dimensiones Campana (Metros)**")
        largo = st.number_input("Largo (m)", min_value=0.5, value=2.0, step=0.1)
        ancho = st.number_input("Ancho (m)", min_value=0.5, value=1.0, step=0.1)
        distancia = st.number_input("Distancia de Captación (m)", min_value=0.1, value=1.0, step=0.05)
        
    with col2:
        st.markdown("**Condiciones de Operación**")
        instalacion = st.selectbox("Instalación", 
                                   ["Adosada a una pared (3 lados abiertos)", 
                                    "Isla (4 lados abiertos)", 
                                    "Esquina (2 lados abiertos)"])
        
        aplicacion_dict = {
            "Light Duty (Hornos, Vapor, Marmitas)": 0.25,
            "Medium Duty (Estufas, Planchas, Freidoras pequeñas)": 0.35,
            "Heavy Duty (Parrillas gas, Carbón, Freidoras alto volumen)": 0.40,
            "Extra Heavy Duty (Wok, Leña sólida, Espadas)": 0.50
        }
        
        aplicacion_key = st.selectbox("Aplicación", list(aplicacion_dict.keys()))
        vc_val = aplicacion_dict[aplicacion_key]
    
    # Cálculo Caudal (Metodología Manual)
    # Perímetro Libre
    if "Isla" in instalacion: perimetro = (2 * largo) + (2 * ancho)
    elif "Adosada" in instalacion: perimetro = (2 * ancho) + largo
    elif "Esquina" in instalacion: perimetro = ancho + largo
    else: perimetro = (2 * largo) + (2 * ancho)
    
    area_paso = perimetro * distancia
    caudal_m3s = area_paso * vc_val
    caudal_m3hr = caudal_m3s * 3600
    caudal_cfm = caudal_m3hr / 1.699
    
    st.markdown("---")
    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1: st.metric("Velocidad Captación", f"{vc_val} m/s")
    with res_col2: st.metric("Perímetro Libre", f"{perimetro:.2f} m")
    with res_col3:
        st.markdown(f"""
        <div style="background-color: #0E4F8F; color: white; padding: 10px; border-radius: 5px; text-align: center;">
            <small>Caudal Requerido</small><br>
            <strong style="font-size: 24px;">{int(caudal_cfm)} CFM</strong>
        </div>
        """, unsafe_allow_html=True)
        
    if st.button("✅ Confirmar Caudal y Dimensionar Ductos"):
        st.session_state['cfm_actual'] = int(caudal_cfm)
        st.success(f"Caudal de {int(caudal_cfm)} CFM fijado.")

# --- TAB 2: DUCTOS ---
with tab2:
    cfm_ducto = st.number_input("Caudal de Diseño (CFM)", value=st.session_state.get('cfm_actual', 0))
    
    if cfm_ducto > 0:
        # Calcular dimensiones ideales (Múltiplos de 2 para 2000 FPM)
        ideal_side, ideal_diam = get_auto_dims(cfm_ducto, 2000)
        
        c_dims, c_info = st.columns([2, 1])
        with c_dims:
            tipo_ducto = st.radio("Forma", ["Rectangular", "Circular"], horizontal=True)
            
            if tipo_ducto == "Rectangular":
                cc1, cc2 = st.columns(2)
                with cc1: w_in = st.number_input("Ancho (pulgadas)", min_value=4, value=ideal_side, step=2)
                with cc2: h_in = st.number_input("Alto (pulgadas)", min_value=4, value=ideal_side, step=2)
                area_ft2 = (w_in * h_in) / 144
                diam_eq = 1.3 * ((w_in * h_in)**0.625) / ((w_in + h_in)**0.25)
            else:
                d_in = st.number_input("Diámetro (pulgadas)", min_value=4, value=ideal_diam, step=2)
                area_ft2 = (math.pi * (d_in/12)**2) / 4
                diam_eq = d_in
                
        velocidad = cfm_ducto / area_ft2 if area_ft2 > 0 else 0
        pd_val = (velocidad / 4005)**2
        
        with c_info:
            st.markdown("##### Resultados:")
            st.metric("Velocidad", f"{int(velocidad)} FPM")
            st.caption(f"Diámetro Eq: {diam_eq:.1f}\"")
            st.caption(f"Presión Dinámica: {pd_val:.3f} in wg")
            
        if 1500 <= velocidad <= 3000:
            st.markdown('<div class="success-box">✅ <strong>VELOCIDAD ÓPTIMA</strong><br>1500-3000 FPM</div>', unsafe_allow_html=True)
        elif velocidad < 1500:
            st.markdown('<div class="danger-box">⚠️ <strong>VELOCIDAD BAJA</strong><br>Riesgo de acumulación de grasa.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box">⚠️ <strong>VELOCIDAD ALTA</strong><br>Riesgo de ruido excesivo.</div>', unsafe_allow_html=True)
            
        st.session_state['vel_actual'] = velocidad
        st.session_state['pd_actual'] = pd_val
        st.session_state['de_actual'] = diam_eq
    else:
        st.info("Define el caudal en la Pestaña 1.")

# --- TAB 3: PRESIÓN Y CIERRE ---
with tab3:
    if st.session_state.get('vel_actual', 0) > 0:
        pd_ref = st.session_state['pd_actual']
        de_ref = st.session_state['de_actual']
        
        st.markdown(f"**Cálculo de Pérdidas** (Pd Ref: {pd_ref:.3f} in wg)")
        
        if 'lista_perdidas' not in st.session_state:
            st.session_state['lista_perdidas'] = []
            
        # --- INPUTS DE COMPONENTES ---
        col_type, col_val, col_btn = st.columns([3, 2, 1])
        
        with col_type:
            tipo_acc = st.selectbox("Componente", 
                                    ["Tramos Rectos", 
                                     "Codo", 
                                     "Dispositivo de Captación", 
                                     "Filtro Inercial de Grasa Tipo Bafle",
                                     "Ampliación",
                                     "Reducción",
                                     "Otras Pérdidas"])
            
            # Submenú para Codos
            codo_grados = None
            codo_tipo = None
            
            if tipo_acc == "Codo":
                c1, c2 = st.columns(2)
                with c1: codo_grados = st.selectbox("Ángulo", ["90°", "45°", "30°"])
                with c2: codo_tipo = st.selectbox("Radio", ["Largo", "Corto"])

        with col_val:
            if tipo_acc == "Tramos Rectos":
                val_input = st.number_input("Longitud (Metros)", 0.0, 500.0, 1.0, step=0.5)
            elif tipo_acc == "Otras Pérdidas":
                val_input = st.number_input("Presión (in wg)", 0.0, 5.0, 0.1, step=0.1)
            else:
                val_input = st.number_input("Cantidad (Pzas)", 1, 100, 1)
        
        with col_btn:
            st.write("")
            st.write("")
            if st.button("➕ Agregar"):
                perdida = 0
                desc = ""
                
                # Lógica Coeficientes Ocultos
                if tipo_acc == "Tramos Rectos":
                    # Convertir metros a pies para cálculo Darcy aproximado
                    feet = val_input * 3.281
                    d_ft = de_ref / 12
                    perdida = (0.018 * (feet/d_ft)) * pd_ref
                    desc = f"Tramo Recto ({val_input} m)"
                    
                elif tipo_acc == "Codo":
                    n = 0.30 # Default
                    if codo_grados == "90°": n = 0.30 if codo_tipo == "Largo" else 0.50
                    elif codo_grados == "45°": n = 0.18
                    elif codo_grados == "30°": n = 0.12
                    
                    perdida = n * pd_ref * val_input
                    desc = f"Codo {codo_grados} {codo_tipo} ({val_input} pzas)"
                    
                elif tipo_acc == "Dispositivo de Captación":
                    perdida = 0.50 * pd_ref * val_input
                    desc = f"Dispositivo Captación ({val_input} pzas)"
                    
                elif tipo_acc == "Filtro Inercial de Grasa Tipo Bafle":
                    perdida = 0.50 * val_input
                    desc = f"Filtro Inercial Bafle ({val_input} pzas)"
                    
                elif tipo_acc == "Ampliación":
                    perdida = 0.55 * pd_ref * val_input
                    desc = f"Ampliación ({val_input} pzas)"
                    
                elif tipo_acc == "Reducción":
                    perdida = 0.05 * pd_ref * val_input
                    desc = f"Reducción ({val_input} pzas)"
                    
                elif tipo_acc == "Otras Pérdidas":
                    perdida = val_input
                    desc = "Pérdida Adicional Manual"
                
                st.session_state['lista_perdidas'].append({"Concepto": desc, "Pe (in wg)": perdida})

        # --- TABLA RESUMEN ---
        total_sp = 0
        if len(st.session_state['lista_perdidas']) > 0:
            st.markdown("---")
            st.table(pd.DataFrame(st.session_state['lista_perdidas']))
            total_sp = sum(item['Pe (in wg)'] for item in st.session_state['lista_perdidas'])
            st.metric("Presión Estática Total", f"{total_sp:.3f} in wg")
            
            # --- OPCIONES FINALES ANTES DE GUARDAR ---
            st.markdown("#### ⚙️ Opciones de Selección de Equipo")
            
            c_pref, c_elec, c_loc = st.columns(3)
            with c_pref:
                st.markdown("**Prioridades:**")
                p1 = st.checkbox("Costo")
                p2 = st.checkbox("Nivel Sonoro")
                p3 = st.checkbox("Eficiencia Energética")
                prioridades = ", ".join([p for p, chk in [("Costo", p1), ("Sonido", p2), ("Energía", p3)] if chk])
            
            with c_elec:
                voltaje = st.radio("Alimentación", ["Monofásico", "Trifásico"])
                
            with c_loc:
                ubicacion_eq = st.radio("Instalación", ["Uso Interior", "Uso Exterior"])
            
            if st.button("💾 GUARDAR PARTIDA"):
                tag = f"VE-{st.session_state['ve_counter']:02d}"
                st.session_state['equipments'].append({
                    "tag": tag,
                    "cfm": int(st.session_state['cfm_actual']),
                    "sp": round(total_sp, 3),
                    "voltaje": voltaje,
                    "ubicacion": ubicacion_eq,
                    "prioridades": prioridades if prioridades else "Estándar"
                })
                st.session_state['ve_counter'] += 1
                st.session_state['lista_perdidas'] = []
                st.success(f"¡Equipo {tag} guardado!")

        # --- BOTÓN FINAL DE CORREO ---
        if len(st.session_state['equipments']) > 0:
            st.markdown("---")
            st.info("Revisa el resumen en la barra lateral antes de enviar.")
            
            p_data = st.session_state.get('project_data', {})
            loc_data = st.session_state.get('location_data', {})
            
            subject = f"Cotización: {p_data.get('nombre', 'Sin Nombre')}"
            
            body = f"Hola Ing. Sotelo,%0D%0A%0D%0ASolicito cotización para el proyecto: {p_data.get('nombre')}%0D%0A"
            body += f"📍 UBICACIÓN: {p_data.get('ubicacion')} (Alt: {loc_data.get('alt',0)}m | Temp: {loc_data.get('temp',0)}C)%0D%0A%0D%0A"
            body += "📋 LISTADO DE EQUIPOS:%0D%0A"
            
            for eq in st.session_state['equipments']:
                body += f"[{eq['tag']}] {eq['cfm']} CFM @ {eq['sp']} in wg | {eq['voltaje']} | {eq['ubicacion']} | Prioridad: {eq['prioridades']}%0D%0A"
            
            st.markdown(f"""
                <a href="mailto:ventas@csventilacion.mx?subject={subject}&body={body}" 
                   style="display: inline-block; background-color: #28a745; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; width: 100%; text-align: center; font-size: 18px;">
                   🚀 FINALIZAR Y ENVIAR POR CORREO
                </a>
            """, unsafe_allow_html=True)
            
    else:
        st.warning("Completa los pasos 1 y 2 para calcular presión.")
