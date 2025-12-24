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
# Generador de hash (USO ADMINISTRATIVO)
# --------------------------------------------------
def generate_hash(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

st.markdown("### 🔐 Generador de hash (uso administrativo)")
with st.form("hash_generator"):
    raw_password = st.text_input("Contraseña a hashear", type="password")
    submit = st.form_submit_button("Generar hash")

    if submit and raw_password:
        st.code(generate_hash(raw_password), language="text")
        st.info("Copia este hash y pégalo en Streamlit → Settings → Secrets")

st.divider()

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
# App protegida (temporal)
# --------------------------------------------------
st.success(f"Bienvenido, {st.session_state.username}")
st.write("Rol:", st.session_state.role)
