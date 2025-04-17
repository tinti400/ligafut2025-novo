import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from utils import verificar_login

st.set_page_config(page_title="Admin Mercado de Transferências", layout="wide")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Verificar login
verificar_login()

st.title("⚙️ Administração do Mercado de Transferências")

# 🔁 Verificar status do mercado
mercado_ref = db.collection("configuracoes").document("mercado")
mercado_doc = mercado_ref.get()
mercado_aberto = mercado_doc.to_dict().get("aberto", False) if mercado_doc.exists else False

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🏪 Status do Mercado:")
    st.markdown(f"🔵 **{'Aberto' if mercado_aberto else 'Fechado'}**")

with col2:
    if mercado_aberto:
        if st.button("❌ Fechar Mercado"):
            mercado_ref.set({"aberto": False})
            st.success("🔒 Mercado fechado com sucesso!")
            st.rerun()
    else:
        if st.button("✅ Abrir Mercado"):
            mercado_ref.set({"aberto": True})
            st.success("🔓 Mercado aberto com sucesso!")
            st.rerun()

st.markdown("---")
st.subheader("📥 Cadastrar Jogador Manualmente no Mercado")

# Lista de posições disponíveis
posicoes = ["GL", "LD", "ZAG", "LE", "VOL", "MC", "MD", "ME", "PD", "PE", "SA", "CA"]

# Formulário de cadastro manual
with st.form("form_cadastro_jogador"):
    nome = st.text_input("Nome do Jogador")
    posicao = st.selectbox("Posição", posicoes)
    overall = st.number_input("Overall", min_value=50, max_value=99, step=1)
    valor = st.number_input("Valor do Jogador (R$)", min_value=1_000_000, step=500_000)

    enviar = st.form_submit_button("Cadastrar Jogador")

    if enviar:
        if nome:
            jogador = {
                "nome": nome,
                "posicao": posicao,
                "overall": overall,
                "valor": valor
            }
            db.collection("mercado_transferencias").add(jogador)
            st.success(f"Jogador {nome} cadastrado com sucesso no mercado!")
            st.rerun()
        else:
            st.warning("Preencha o nome do jogador.")

st.markdown("---")
st.subheader("📋 Jogadores Disponíveis no Mercado")

mercado_ref = db.collection("mercado_transferencias").stream()
mercado = [doc.to_dict() | {"id_doc": doc.id} for doc in mercado_ref]

if not mercado:
    st.info("Nenhum jogador disponível no mercado.")
else:
    for jogador in mercado:
        nome = jogador.get("nome", "Sem nome")
        posicao = jogador.get("posicao", "Desconhecida")
        overall = jogador.get("overall", "N/A")
        valor = jogador.get("valor", 0)
        id_jogador = jogador.get("id_doc")

        col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 2, 1])
        with col1:
            st.write(f"**{nome}**")
        with col2:
            st.write(f"{posicao}")
        with col3:
            st.write(f"{overall}")
        with col4:
            st.write(f"R$ {valor:,.0f}")
        with col5:
            if st.button("🗑️ Excluir", key=f"excluir_{id_jogador}"):
                db.collection("mercado_transferencias").document(id_jogador).delete()
                st.warning(f"Jogador {nome} removido do mercado.")
                st.rerun()
