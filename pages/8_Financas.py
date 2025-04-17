# 8_Financas.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from utils import verificar_login

st.set_page_config(page_title="Financeiro", layout="wide")

# Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

verificar_login()

id_time = st.session_state.id_time
nome_time = st.session_state.nome_time

st.title("💰 Painel Financeiro")
st.markdown(f"### 📊 Time: **{nome_time}**")

movimentacoes_ref = db.collection("movimentacoes").where("id_time", "==", id_time).order_by("data", direction=firestore.Query.DESCENDING)
movimentacoes = [doc.to_dict() for doc in movimentacoes_ref.stream()]

if not movimentacoes:
    st.info("Nenhuma movimentação encontrada.")
else:
    st.markdown("""
        <style>
            .tabela-financas {
                background-color: #f0f2f6;
                border-radius: 10px;
                padding: 10px;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    for mov in movimentacoes:
        tipo = mov.get("tipo", "-")
        jogador = mov.get("jogador", "-")
        valor = mov.get("valor", 0)
        data = mov.get("data")
        if isinstance(data, datetime):
            data_str = data.strftime("%d/%m/%Y %H:%M")
        else:
            data_str = "-"

        col1, col2, col3, col4 = st.columns([3, 3, 2, 2])
        with col1:
            st.markdown(f"<div class='tabela-financas'><b>Tipo:</b> {tipo.replace('_', ' ').title()}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='tabela-financas'><b>Jogador:</b> {jogador}</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='tabela-financas'><b>Valor:</b> R$ {valor:,.0f}</div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='tabela-financas'><b>Data:</b> {data_str}</div>", unsafe_allow_html=True)
