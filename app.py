import streamlit as st
import pandas as pd
import math

# --- 1. CONFIGURACIÓN ---
st.set_page_config(
    page_title="CS Ventilación",
    page_icon="🔥",
    layout="centered"
)

# --- 2. ESTILOS ---
st.markdown("""
    <style>
    .main-header {
        font-size: 28px;
        font-weight: bold;
        color: #0E4F8F;
        text-align: center;
    }
    .success-box {
        padding: 10px;
        background-color: #d4edda;
        color: #155724;
        border-radius: 5px;
    }
    .warning-box {
        padding: 10px;
        background-color: #fff3cd;
        color: #856404;
        border-radius: 5px;
    }
    .danger-box {
        padding: 10px;
        background-color: #f8d7da;
        color: #721c24;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. INICIALIZACIÓN (LÍNEAS CORTAS) ---
if 'equipments' not in st.session_state:
    st.session_state['equipments'] = []

if 've_counter' not in st.session_state:
    st.session_state['ve_counter'] = 1

if 'cfm_actual' not in st.session_state:
    st.session_state['cfm_actual'] = 0

if 'vel_actual' not in st.session_state:
    st.session_state['vel_actual'] = 0

if 'pd_state' not in st.session_state:
    st.session_state['pd_state'] = 0

if 'de_state' not in st.session_state:
    st.session_state['de_state'] = 0

if 'current_app' not in st.session_state:
    st.session_state['current_app'] = "N/A"

# --- 4. BASE DE DATOS (BLOQUES SEGUROS) ---
db_geo = {}

# Aguascalientes
db_geo["Aguascalientes"] = {
    "Aguascalientes": {"alt": 1888, "temp": 26},
    "Jesus Maria": {"alt": 1890, "temp": 26},
    "Calvillo": {"alt": 1640, "temp": 28}
}

# Baja California
db_geo["Baja California"] = {
    "Tijuana": {"alt": 20, "temp": 26},
    "Mexicali": {"alt": 8, "temp": 42},
    "Ensenada": {"alt": 10, "temp": 24}
}

# Baja California Sur
db_geo["Baja California Sur"] = {
    "La Paz": {"alt": 27, "temp": 30},
    "Cabo San Lucas": {"alt": 10, "temp": 29},
    "San Jose": {"alt": 10, "temp": 29}
}

# Campeche
db_geo["Campeche"] = {
    "Campeche": {"alt": 10, "temp": 34},
    "Cd del Carmen": {"alt": 2, "temp": 35},
    "Champoton": {"alt": 10, "temp": 34}
}

# CDMX
db_geo["Ciudad de Mexico"] = {
    "Centro": {"alt": 2240, "temp": 24},
    "Santa Fe": {"alt": 2500, "temp": 21},
    "Polanco": {"alt": 2250, "temp": 24}
}

# Coahuila
db_geo["Coahuila"] = {
    "Saltillo": {"alt": 1600, "temp": 28},
    "Torreon": {"alt": 1120, "temp": 32},
    "Monclova": {"alt": 600, "temp": 34}
}

# Jalisco
db_geo["Jalisco"] = {
    "Guadalajara": {"alt": 1566, "temp": 28},
    "Zapopan": {"alt": 1570, "temp": 28},
    "Puerto Vallarta": {"alt": 10, "temp": 32}
}

# Nuevo Leon
db_geo["Nuevo Leon"] = {
    "Monterrey": {"alt": 540, "temp": 35},
    "San Pedro": {"alt": 600, "temp": 34},
    "Apodaca": {"alt": 400, "temp": 36}
}

# Puebla
db_geo["Puebla"] = {
    "Puebla": {"alt": 2135, "temp": 25},
    "Cholula": {"alt": 2150, "temp": 25},
    "Tehuacan": {"alt": 1600, "temp": 28}
}

# Queretaro
db_geo["Queretaro"] = {
    "Queretaro": {"alt": 1820, "temp": 28},
    "San Juan": {"alt": 1920, "temp": 27},
    "El Marques": {"alt": 1900, "temp": 28}
}

# Quintana Roo
db_geo["Quintana Roo"] = {
    "Cancun": {"alt": 10, "temp": 32},
    "Playa del Carmen": {"alt": 10, "temp": 32},
    "Tulum": {"alt": 10, "temp": 32}
}

# Sinaloa
db_geo["Sinaloa"] = {
    "Culiacan": {"alt": 54, "temp": 36},
    "Mazatlan": {"alt": 10, "temp": 32},
    "Los Mochis": {"alt": 10, "temp": 35}
}

# Sonora
db_geo["Sonora"] = {
    "Hermosillo": {"alt": 210, "temp": 40},
    "Cd Obregon": {"alt": 40, "temp": 39},
    "Nogales": {"alt": 1200, "temp": 30}
}

# Veracruz
db_geo["Veracruz"] = {
    "Veracruz": {"alt": 10, "temp": 30},
    "Xalapa": {"alt": 1400, "temp": 24},
    "Coatzacoalcos": {"alt": 10, "temp": 32}
}

# Yucatan
db_geo["Yucatan"] = {
    "Merida": {"alt": 10, "temp": 36},
    "Valladolid": {"alt": 20, "temp": 34},
    "Progreso": {"alt": 0, "temp": 35}
}


# --- 5. FUNCIONES ---
def get_auto_dims(cfm, vel_target=2000):
    if cfm <= 0:
        return 6, 6
    
    area = cfm / vel_target
    
    # Circular
    d_ideal = math.sqrt(area * 4 / math.pi) * 12
    d_final = round(d_ideal / 2) * 2
    if d_final < 4: d_final = 4
    
    # Rectangular
    s_ideal = math.sqrt(area) * 12
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
    
    with st.expander("📍 Datos Proyecto", expanded=True):
        nom_proy = st.text_input("Nombre", "Ej. Restaurante")
        pais = st.selectbox("País", ["México", "Otro"])
        
        ciudad = ""
        estado = ""
        alt = 0
        temp = 25
        
        if pais == "México":
            edos = sorted(list(db_geo.keys()))
            estado = st.selectbox("Estado", edos)
            
            if estado:
                ciuds = list(db_geo[estado].keys())
                ciudad = st.selectbox("Ciudad", ciuds)
                
                if ciudad:
                    data = db_geo[estado][ciudad]
                    alt = data['alt']
                    temp = data['temp']
                    
                    c1, c2 = st.columns(2)
                    with c1: st.metric("Alt", f"{alt}m")
                    with c2: st.metric("Temp", f"{temp}C")
        else:
            ciudad = st.text_input("Ciudad")
            alt = st.number_input("Altitud", 0)
            temp = st.number_input("Temp", 25)
            
        st.session_state['proj'] = {
            "nombre": nom_proy,
            "loc": f"{ciudad}, {estado}",
            "alt": alt,
            "temp": temp
        }
    
    st.markdown("---")
    if len(st.session_state['equipments']) > 0:
        st.markdown("**Equipos:**")
        for item in st.session_state['equipments']:
            st.caption(f"🔹 {item['tag']}")
        
        if st.button("🗑️ Borrar"):
            st.session_state['equipments'] = []
            st.session_state['ve_counter'] = 1
            st.rerun()

# --- 7. MAIN ---
st.markdown('<div class="main-header">CALCULADORA COCINAS</div>', unsafe_allow_html=True)
tag_label = f"VE-{st.session_state['ve_counter']:02d}"
st.write(f"Partida Actual: **{tag_label}**")
st.markdown("---")

t1, t2, t3 = st.tabs(["1. Caudal", "2. Ductos", "3. Presión"])

# --- TAB 1 ---
with t1:
    c1, c2 = st.columns(2)
    with c1:
        L = st.number_input("Largo (m)", 0.5, 10.0, 2.0, 0.1)
        A = st.number_input("Ancho (m)", 0.5, 5.0, 1.0, 0.1)
        H = st.number_input("Distancia (m)", 0.1, 2.0, 1.0, 0.05)
    with c2:
        inst = st.selectbox("Instalación", ["Pared (3 lados)", "Isla (4 lados)", "Esquina (2 lados)"])
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
    elif "Pared" in inst: P = (2*A) + L
    else: P = A + L
    
    Q = ((P * H) * vc * 3600) / 1.699
    
    st.info(f"Velocidad: **{vc} m/s**")
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
            
        if vel < 1500:
            st.error("⚠️ BAJA VELOCIDAD (< 1500)")
        elif 1500 <= vel <= 2500:
            st.success("✅ VELOCIDAD ÓPTIMA")
        elif 2500 < vel <= 4000:
            st.warning("⚠️ ALTA VELOCIDAD (> 2500)")
        else:
            st.error("⛔ FUERA DE RANGO (> 4000)")
            
        st.session_state['vel_actual'] = vel
        st.session_state['pd_state'] = pd_val
        st.session_state['de_state'] = de
    else:
        st.info("Calcula caudal primero.")

# --- TAB 3 ---
with t3:
    vel = st.session_state['vel_actual']
    
    if vel > 0 and vel <= 4000:
        pd_ref = st.session_state['pd_state']
        de_ref = st.session_state['de_state']
        
        st.markdown(f"**Pérdidas** (Pd: {pd_ref:.3f})")
        
        if 'losses' not in st.session_state:
            st.session_state['losses'] = []
        
        c_t, c_v, c_b = st.columns([3, 2, 1])
        with c_t:
            items = ["Tramo Recto (m)", "Codo", "Entrada Campana", "Filtro", "Ampliación", "Reducción", "Otro"]
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
                    desc = f"Filtro ({val})"
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
            with c1: v = st.radio("Voltaje",
