import streamlit as st
import pandas as pd
import math

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="CS Ventilación - Calculadora Pro",
    page_icon="❄️",
    layout="centered"
)

# --- ESTILOS VISUALES ---
st.markdown("""
    <style>
    .main-header {
        font-size: 28px;
        font-weight: bold;
        color: #333; 
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
    st.session_state['equipments'] = []  # Lista para guardar VE-01, VE-02...
if 've_counter' not in st.session_state:
    st.session_state['ve_counter'] = 1   # Contador de partidas

# --- BASE DE DATOS GEOGRÁFICA (SIMPLIFICADA) ---
ciudades_db = {
    "Culiacán, Sinaloa": {"alt": 54, "temp": 35},
    "Ciudad de México": {"alt": 2240, "temp": 24},
    "Monterrey, Nuevo León": {"alt": 540, "temp": 32},
    "Guadalajara, Jalisco": {"alt": 1566, "temp": 28},
    "Tijuana, Baja California": {"alt": 20, "temp": 26},
    "Cancún, Quintana Roo": {"alt": 10, "temp": 30},
    "Hermosillo, Sonora": {"alt": 210, "temp": 40},
    "Mérida, Yucatán": {"alt": 10, "temp": 36},
    "Puebla, Puebla": {"alt": 2135, "temp": 25},
    "Querétaro, Querétaro": {"alt": 1820, "temp": 28}
}

# --- SIDEBAR: LOGO Y DATOS DE PROYECTO ---
with st.sidebar:
    # LOGO (Asegúrate de subir 'logo.jpg' a tu GitHub)
    try:
        st.image("logo.jpg", use_column_width=True) 
    except:
        st.header("CS VENTILACIÓN") # Texto de respaldo si no carga la imagen
    
    st.markdown("---")
    st.header("📍 Datos del Proyecto")
    
    pais = st.selectbox("País", ["México", "Otro"])
    
    if pais == "México":
        ciudad_select = st.selectbox("Ciudad / Zona", list(ciudades_db.keys()))
        datos_ciudad = ciudades_db[ciudad_select]
        st.caption(f"Altitud: {datos_ciudad['alt']} msnm | Temp. Prom: {datos_ciudad['temp']}°C")
    else:
        ciudad_select = st.text_input("Ciudad")
        altitud_manual = st.number_input("Altitud (msnm)", value=0)
        temp_manual = st.number_input("Temperatura (°C)", value=25)
        datos_ciudad = {"alt": altitud_manual, "temp": temp_manual}
        
    st.session_state['location_data'] = {
        "ciudad": ciudad_select,
        "alt": datos_ciudad['alt'],
        "temp": datos_ciudad['temp']
    }
    
    st.markdown("---")
    st.markdown("**Lista de Equipos:**")
    if len(st.session_state['equipments']) > 0:
        for item in st.session_state['equipments']:
            st.text(f"{item['tag']}: {item['cfm']} CFM")
        
        if st.button("🗑️ Borrar Lista"):
            st.session_state['equipments'] = []
            st.session_state['ve_counter'] = 1
            st.rerun()
    else:
        st.caption("No hay equipos guardados aún.")

# --- TÍTULO PRINCIPAL ---
st.markdown('<div class="main-header">CALCULADORA TÉCNICA</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">Partida Actual: <strong>VE-{st.session_state["ve_counter"]:02d}</strong></div>', unsafe_allow_html=True)
st.markdown("---")

# --- FUNCIONES DE CÁLCULO (MÉTODO INDUSTRIAL VENTILATION) ---
def calcular_caudal_metrico(largo_m, ancho_m, distancia_m, tipo_app, tipo_inst):
    # 1. Determinar Perímetro Libre (P)
    if tipo_inst == "Isla (4 lados abiertos)":
        perimetro = (2 * largo_m) + (2 * ancho_m)
    elif tipo_inst == "Pared (3 lados abiertos)":
        perimetro = (2 * ancho_m) + largo_m
    elif tipo_inst == "Esquina (2 lados abiertos)":
        perimetro = ancho_m + largo_m
    else:
        perimetro = (2 * largo_m) + (2 * ancho_m) # Default isla
        
    # 2. Velocidad de Captación (Vc) según Manual
    velocidades = {
        "Light Duty (Vapores ligeros)": 0.25,
        "Medium Duty (Cocción estándar)": 0.35,
        "Heavy Duty (Grasa abundante)": 0.40,
        "Extra Heavy Duty (Wok/Carbón)": 0.50
    }
    vc = velocidades.get(tipo_app, 0.25)
    
    # 3. Fórmula Q = P * D * Vc * 3600 (para m3/hr) -> Luego a CFM
    # Formula Industrial Ventilation: Q = Vc * (1.4 * P * D)? 
    # Usaremos la logica de tu manual (P * D * Vc) asumiendo área de paso teórica
    # Nota: Tu manual pag 33 dice: Q = (Suma Perimetro) * (Dist Captacion) * (Velocidad * 3600)
    
    area_paso = perimetro * distancia_m
    caudal_m3s = area_paso * vc
    caudal_m3hr = caudal_m3s * 3600
    caudal_cfm = caudal_m3hr / 1.699 # Factor conversión m3/hr a CFM
    
    return int(caudal_cfm), vc, perimetro

# --- TABS DE TRABAJO ---
tab1, tab2, tab3 = st.tabs(["1️⃣ Caudal (Campana)", "2️⃣ Ductos", "3️⃣ Presión y Cierre"])

# --- TAB 1: CÁLCULO DE CAMPANA ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Dimensiones Campana (Metros)**")
        largo = st.number_input("Largo (m)", min_value=0.5, value=2.0, step=0.1)
        ancho = st.number_input("Ancho (m)", min_value=0.5, value=1.0, step=0.1)
        distancia = st.number_input("Distancia de Captación (m)", min_value=0.1, value=1.0, step=0.1, help="Distancia vertical desde la fuente de calor hasta el filtro")
        
    with col2:
        st.markdown("**Condiciones de Operación**")
        instalacion = st.selectbox("Instalación", ["Pared (3 lados abiertos)", "Isla (4 lados abiertos)", "Esquina (2 lados abiertos)"])
        aplicacion = st.selectbox("Aplicación", 
                                  ["Light Duty (Vapores ligeros)", 
                                   "Medium Duty (Cocción estándar)", 
                                   "Heavy Duty (Grasa abundante)", 
                                   "Extra Heavy Duty (Wok/Carbón)"])
    
    # Calcular en tiempo real
    cfm_calc, vc_used, perim_calc = calcular_caudal_metrico(largo, ancho, distancia, aplicacion, instalacion)
    
    st.markdown("---")
    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1:
        st.metric("Velocidad Captación", f"{vc_used} m/s")
    with res_col2:
        st.metric("Perímetro Libre", f"{perim_calc:.2f} m")
    with res_col3:
        st.markdown(f"""
        <div style="background-color: #0E4F8F; color: white; padding: 10px; border-radius: 5px; text-align: center;">
            <small>Caudal Requerido</small><br>
            <strong style="font-size: 24px;">{cfm_calc} CFM</strong>
        </div>
        """, unsafe_allow_html=True)
        
    if st.button("✅ Confirmar Caudal y Pasar a Ductos"):
        st.session_state['cfm_actual'] = cfm_calc
        st.success(f"Caudal de {cfm_calc} CFM fijado para diseño de ductos.")

# --- TAB 2: DUCTOS ---
with tab2:
    cfm_ducto = st.number_input("Caudal de Diseño (CFM)", value=st.session_state.get('cfm_actual', 0))
    
    if cfm_ducto > 0:
        c_dims, c_info = st.columns([2, 1])
        
        with c_dims:
            tipo_ducto = st.radio("Forma", ["Rectangular", "Circular"], horizontal=True)
            area_ft2 = 0
            
            if tipo_ducto == "Rectangular":
                cc1, cc2 = st.columns(2)
                with cc1: w_in = st.number_input("Ancho (pulgadas)", 10.0, step=2.0)
                with cc2: h_in = st.number_input("Alto (pulgadas)", 10.0, step=2.0)
                area_ft2 = (w_in * h_in) / 144
                diam_eq = 1.3 * ((w_in * h_in)**0.625) / ((w_in + h_in)**0.25)
            else:
                d_in = st.number_input("Diámetro (pulgadas)", 10.0, step=2.0)
                area_ft2 = (math.pi * (d_in/12)**2) / 4
                diam_eq = d_in
                
        # Cálculo Velocidad
        velocidad = cfm_ducto / area_ft2
        pd_val = (velocidad / 4005)**2  # Presión dinámica
        
        with c_info:
            st.markdown("##### Resultados:")
            st.metric("Velocidad", f"{int(velocidad)} FPM")
            st.caption(f"Diámetro Eq: {diam_eq:.1f}\"")
            st.caption(f"Presión Dinámica: {pd_val:.3f} in wg")
            
        # Semáforo
        if 1500 <= velocidad <= 3000:
            st.markdown('<div class="success-box">✅ <strong>VELOCIDAD CORRECTA</strong><br>Rango ideal para transporte de grasa (1500-3000 FPM).</div>', unsafe_allow_html=True)
        elif velocidad < 1500:
            st.markdown('<div class="danger-box">⚠️ <strong>PELIGRO: VELOCIDAD BAJA</strong><br>Riesgo alto de acumulación de grasa e incendio. Reduce el ducto.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box">⚠️ <strong>PRECAUCIÓN: VELOCIDAD ALTA</strong><br>Posible ruido excesivo y alto consumo. Aumenta el ducto.</div>', unsafe_allow_html=True)
            
        st.session_state['vel_actual'] = velocidad
        st.session_state['pd_actual'] = pd_val
        st.session_state['de_actual'] = diam_eq
    else:
        st.info("Define el caudal en la Pestaña 1.")

# --- TAB 3: PÉRDIDA DE CARGA Y CIERRE ---
with tab3:
    if st.session_state.get('vel_actual', 0) > 0:
        pd_ref = st.session_state['pd_actual']
        de_ref = st.session_state['de_actual']
        
        st.markdown(f"**Cálculo de Pérdidas (Sistema Inglés)** | Pd Ref: {pd_ref:.3f} in wg")
        
        # --- INPUTS DE ACCESORIOS ---
        if 'lista_perdidas' not in st.session_state:
            st.session_state['lista_perdidas'] = []
            
        col_add1, col_add2, col_add3 = st.columns([3, 1, 1])
        
        with col_add1:
            accesorio = st.selectbox("Agregar Componente", [
                "Ducto Recto (Pies)",
                "Codo 90° Radio Largo (n=0.30)",
                "Codo 90° Radio Corto (n=0.50)",
                "Codo 45° (n=0.18)",
                "Ampliación (n=0.55)",
                "Reducción (n=0.05)",
                "Entrada Campana (n=0.50)",
                "Filtros de Grasa (Fijo 0.50 in wg)",
                "Otras Pérdidas (Manual)"
            ])
            
        with col_add2:
            cantidad = st.number_input("Cant/Valor", 0.0, 1000.0, 1.0, step=1.0)
            
        with col_add3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕"):
                perdida = 0
                desc = ""
                
                # Lógica Coeficientes
                if "Ducto Recto" in accesorio:
                    # Darcy simplificado: f aprox 0.018 para galv
                    # HL = f * (L/D) * Pd
                    d_ft = de_ref / 12
                    perdida = (0.018 * (cantidad/d_ft)) * pd_ref
                    desc = f"Ducto Recto ({cantidad} ft)"
                elif "Codo 90° Radio Largo" in accesorio:
                    perdida = 0.30 * pd_ref * cantidad
                    desc = f"Codos 90° RL ({int(cantidad)})"
                elif "Codo 90° Radio Corto" in accesorio:
                    perdida = 0.50 * pd_ref * cantidad
                    desc = f"Codos 90° RC ({int(cantidad)})"
                elif "Codo 45°" in accesorio:
                    perdida = 0.18 * pd_ref * cantidad
                    desc = f"Codos 45° ({int(cantidad)})"
                elif "Ampliación" in accesorio:
                    perdida = 0.55 * pd_ref * cantidad
                    desc = f"Ampliaciones ({int(cantidad)})"
                elif "Reducción" in accesorio:
                    perdida = 0.05 * pd_ref * cantidad
                    desc = f"Reducciones ({int(cantidad)})"
                elif "Entrada Campana" in accesorio:
                    perdida = 0.50 * pd_ref * cantidad
                    desc = "Entrada Campana"
                elif "Filtros" in accesorio:
                    perdida = 0.50 * cantidad # Fijo por banco
                    desc = "Banco Filtros"
                elif "Otras" in accesorio:
                    perdida = cantidad
                    desc = "Pérdida Adicional"
                
                st.session_state['lista_perdidas'].append({"Concepto": desc, "Pe (in wg)": perdida})
        
        # --- TABLA Y TOTAL ---
        st.markdown("---")
        total_sp = 0
        if len(st.session_state['lista_perdidas']) > 0:
            df_loss = pd.DataFrame(st.session_state['lista_perdidas'])
            st.table(df_loss)
            total_sp = df_loss['Pe (in wg)'].sum()
            
            col_tot1, col_tot2 = st.columns([3, 1])
            with col_tot2:
                st.metric("Presión Estática Total", f"{total_sp:.3f} in wg")
            
            if st.button("💾 GUARDAR PARTIDA EN CUADRO DE EQUIPOS"):
                tag = f"VE-{st.session_state['ve_counter']:02d}"
                st.session_state['equipments'].append({
                    "tag": tag,
                    "cfm": int(st.session_state['cfm_actual']),
                    "sp": round(total_sp, 3),
                    "app": "Cocina Comercial",
                    "details": f"Vel: {int(st.session_state['vel_actual'])} FPM | De: {de_ref:.1f}\""
                })
                st.session_state['ve_counter'] += 1
                st.session_state['lista_perdidas'] = [] # Reset lista
                st.success(f"¡Equipo {tag} guardado! Puedes calcular otro.")
                
        # --- BOTÓN FINAL DE ENVÍO ---
        if len(st.session_state['equipments']) > 0:
            st.markdown("### 📤 Finalizar Proyecto")
            st.info("Revisa el cuadro de equipos en la barra lateral antes de enviar.")
            
            # Construcción del mailto
            loc = st.session_state['location_data']
            subject = f"Solicitud Cotización - {loc['ciudad']}"
            
            body = f"Hola Ing. Sotelo,%0D%0A%0D%0ARequiero cotización para el siguiente proyecto:%0D%0A%0D%0A"
            body += f"📍 UBICACIÓN:%0D%0ACiudad: {loc['ciudad']}%0D%0AAltitud: {loc['alt']} msnm%0D%0ATemp Prom: {loc['temp']}°C%0D%0A%0D%0A"
            body += "📋 CUADRO DE EQUIPOS:%0D%0A"
            
            for eq in st.session_state['equipments']:
                body += f"[{eq['tag']}] Caudal: {eq['cfm']} CFM | P.E.: {eq['sp']} in wg | App: {eq['app']}%0D%0A"
            
            body += "%0D%0A%0D%0AAtentamente,%0D%0A(Tu Nombre)"
            
            st.markdown(f"""
                <a href="mailto:ventas@csventilacion.mx?subject={subject}&body={body}" 
                   style="display: inline-block; background-color: #28a745; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; width: 100%; text-align: center;">
                   📧 ENVIAR REPORTE Y COTIZAR
                </a>
            """, unsafe_allow_html=True)
            
    else:
        st.warning("Completa los pasos 1 y 2 primero.")
