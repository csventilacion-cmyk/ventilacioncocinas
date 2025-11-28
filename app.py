import streamlit as st
import pandas as pd
import math

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Calculadora CS Ventilación",
    page_icon="❄️",
    layout="centered"
)

# --- ESTILOS VISUALES (CS BRANDING) ---
st.markdown("""
    <style>
    .main-header {
        font-size: 30px;
        font-weight: bold;
        color: #0E4F8F; /* Azul S&P/Industrial */
        text-align: center;
    }
    .sub-header {
        font-size: 20px;
        color: #444;
        margin-bottom: 20px;
    }
    .success-box {
        padding: 15px;
        background-color: #D4EDDA;
        color: #155724;
        border-radius: 5px;
        border: 1px solid #C3E6CB;
    }
    .warning-box {
        padding: 15px;
        background-color: #F8D7DA;
        color: #721C24;
        border-radius: 5px;
        border: 1px solid #F5C6CB;
    }
    </style>
""", unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown('<div class="main-header">CS SISTEMAS DE AIRE</div>', unsafe_allow_html=True)
st.markdown('<div class="main-header" style="font-size: 20px; color: #666;">Ingeniería Aplicada & Suministro S&P</div>', unsafe_allow_html=True)
st.markdown("---")

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.header("🛠️ Herramientas")
    st.info("Esta herramienta sigue la metodología del **Manual Práctico de Diseño V3.1** de CS Ventilación y normativa **ASHRAE 154**.")
    st.write("---")
    st.write("**Contacto Comercial:**")
    st.write("📧 ventas@csventilacion.mx")
    st.write("📍 Culiacán, Sinaloa")
    st.write("---")
    st.caption("v1.0 - Validación Piloto")

# --- FUNCIONES DE CÁLCULO ---
def get_ashrae_factor(hood_type, duty_type):
    # Factores aproximados CFM/ft lineal según ASHRAE 154
    factors = {
        "Pared (Wall-mounted)": {"Light Duty": 200, "Medium Duty": 300, "Heavy Duty": 400, "Extra Heavy Duty": 550},
        "Isla (Single Island)": {"Light Duty": 400, "Medium Duty": 500, "Heavy Duty": 600, "Extra Heavy Duty": 700},
        "Isla Doble (Double Island)": {"Light Duty": 250, "Medium Duty": 300, "Heavy Duty": 400, "Extra Heavy Duty": 550}
    }
    return factors.get(hood_type, {}).get(duty_type, 0)

def calc_equivalent_diameter(a, b):
    # De = 1.3 * ((a*b)^0.625) / ((a+b)^0.25) -> Fórmula aproximada Huebscher
    # Usaremos la fórmula del manual S&P simplificada o diámetro hidráulico para cálculos rápidos
    # Manual Pag 27: De = 1.265 * ((a*b^3)/(a+b))^0.2 ... La fórmula exacta es compleja, usaremos diámetro equivalente por área para simplificar en esta demo o la fórmula de Huebscher
    if a == 0 or b == 0: return 0
    return 1.3 * ((a * b)**0.625) / ((a + b)**0.25)

# --- PESTAÑAS PRINCIPALES ---
tab1, tab2, tab3 = st.tabs(["🔥 1. Cálculo de Campana", "💨 2. Ductos y Velocidad", "📉 3. Pérdida de Carga"])

# --- TAB 1: CÁLCULO DE CAMPANA (ASHRAE 154) ---
with tab1:
    st.header("Selección de Caudal (Q)")
    
    col1, col2 = st.columns(2)
    with col1:
        hood_type = st.selectbox("Tipo de Campana", ["Pared (Wall-mounted)", "Isla (Single Island)", "Isla Doble (Double Island)"])
        length_ft = st.number_input("Longitud de Campana (pies)", min_value=1.0, value=10.0, step=0.5)
    
    with col2:
        duty_type = st.selectbox("Tipo de Cocción (Carga)", 
                                 ["Light Duty (Hornos, Vapor)", 
                                  "Medium Duty (Planchas, Estufas)", 
                                  "Heavy Duty (Parrillas gas, Carbón)", 
                                  "Extra Heavy Duty (Wok, Leña sólida)"])
        
        # Mapeo simple para limpiar el string
        duty_clean = duty_type.split(" (")[0]
        
    factor = get_ashrae_factor(hood_type, duty_clean)
    cfm_required = length_ft * factor
    
    st.metric(label="Caudal Requerido (Q)", value=f"{int(cfm_required)} CFM", delta=f"Factor: {factor} CFM/ft")
    
    if st.button("Usar este Caudal para Ductos"):
        st.session_state['cfm_global'] = cfm_required
        st.success("¡Caudal guardado! Ve a la pestaña 2.")

# --- TAB 2: DIMENSIONAMIENTO Y SEMÁFORO ---
with tab2:
    st.header("Diseño de Conducto")
    
    # Recuperar valor de Tab 1 si existe
    default_cfm = st.session_state.get('cfm_global', 5000.0)
    cfm_input = st.number_input("Caudal de Aire (CFM)", value=float(default_cfm))
    
    shape = st.radio("Forma del Ducto", ["Rectangular", "Circular"], horizontal=True)
    
    area_sqft = 0
    
    if shape == "Rectangular":
        c1, c2 = st.columns(2)
        with c1: width = st.number_input("Ancho (pulgadas)", min_value=1.0, value=20.0)
        with c2: height = st.number_input("Alto (pulgadas)", min_value=1.0, value=20.0)
        area_sqft = (width * height) / 144
        diameter_eq = calc_equivalent_diameter(width, height)
        st.caption(f"Diámetro Equivalente aprox: {diameter_eq:.1f} pulgadas")
        
    else:
        diameter = st.number_input("Diámetro (pulgadas)", min_value=1.0, value=24.0)
        area_sqft = (math.pi * (diameter/12)**2) / 4
        diameter_eq = diameter

    # Cálculo de Velocidad
    if area_sqft > 0:
        velocity = cfm_input / area_sqft
    else:
        velocity = 0
        
    st.metric("Velocidad Resultante", f"{int(velocity)} FPM")
    
    # --- EL SEMÁFORO (VALIDACIÓN NORMATIVA) ---
    st.subheader("Validación Técnica (Manual CS):")
    if 1500 <= velocity <= 3000:
        st.markdown(f"""
        <div class="success-box">
            ✅ <strong>VELOCIDAD ÓPTIMA</strong><br>
            La velocidad está dentro del rango seguro para transporte de grasa (1500-3000 FPM).
            <br>Cumple con criterios de autolimpieza y seguridad.
        </div>
        """, unsafe_allow_html=True)
    elif velocity < 1500:
        st.markdown(f"""
        <div class="warning-box">
            ⚠️ <strong>VELOCIDAD BAJA (RIESGO)</strong><br>
            Velocidad menor a 1500 FPM. <br>
            <strong>Riesgo:</strong> Acumulación de grasa en ductos y peligro de incendio grave. 
            Reduzca el tamaño del ducto.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="warning-box">
            ⚠️ <strong>VELOCIDAD ALTA (RUIDO)</strong><br>
            Velocidad mayor a 3000 FPM. <br>
            <strong>Riesgo:</strong> Ruido excesivo y alto consumo energético. Aumente el tamaño del ducto.
        </div>
        """, unsafe_allow_html=True)
        
    st.session_state['velocity_global'] = velocity
    st.session_state['diameter_global'] = diameter_eq

# --- TAB 3: PÉRDIDA DE CARGA (SIMPLIFICADA) ---
with tab3:
    st.header("Estimación de Caída de Presión (Pe)")
    
    vel = st.session_state.get('velocity_global', 0)
    
    if vel > 0:
        # Presión Dinámica (Formula: (V/4005)^2)
        pd_val = (vel / 4005) ** 2
        st.write(f"**Presión Dinámica (Pd):** {pd_val:.3f} in wg (Base para cálculo de accesorios)")
        
        # --- LISTA DE MATERIALES ---
        st.subheader("Agregar Tramos y Accesorios")
        
        # Inicializar lista en sesión
        if 'items' not in st.session_state:
            st.session_state['items'] = []
            
        c_type, c_val = st.columns([2,1])
        with c_type:
            item_type = st.selectbox("Elemento", 
                                     ["Tramo Recto (10 ft)", 
                                      "Codo 90° (n=0.30)", 
                                      "Codo 45° (n=0.18)", 
                                      "Entrada Campana (n=0.50)",
                                      "Filtros de Grasa (Estándar 0.50)"])
        with c_val:
            qty = st.number_input("Cantidad/Longitud", min_value=1, value=1)
            
        if st.button("Agregar a la lista"):
            pe_calc = 0
            description = ""
            
            # Lógica simplificada de cálculo (coeficientes aproximados Manual CS)
            if "Tramo Recto" in item_type:
                # Darcy aproximado para ducto galv estándar
                # Pe = (0.02 * L/D) * Pd  <- Simplificación visual para la app
                d_ft = st.session_state.get('diameter_global', 20) / 12
                # Factor fricción aprox 0.015 manual
                loss = (0.015 * (qty*10) / d_ft) * pd_val 
                pe_calc = loss
                description = f"Ducto Recto ({qty*10} ft)"
            
            elif "Codo 90" in item_type:
                pe_calc = 0.30 * pd_val * qty
                description = f"Codos 90° ({qty} pzas)"
                
            elif "Codo 45" in item_type:
                pe_calc = 0.18 * pd_val * qty
                description = f"Codos 45° ({qty} pzas)"
            
            elif "Entrada Campana" in item_type:
                pe_calc = 0.50 * pd_val * qty # Aprox n=0.5
                description = f"Pérdida Entrada ({qty} pzas)"
                
            elif "Filtros" in item_type:
                pe_calc = 0.50 * qty # Valor fijo típico pulgadas
                description = f"Banco Filtros ({qty} pzas)"
            
            st.session_state['items'].append({"Desc": description, "Pe": pe_calc})
            
        # --- TABLA DE RESUMEN ---
        total_pe = 0
        if len(st.session_state['items']) > 0:
            df = pd.DataFrame(st.session_state['items'])
            st.table(df)
            total_pe = df['Pe'].sum()
            
            st.metric("Caída de Presión Total (ESP)", f"{total_pe:.3f} in wg")
            
            # --- GENERADOR DE PEDIDO ---
            st.markdown("### 🚀 ¿Listo para cotizar?")
            st.info(f"Has calculado un sistema para **{int(cfm_input)} CFM** con **{total_pe:.3f} in wg** de presión.")
            
            subject = f"Cotización Proyecto: {int(cfm_input)} CFM"
            body = f"Hola Ing. Sotelo,%0D%0A%0D%0AEtoy diseñando un sistema con los siguientes datos:%0D%0A- Caudal: {int(cfm_input)} CFM%0D%0A- Presión Estática: {total_pe:.3f} in wg%0D%0A- Aplicación: Cocina Comercial%0D%0A%0D%0A¿Me ayudas a seleccionar el equipo S&P adecuado y validar mi cálculo?"
            
            st.markdown(f"""
                <a href="mailto:ventas@csventilacion.mx?subject={subject}&body={body}" 
                   style="background-color: #0E4F8F; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                   📧 ENVIAR A COTIZAR AHORA
                </a>
            """, unsafe_allow_html=True)
            
            if st.button("Borrar Lista"):
                st.session_state['items'] = []
                st.rerun()
                
    else:
        st.warning("Primero calcula la velocidad en la Pestaña 2.")

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("© 2025 CS Sistemas de Aire - Desarrollado para uso exclusivo de nuestros socios comerciales.")
