import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta, timezone
from utils import verificar_login

st.set_page_config(page_title="Administração - Leilão", layout="wide")

# Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
verificar_login()

st.title("🎯 Administração - Leilão")

# ============================
# 🔘 Status do Leilão do Sistema
# ============================
leilao_sistema_ref = db.collection("configuracoes").document("leilao_sistema")
leilao_sistema = leilao_sistema_ref.get().to_dict() if leilao_sistema_ref.get().exists else {}

leilao_ativo = leilao_sistema.get("ativo", False)

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Status do Leilão:")
    status_cor = "🟢 Aberto" if leilao_ativo else "🔴 Fechado"
    st.markdown(f"**{status_cor}**")

with col2:
    if leilao_ativo:
        if st.button("❌ Fechar Mercado"):
            leilao_sistema_ref.update({"ativo": False})
            st.success("Leilão fechado.")
            st.rerun()
    else:
        if st.button("✅ Abrir Mercado"):
            leilao_sistema_ref.update({"ativo": True})
            st.success("Leilão aberto.")
            st.rerun()

# ================================
# 📥 Criar Novo Leilão Manualmente
# ================================
st.markdown("---")
st.subheader("📦 Criar Novo Leilão Manualmente")

posicoes = ["GL", "LD", "ZAG", "LE", "VOL", "MC", "MD", "ME", "PD", "PE", "SA", "CA"]

with st.form("form_leilao"):
    nome = st.text_input("Nome do Jogador")
    posicao = st.selectbox("Posição", posicoes)
    overall = st.number_input("Overall", min_value=50, max_value=99, step=1)
    valor = st.number_input("Valor Inicial (R$)", min_value=1_000_000, step=500_000)
    duracao = st.number_input("⏱️ Duração do Leilão (em segundos)", min_value=30, value=120, step=15)

    enviar = st.form_submit_button("🚀 Criar Leilão")

    if enviar:
        if not nome:
            st.warning("Digite o nome do jogador.")
        else:
            fim = datetime.now(timezone.utc) + timedelta(seconds=duracao)
            leilao = {
                "jogador": {
                    "nome": nome,
                    "posicao": posicao,
                    "overall": overall,
                    "valor": valor
                },
                "valor_atual": valor,
                "ativo": True,
                "fim": fim,
                "ultimo_lance": None,
                "id_time_vencedor": None
            }
            db.collection("leiloes_livres").add(leilao)
            st.success(f"Leilão criado para {nome}!")
            st.rerun()

# =======================
# 🔍 Leilões Ativos
# =======================
st.markdown("---")
st.subheader("📋 Leilões Ativos")

leiloes_ativos = db.collection("leiloes_livres").where("ativo", "==", True).stream()

tem_ativo = False
for doc in leiloes_ativos:
    tem_ativo = True
    leilao = doc.to_dict()
    fim = leilao.get("fim")

    tempo_restante = max(0, int((fim - datetime.now(timezone.utc)).total_seconds())) if fim else "?"

    col1, col2, col3 = st.columns([3, 3, 3])
    with col1:
        st.markdown(f"**Jogador:** {leilao['jogador']['nome']}")
    with col2:
        st.markdown(f"**Valor Atual:** R$ {leilao.get('valor_atual', 0):,.0f}")
    with col3:
        st.markdown(f"**Tempo restante:** {tempo_restante} seg")

if not tem_ativo:
    st.info("Nenhum leilão ativo no momento.")

# ================================
# ⏳ Últimos 5 Leilões Encerrados
# ================================
st.markdown("---")
st.subheader("⏱️ Últimos 5 Leilões Encerrados")

leiloes_encerrados = list(
    db.collection("leiloes_livres")
    .where("ativo", "==", False)
    .order_by("fim", direction=firestore.Query.DESCENDING)
    .limit(5)
    .stream()
)

for doc in leiloes_encerrados:
    dados = doc.to_dict()
    jogador = dados["jogador"]
    status = dados.get("id_time_vencedor")
    nome_time = "Sem lances"

    if status:
        time_doc = db.collection("times").document(status).get()
        if time_doc.exists:
            nome_time = f"Vendido para {time_doc.to_dict().get('nome', 'Desconhecido')}"
        cor = "🟢"
    else:
        cor = "❌"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Jogador:** {jogador['nome']}")
    with col2:
        st.markdown(f"**Valor:** R$ {dados.get('valor_atual', 0):,.0f}")
    with col3:
        st.markdown(f"**Status:** {cor} {nome_time}")


