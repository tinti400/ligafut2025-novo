import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="LigaFut - Home", layout="centered")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ✅ Verificação de login
if "id_time" not in st.session_state or "usuario" not in st.session_state:
    st.warning("Você precisa estar logado para acessar esta página.")
    switch_page("login")  # <-- Nome legível da página Login

# Informações do usuário logado
nome_time = st.session_state.nome_time
email_usuario = st.session_state.usuario

st.title("🏆 LigaFut - Home")
st.subheader(f"Bem-vindo, {nome_time}!")
st.write(f"Técnico: {email_usuario}")
