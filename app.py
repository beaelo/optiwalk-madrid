import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(
    page_title="OptiWalk Madrid",
    page_icon="🚶",
    layout="wide"
)

st.title("🚶 OptiWalk Madrid")
st.subheader("Encuentra un paseo adaptado a tus preferencias")

st.write(
    "Prototipo de una herramienta que combina sombra, zonas verdes, "
    "pendientes y calidad ambiental para recomendar paseos urbanos."
)

st.divider()

col_izquierda, col_derecha = st.columns([1, 2])

with col_izquierda:
    st.header("Configura tu paseo")

    origen = st.selectbox(
        "¿Dónde quieres empezar?",
        [
            "Plaza de España",
            "Atocha",
            "Moncloa",
            "Retiro",
            "Chamartín"
        ]
    )

    duracion = st.slider(
        "¿Cuánto tiempo quieres caminar?",
        min_value=15,
        max_value=90,
        value=40,
        step=5
    )

    st.write("¿Qué quieres priorizar?")

    prioridad_sombra = st.checkbox("🌳 Sombra", value=True)
    prioridad_parques = st.checkbox("🌿 Zonas verdes", value=True)
    prioridad_pendiente = st.checkbox("♿ Poca pendiente", value=False)
    prioridad_aire = st.checkbox("🌬️ Buena calidad del aire", value=False)
    prioridad_servicios = st.checkbox("💧 Fuentes y bancos", value=False)

    calcular = st.button(
        "Calcular paseos",
        type="primary",
        use_container_width=True
    )

with col_derecha:
    st.header("Mapa de rutas")

    rutas = pd.DataFrame(
        {
            "ruta": [
                "Ruta más fresca",
                "Ruta más accesible",
                "Ruta más rápida"
            ],
            "latitud": [40.4205, 40.4168, 40.4230],
            "longitud": [-3.7140, -3.7038, -3.7095],
            "color": [
                [40, 167, 69],
                [0, 123, 255],
                [255, 145, 0]
            ]
        }
    )

    capa = pdk.Layer(
        "ScatterplotLayer",
        data=rutas,
        get_position="[longitud, latitud]",
        get_fill_color="color",
        get_radius=90,
        pickable=True
    )

    vista = pdk.ViewState(
        latitude=40.418,
        longitude=-3.708,
        zoom=12.5
    )

    mapa = pdk.Deck(
        layers=[capa],
        initial_view_state=vista,
        tooltip={"text": "{ruta}"}
    )

    st.pydeck_chart(mapa)

if calcular:
    st.success(
        f"Hemos calculado opciones de aproximadamente {duracion} minutos "
        f"desde {origen}."
    )

    puntuacion_sombra = 82 if prioridad_sombra else 65
    puntuacion_parques = 86 if prioridad_parques else 68
    puntuacion_pendiente = 88 if prioridad_pendiente else 70
    puntuacion_aire = 84 if prioridad_aire else 69
    puntuacion_servicios = 80 if prioridad_servicios else 67

    resultados = pd.DataFrame(
        {
            "Ruta": [
                "Ruta más fresca",
                "Ruta más accesible",
                "Ruta más rápida"
            ],
            "Duración": [
                f"{duracion + 2} min",
                f"{duracion + 7} min",
                f"{max(duracion - 8, 10)} min"
            ],
            "Sombra": [
                f"{puntuacion_sombra} %",
                "61 %",
                "38 %"
            ],
            "Pendiente máxima": [
                "4 %",
                f"{puntuacion_pendiente // 20} %",
                "8 %"
            ],
            "Zonas verdes": [
                "Alta",
                "Media",
                "Baja"
            ],
            "Puntuación": [
                86,
                81,
                68
            ]
        }
    )

    st.header("Paseos recomendados")
    st.dataframe(
        resultados,
        hide_index=True,
        use_container_width=True
    )

    st.info(
        "La ruta más fresca prioriza la sombra y las zonas verdes. "
        "La ruta más accesible reduce las pendientes. "
        "La ruta más rápida minimiza el tiempo de recorrido."
    )

st.divider()

st.caption(
    "Prototipo inicial de OptiWalk Madrid · Datos simulados para demostración"
)