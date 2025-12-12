import streamlit as st
import bcrypt

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
# CSS para ocultar UI de Streamlit (permitido)
# --------------------------------------------------
HIDE_STREAMLIT_UI = """
<style>
    header[data-testid="stHeader"] { display: none !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    button[kind="header"] { display: none !important; }
    footer { visibility: hidden !important; height: 0 !important; }
</style>
"""
st.markdown(HIDE_STREAMLIT_UI, unsafe_allow_html=True)

# --------------------------------------------------
# Inicializar Session State
# --------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None

# --------------------------------------------------
# UTILIDAD: generar hash bcrypt (ADMIN TEMPORAL)
# --------------------------------------------------
def generate_hash(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

# --------------------------------------------------
# PANEL TEMPORAL PARA GENERAR HASHES
# --------------------------------------------------
st.markdown("### 🔐 Generador de hash (uso administrativo)")

with st.form("hash_generator"):
    raw_password = st.text_input("Contraseña a hashear", type="password")
    generate = st.form_submit_button("Generar hash")

    if generate and raw_password:
        hash_result = generate_hash(raw_password)
        st.code(hash_result, language="text")
        st.info("Copia este hash y pégalo en Streamlit → Settings → Secrets")

st.divider()

# --------------------------------------------------
# Funciones de autenticación
# --------------------------------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

def authenticate(username: str, password: str) -> bool:
    users = st.secrets["auth"]["users"]
    passwords = st.secrets["auth"]["passwords"]

    if username not in users:
        return False

    stored_hash = passwords.get(username)
    if not stored_hash:
        return False

    return verify_password(password, stored_hash)

# --------------------------------------------------
# Login
# --------------------------------------------------
def login_screen():
    st.markdown("## Acceso a SolMar")

    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Ingresar")

        if submit:
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

# --------------------------------------------------
# Logout
# --------------------------------------------------
def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.rerun()

# --------------------------------------------------
# Control de acceso
# --------------------------------------------------
if not st.session_state.authenticated:
    login_screen()
    st.stop()

# --------------------------------------------------
# APP PROTEGIDA
# --------------------------------------------------
st.success(f"Bienvenido, {st.session_state.username}")

if st.button("Cerrar sesión"):
    logout()

st.write("Aplicación protegida en construcción.")
