import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase se ainda não estiver inicializado
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("📋 Cadastro de Usuário")

nome = st.text_input("Nome")
email = st.text_input("E-mail")
senha = st.text_input("Senha", type="password")

if st.button("Cadastrar"):
    if not nome or not email or not senha:
        st.warning("Preencha todos os campos!")
    else:
        usuarios_ref = db.collection("usuarios")
        # Verificar se e-mail já existe
        docs = usuarios_ref.where("email", "==", email).stream()
        if any(docs):
            st.error("E-mail já cadastrado!")
        else:
            usuarios_ref.add({
                "nome": nome,
                "email": email,
                "senha": senha  # Aqui você pode futuramente criptografar a senha
            })
            st.success("Usuário cadastrado com sucesso!")
