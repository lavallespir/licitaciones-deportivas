from datetime import datetime
import requests
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Buscador de Licitaciones Deportivas", page_icon="⚽", layout="wide"
)

st.title("🎯 Detector de Licitaciones Deportivas - Mercado Público")
st.write(
    "Haz clic en el botón para consultar y filtrar las licitaciones publicadas"
    " hoy de forma automática."
)

# Ticket integrado de forma fija y segura en la aplicación
TICKET_API = "0D0F031C-DBFF-4D34-A874-4A1C954A7CB9"

# Palabras clave para filtrar artículos deportivos
PALABRAS_CLAVE = [
    "deporte",
    "deportivo",
    "implementos deportivos",
    "indumentaria",
    "balon",
    "balones",
    "futbol",
    "cancha",
    "gimnasio",
    "trofeo",
    "medalla",
    "camisetas",
    "equipamiento deportivo",
    "uniforme deportivo",
]

if st.button("🔍 Buscar Licitaciones de Hoy"):
  with st.spinner("Conectando con la API de Mercado Público y filtrando..."):
    # Obtener fecha actual en formato ddmmaaaa requerido por la API
    fecha_hoy = datetime.now().strftime("%d%m%Y")
    url = f"https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json?fecha={fecha_hoy}&ticket={TICKET_API}"

    try:
      response = requests.get(url)
      if response.status_code == 401:
        st.error(
            "El ticket integrado no es válido o ha expirado. (Código 401)"
        )
      elif response.status_code == 200:
        data = response.json()
        licitaciones = data.get("Listado", [])

        encontradas = []
        for lic in licitaciones:
          nombre = lic.get("Nombre", "").lower()
          descripcion = lic.get("Descripcion", "").lower()
          texto_completo = nombre + " " + descripcion

          # Validar si contiene alguna palabra clave deportiva
          if any(palabra in texto_completo for palabra in PALABRAS_CLAVE):
            codigo = lic.get("CodigoExterno")
            comprador = lic.get("Comprador", {}).get(
                "NombreOrganismo", "Desconocido"
            )
            fecha_cierre = lic.get("FechaCierre")

            encontradas.append({
                "Código": codigo,
                "Nombre": lic.get("Nombre"),
                "Organismo": comprador,
                "Cierre": fecha_cierre,
            })

        if encontradas:
          st.success(
              f"¡Se encontraron {len(encontradas)} licitaciones de artículos"
              " deportivos para hoy!"
          )

          # Enlace directo al buscador general de Mercado Público
          st.markdown(
              "🔗 [Abrir el Buscador General de Mercado"
              " Público](https://www.mercadopublico.cl/Home/Busqueda)"
          )

          # Mostrar cada licitación junto con su código claramente visible
          for item in encontradas:
            with st.container(border=True):
              st.subheader(item["Nombre"])
              st.write(
                  f"**Institución:** {item['Organismo']} | **Cierre:**"
                  f" {item['Cierre']}"
              )
              st.info(f"📋 **Código de Licitación:** `{item['Código']}`")
              st.write(
                  "*(Copia este código y pégalo en el buscador de Mercado"
                  " Público para ver su ficha oficial sin errores)*"
              )
        else:
          st.info(
              "No se encontraron licitaciones con términos deportivos para la"
              " fecha de hoy."
          )
      else:
        st.error(f"Error al consultar la API. Código: {response.status_code}")
    except Exception as e:
      st.error(f"Ocurrió un error de conexión: {e}")
