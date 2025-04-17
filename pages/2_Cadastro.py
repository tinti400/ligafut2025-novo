import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import uuid

st.set_page_config(page_title="Cadastro de Usuário", layout="wide")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.title("📝 Cadastro de Usuário")

usuario = st.text_input("Usuário (E-mail)").strip().lower()
senha = st.text_input("Senha", type="password")

if st.button("Cadastrar"):
    if usuario and senha:
        usuarios_ref = db.collection("usuarios")

        docs = usuarios_ref.where("usuario", "==", usuario).stream()
        usuario_existente = False
        for doc in docs:
            usuario_existente = True

        if usuario_existente:
            st.warning("Este usuário já está cadastrado.")
        else:
            novo_id = str(uuid.uuid4())
            usuarios_ref.document(novo_id).set({
                "usuario": usuario,
                "senha": senha
            })
            st.success("Usuário cadastrado com sucesso!")
    else:
        st.warning("Preencha todos os campos para se cadastrar.")
