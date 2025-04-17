import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from utils import verificar_login, registrar_movimentacao

st.set_page_config(page_title="Mercado de Transferências", layout="wide")

# Inicializa Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Verifica login
verificar_login()

# Info do time logado
id_time = st.session_state.id_time
nome_time = st.session_state.nome_time

st.title("💰 Mercado de Transferências")
st.markdown(f"### Time: `{nome_time}`")

# Buscar jogadores no mercado
mercado_ref = db.collection("mercado_transferencias").stream()
mercado = [doc.to_dict() | {"id_doc": doc.id} for doc in mercado_ref]

# Organizar por posição
ordem_posicoes = {
    "GL": 0, "LD": 1, "ZAG": 2, "LE": 3, "VOL": 4, "MC": 5,
    "MD": 6, "ME": 7, "PD": 8, "PE": 9, "SA": 10, "CA": 11
}
mercado.sort(key=lambda x: ordem_posicoes.get(x.get("posicao", ""), 99))

if not mercado:
    st.warning("⚠️ Nenhum jogador disponível no mercado.")
else:
    st.markdown("### 📋 Jogadores Disponíveis")
    for jogador in mercado:
        col1, col2, col3, col4, col5 = st.columns([1, 3, 1, 2, 2])
        with col1:
            st.markdown(f"**{jogador.get('posicao', '')}**")
        with col2:
            st.write(jogador.get("nome", ""))
        with col3:
            st.write(jogador.get("overall", ""))
        with col4:
            st.write(f"R$ {jogador.get('valor', 0):,.0f}")
        with col5:
            if st.button("Comprar", key=f"comprar_{jogador['id_doc']}"):
                # Verificar saldo
                time_ref = db.collection("times").document(id_time)
                saldo = time_ref.get().to_dict().get("saldo", 0)
                valor = jogador.get("valor", 0)

                if saldo < valor:
                    st.error("❌ Saldo insuficiente para realizar a compra.")
                else:
                    # Atualiza saldo
                    time_ref.update({"saldo": saldo - valor})

                    # Adiciona jogador ao elenco
                    jogador_elenco = {
                        "nome": jogador.get("nome"),
                        "posicao": jogador.get("posicao"),
                        "overall": jogador.get("overall"),
                        "valor": valor
                    }
                    db.collection("times").document(id_time).collection("elenco").add(jogador_elenco)

                    # Remove do mercado
                    db.collection("mercado_transferencias").document(jogador["id_doc"]).delete()

                    # Registrar movimentação
                    registrar_movimentacao(
                        db=db,
                        id_time=id_time,
                        jogador=jogador["nome"],
                        categoria="Compra",
                        tipo="Saída",
                        valor=valor
                    )

                    st.success(f"✅ {jogador['nome']} comprado com sucesso!")
                    st.rerun()
