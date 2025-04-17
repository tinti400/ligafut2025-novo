import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Inicialização Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")  # Altere aqui
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Dicionário de times
times_ref = db.collection("times").stream()
times_dict = {doc.id: doc.to_dict().get("nome", "Desconhecido") for doc in times_ref}

st.title("📊 Inserir Resultados Manualmente - LigaFut")

# Escolher rodada
rodada = st.selectbox("Escolha a rodada:", [f"rodada_{i}" for i in range(1, 21)])

# Buscar jogos da rodada
jogos_doc = db.collection("ligas").document("VUnsRMAPOc9Sj9n5BenE").collection("rodadas_divisao_1").document(rodada).get()
if jogos_doc.exists:
    jogos = jogos_doc.to_dict().get("jogos", [])
    
    for idx, jogo in enumerate(jogos):
        mandante_id = jogo["mandante"]
        visitante_id = jogo["visitante"]

        mandante_nome = times_dict.get(mandante_id, "???")
        visitante_nome = times_dict.get(visitante_id, "???")

        col1, col2, col3 = st.columns([4, 1, 4])
        with col1:
            st.markdown(f"### {mandante_nome}")
            gols_mandante = st.number_input("Gols", min_value=0, key=f"gols_m_{idx}")
        with col2:
            st.markdown("### x")
        with col3:
            st.markdown(f"### {visitante_nome}")
            gols_visitante = st.number_input("Gols", min_value=0, key=f"gols_v_{idx}")
        
        if st.button(f"Salvar resultado {mandante_nome} x {visitante_nome}", key=f"btn_{idx}"):
            # Atualizar Firestore
            jogo["gols_mandante"] = gols_mandante
            jogo["gols_visitante"] = gols_visitante
            jogos[idx] = jogo
            db.collection("ligas").document("VUnsRMAPOc9Sj9n5BenE").collection("rodadas_divisao_1").document(rodada).update({
                "jogos": jogos
            })
            st.success("✅ Resultado salvo!")
else:
    st.warning("Rodada não encontrada.")
ssSVV