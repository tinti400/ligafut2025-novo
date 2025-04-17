import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("🔐 Login")

email = st.text_input("E-mail")
senha = st.text_input("Senha", type="password")

if st.button("Entrar"):
    usuarios_ref = db.collection("usuarios")
    query = usuarios_ref.where("email", "==", email).where("senha", "==", senha).stream()

    usuario_encontrado = None
    for doc in query:
        usuario_encontrado = doc.to_dict()

    if usuario_encontrado:
        st.success(f"Bem-vindo, {usuario_encontrado['nome']}!")
        st.page_link("painel_classificacao.py", label="Ir para o Painel", icon="🏆")
    else:
        st.error("E-mail ou senha inválidos!")
