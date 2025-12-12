import streamlit as st

# --------------------------------------------------
# Configuración inicial de la página
# --------------------------------------------------
st.set_page_config(
    page_title="SolMar",
    page_icon="▪️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# CSS para ocultar elementos visuales de Streamlit
# (solo lo que es posible en Streamlit Cloud Free)
# --------------------------------------------------
HIDE_STREAMLIT_UI = """
<style>

    /* Ocultar barra superior (Share, GitHub, Options) */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* Ocultar toolbar superior derecha */
    div[data-testid="stToolbar"] {
        display: none !important;
    }

    /* Ocultar menú hamburguesa */
    button[kind="header"] {
        display: none !important;
    }

    /* Ocultar footer interno de Streamlit */
    footer {
        visibility: hidden !important;
        height: 0 !important;
    }

    /* Evitar espacio residual */
    .block-container {
        padding-top: 1rem !important;
    }

</style>
"""

st.markdown(HIDE_STREAMLIT_UI, unsafe_allow_html=True)

# --------------------------------------------------
# Hoja en blanco (intencional)
# --------------------------------------------------
# No se renderiza ningún contenido.
# Aquí comenzará el desarrollo futuro de SolMar.

