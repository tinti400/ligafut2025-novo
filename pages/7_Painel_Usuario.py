import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

st.set_page_config(page_title="Painel do Usuário", layout="wide")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Dados do usuário logado
id_time = st.session_state.id_time
usuario = st.session_state.usuario

# Buscar quantidade de propostas recebidas com status "pendente"
propostas_ref = db.collection("propostas").where("id_time_destino", "==", id_time).stream()
qtd_pendentes = sum(1 for doc in propostas_ref if doc.to_dict().get("status") == "pendente")

# Título centralizado
st.markdown("<h1 style='text-align: center;'>⚙️ Painel do Usuário</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Escolha uma opção abaixo:</p>", unsafe_allow_html=True)

# Linha 1
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🎽 Elenco"):
        st.switch_page("pages/4_Elenco.py")
with col2:
    if st.button("💰 Mercado de Transferências"):
        st.switch_page("pages/5_Mercado_Transferencias.py")
with col3:
    if st.button("🤝 Negociações"):
        st.switch_page("pages/11_Negociacoes.py")

# Linha 2
col4, col5, col6 = st.columns(3)
with col4:
    if st.button("📊 Classificação"):
        st.switch_page("pages/3_Painel_Classificacao.py")
with col5:
    label = f"📥 Propostas Recebidas ({qtd_pendentes})" if qtd_pendentes > 0 else "📥 Propostas Recebidas"
    if st.button(label):
        st.switch_page("pages/12_Propostas_Recebidas.py")
with col6:
    if st.button("📤 Propostas Enviadas"):
        st.switch_page("pages/13_Propostas_Enviadas.py")

# Linha 3 (centralizado)
col7 = st.columns(1)[0]
with col7:
    if st.button("🏷️ Leilão"):
        st.switch_page("pages/10_Leilao_Sistema.py")
