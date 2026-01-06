import streamlit as st
import bcrypt
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --------------------------------------------------
# Configuración de la página
# --------------------------------------------------
st.set_page_config(
    page_title="SolMar",
    page_icon="▪️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# CSS para ocultar UI de Streamlit
# --------------------------------------------------
HIDE_STREAMLIT_UI = """
<style>
header[data-testid="stHeader"] {
    display: none !important;
}
div[data-testid="stToolbar"] {
    display: none !important;
}
button[kind="header"] {
    display: none !important;
}
footer {
    visibility: hidden !important;
    height: 0 !important;
}
</style>
"""
st.markdown(HIDE_STREAMLIT_UI, unsafe_allow_html=True)

# --------------------------------------------------
# Estado de sesión
# --------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None

# --------------------------------------------------
# Autenticación
# --------------------------------------------------
def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def authenticate(username: str, password: str):
    users = st.secrets["auth"]["users"]
    passwords = st.secrets["auth"]["passwords"]

    if username not in users:
        return None

    hashed = passwords.get(username)
    if not hashed:
        return None

    if not verify_password(password, hashed):
        return None

    return users[username]["role"]

# --------------------------------------------------
# Login
# --------------------------------------------------
def login():
    st.markdown("## Acceso a SolMar")

    usuarios = list(st.secrets["auth"]["users"].keys())

    with st.form("login_form"):
        user = st.selectbox("Usuario", options=usuarios)
        pwd = st.text_input("Contraseña", type="password")
        ok = st.form_submit_button("Ingresar")

        if ok:
            role = authenticate(user, pwd)

            if role:
                st.session_state.authenticated = True
                st.session_state.username = user
                st.session_state.role = role
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

# --------------------------------------------------
# Control de acceso
# --------------------------------------------------
if not st.session_state.authenticated:
    login()
    st.stop()

# --------------------------------------------------
# Conexión a Google Sheets
# --------------------------------------------------
def get_gsheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )

    client = gspread.authorize(credentials)

    sheet_id = st.secrets["google_sheets"]["sheet_id"]
    sheet = client.open_by_key(sheet_id).sheet1

    return sheet

# --------------------------------------------------
# App protegida
# --------------------------------------------------
st.success(f"Bienvenido, {st.session_state.username}")
st.write("Rol:", st.session_state.role)

st.divider()
st.subheader("Registro de actividad")

with st.form("registro_form"):
    comentario = st.text_input("Comentario")
    guardar = st.form_submit_button("Guardar registro")

    if guardar:
        if comentario.strip() == "":
            st.warning("El comentario no puede estar vacío")
        else:
            try:
                sheet = get_gsheet()
                sheet.append_row([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    st.session_state.username,
                    st.session_state.role,
                    comentario
                ])
                st.success("Registro guardado correctamente")
            except Exception as e:
                st.error(f"Error al guardar el registro: {e}")
