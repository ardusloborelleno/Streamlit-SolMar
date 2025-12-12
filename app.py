import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="SolMar",
    page_icon="▪️",  # puedes eliminar el icono si prefieres algo más formal
    layout="wide"
)

# Ocultar elementos de Streamlit (barra superior, menú, manage app)
hide_streamlit_style = """
    <style>
        /* Ocultar menú superior derecho: Share, GitHub, Options */
        header[data-testid="stHeader"] {
            display: none !important;
        }

        /* Ocultar hamburger menu (≡) en modo viewer */
        button[kind="header"] {
            display: none !important;
        }

        /* Ocultar footer "Manage App" */
        footer {
            visibility: hidden !important;
        }
        footer:after {
            content:'' !important;
            visibility:hidden !important;
        }

        /* Ocultar barra inferior por si aparece en modo editor */
        div[data-testid="stStatusWidget"] {
            display: none !important;
        }

        /* Ocultar toolbar de la esquina superior derecha */
        div[data-testid="stToolbar"] {
            display: none !important;
        }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

