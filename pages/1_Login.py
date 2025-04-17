import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from google.oauth2 import service_account

st.set_page_config(page_title="Login - LigaFut", page_icon="⚽", layout="centered")

# 🔐 Inicialização segura do Firebase com secrets
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["firebase"])
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 🔓 Interface de login
st.markdown("<h1 style='text-align: center; color: white;'>🔐 Login - LigaFut</h1><br>", unsafe_allow_html=True)

with st.form("login_form"):
    usuario_input = st.text_input("Usuário (e-mail)")
    senha_input = st.text_input("Senha", type="password")
    botao_login = st.form_submit_button("Entrar")

# 🔍 Verifica credenciais
if botao_login:
    if usuario_input and senha_input:
        try:
            usuarios_ref = db.collection("usuarios").where("usuario", "==", usuario_input).stream()
            usuario_encontrado = None
            usuario_doc_id = None

            for doc in usuarios_ref:
                dados = doc.to_dict()
                if dados.get("senha") == senha_input:
                    usuario_encontrado = dados
                    usuario_doc_id = doc.id
                    break

            if usuario_encontrado:
                # Verificação se dados de time estão completos
                if "id_time" not in usuario_encontrado or "nome_time" not in usuario_encontrado:
                    st.error("❌ O cadastro do usuário está incompleto. Faltam dados do time.")
                    st.stop()

                # Salva dados na sessão
                st.session_state["usuario_id"] = usuario_doc_id
                st.session_state["usuario_logado"] = usuario_encontrado["usuario"]
                st.session_state["id_time"] = usuario_encontrado["id_time"]
                st.session_state["nome_time"] = usuario_encontrado["nome_time"]

                st.success("✅ Login realizado com sucesso!")
                st.markdown("🔄 Vá até o menu lateral e clique em **4_Elenco** para continuar.")
                st.stop()
            else:
                st.error("❌ Usuário ou senha incorretos.")
        except Exception as e:
            st.error(f"Erro ao conectar com o Firebase: {e}")
    else:
        st.warning("Preencha todos os campos para fazer login.")
