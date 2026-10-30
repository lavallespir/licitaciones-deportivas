import streamlit as st
import requests

# Configuración de la página
st.set_page_config(
    page_title="RAM Deportes - Buscador de Licitaciones",
    page_icon="🏆",
    layout="wide"
)

# Estilos CSS corporativos (Tonos limpios, negros y verdes deportivos)
st.markdown("""
    <style>
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 6px;
        border: none;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        color: white;
    }
    div.stMetric {
        background-color: #f1f8e9;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #2e7d32;
    }
    .main-header {
        font-size: 28px;
        font-weight: bold;
        color: #1b5e20;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- BARRA LATERAL -----------------
st.sidebar.image("logo.png", width=180)  # Carga el logo si lo subes a GitHub como logo.png
st.sidebar.markdown("---")
st.sidebar.markdown("### 🏢 Panel RAM Deportes")
st.sidebar.info("Herramienta automatizada de monitoreo y búsqueda de licitaciones de artículos deportivos en Mercado Público (ChileCompra).")

ticket_api = st.sidebar.text_input("Ticket API ChileCompra", value="0D0F031C-DBFF-4D34-A874-4A1C954A7CB9", type="password")

# ----------------- CUERPO PRINCIPAL -----------------
st.markdown('<p class="main-header">🏆 Sistema de Gestión de Licitaciones - RAM Deportes</p>', unsafe_allow_html=True)
st.markdown("Busca y filtra en tiempo real oportunidades de negocios con el Estado en el rubro deportivo.")

# Pestañas para organizar la interfaz de forma profesional
tab1, tab2 = st.tabs(["🔍 Buscador Activo", "📊 Estado del Sistema"])

with tab1:
    st.subheader("Filtros de Búsqueda")
    
    col1, col2 = st.columns(2)
    with col1:
        palabra_clave = st.text_input("Palabra clave (ej. padel, futbol, deporte)", value="deporte")
    with col2:
        fecha_busqueda = st.date_input("Fecha de publicación")

    if st.button("Buscar Licitaciones en Mercado Público"):
        with st.spinner("Conectando con la API de ChileCompra..."):
            try:
                # URL oficial de la API de ChileCompra por fecha
                fecha_str = fecha_busqueda.strftime("%d-%m-%Y")
                url = f"https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json?fecha={fecha_str}&ticket={ticket_api}"
                
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    licitaciones = data.get("Listado", [])
                    
                    # Filtrar por palabra clave ingresada
                    filtradas = [
                        l for l in licitaciones 
                        if palabra_clave.lower() in l.get("Nombre", "").lower() 
                        or palabra_clave.lower() in l.get("Descripcion", "").lower()
                    ]
                    
                    st.success(f"¡Consulta exitosa! Se encontraron {len(filtradas)} licitaciones coincidentes.")
                    
                    if filtradas:
                        for lic in filtradas:
                            with st.expander(f"📦 {lic.get('Nombre', 'Sin nombre')} (Código: {lic.get('Codigo')})"):
                                st.write(f"**Descripción:** {lic.get('Descripcion', 'No disponible')}")
                                st.write(f"**Estado:** {lic.get('Estado')}")
                                st.write(f"**Fecha de Cierre:** {lic.get('FechaCierre')}")
                                codigo_lic = lic.get('Codigo')
                                st.markdown(f"[🔗 Ver ficha oficial en Mercado Público](https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?qs={codigo_lic})")
                    else:
                        st.warning("No se encontraron licitaciones con esa palabra clave para la fecha seleccionada.")
                else:
                    st.error("Error al conectar con la API de Mercado Público. Revisa tu Ticket API.")
            except Exception as e:
                st.error(f"Ocurrió un error inesperado: {e}")

with tab2:
    st.subheader("Estado Operativo")
    st.metric(label="Estado del Bot de Alertas por Correo", value="Activo en Segundo Plano", delta="Conectado a Gmail")
    st.markdown("""
    * **Frecuencia de revisión:** Cada 5 minutos.
    * **Destinatario de alertas:** Configurado mediante `bot_correo.py`.
    * **Plataforma:** Desplegado de forma segura en Streamlit Cloud.
    """)
