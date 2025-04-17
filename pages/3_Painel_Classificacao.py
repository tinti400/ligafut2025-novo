import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# Configuração da página
st.set_page_config(page_title="Classificação", layout="wide")

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Verificação de login
if "id_time" not in st.session_state:
    st.warning("Você precisa estar logado para acessar esta página.")
    st.stop()

st.title("🏆 Painel de Classificação e Resultados")

id_liga = st.text_input("ID da Liga", "VUnsRMAPOc9Sj9n5BenE")
numero_rodada = st.number_input("Número da Rodada", min_value=1, step=1)

# Buscar Times
def buscar_times():
    times_ref = db.collection("times").stream()
    return {doc.id: doc.to_dict().get("nome", "Sem Nome") for doc in times_ref}

# Buscar Jogos
def buscar_jogos(id_liga, numero_rodada):
    ref = db.collection("ligas").document(id_liga).collection("rodadas_divisao_1").document(f"rodada_{numero_rodada}")
    doc = ref.get()
    if doc.exists:
        return doc.to_dict().get("jogos", [])
    return []

# Salvar Resultado
def salvar_resultado(id_liga, numero_rodada, index, gols_mandante, gols_visitante):
    ref = db.collection("ligas").document(id_liga).collection("rodadas_divisao_1").document(f"rodada_{numero_rodada}")
    doc = ref.get()
    if doc.exists:
        dados = doc.to_dict()
        jogos = dados.get("jogos", [])
        jogos[index]["gols_mandante"] = gols_mandante
        jogos[index]["gols_visitante"] = gols_visitante
        ref.update({"jogos": jogos})
        st.success("✅ Resultado salvo com sucesso!")

# Calcular Classificação
def calcular_classificacao(times, id_liga, rodada_maxima):
    tabela = {id_time: {"Time": nome, "P": 0, "J": 0, "V": 0, "E": 0, "D": 0, "GP": 0, "GC": 0, "SG": 0} for id_time, nome in times.items()}

    for numero in range(1, rodada_maxima + 1):
        jogos = buscar_jogos(id_liga, numero)
        for jogo in jogos:
            if "gols_mandante" not in jogo or "gols_visitante" not in jogo:
                continue

            mandante = jogo["mandante"]
            visitante = jogo["visitante"]
            gm = jogo["gols_mandante"]
            gv = jogo["gols_visitante"]

            if mandante not in tabela or visitante not in tabela:
                continue

            tabela[mandante]["J"] += 1
            tabela[visitante]["J"] += 1
            tabela[mandante]["GP"] += gm
            tabela[mandante]["GC"] += gv
            tabela[visitante]["GP"] += gv
            tabela[visitante]["GC"] += gm

            if gm > gv:
                tabela[mandante]["P"] += 3
                tabela[mandante]["V"] += 1
                tabela[visitante]["D"] += 1
            elif gm < gv:
                tabela[visitante]["P"] += 3
                tabela[visitante]["V"] += 1
                tabela[mandante]["D"] += 1
            else:
                tabela[mandante]["P"] += 1
                tabela[visitante]["P"] += 1
                tabela[mandante]["E"] += 1
                tabela[visitante]["E"] += 1

    for time in tabela.values():
        time["SG"] = time["GP"] - time["GC"]

    return sorted(tabela.values(), key=lambda x: (-x["P"], -x["SG"], -x["GP"]))

# Exibir jogos da rodada
times = buscar_times()
jogos = buscar_jogos(id_liga, numero_rodada)

if jogos:
    st.subheader(f"📋 Rodada {numero_rodada} - Resultados")

    for i, jogo in enumerate(jogos):
        col1, col2, col3, col4 = st.columns([4, 1, 1, 2])
        with col1:
            mandante = times.get(jogo["mandante"], "Desconhecido")
            visitante = times.get(jogo["visitante"], "Desconhecido")
            st.text(f"{mandante} x {visitante}")
        with col2:
            gm = st.number_input(f"Gols {mandante}", min_value=0, value=jogo.get("gols_mandante", 0), key=f"gm_{i}")
        with col3:
            gv = st.number_input(f"Gols {visitante}", min_value=0, value=jogo.get("gols_visitante", 0), key=f"gv_{i}")
        with col4:
            if st.button("Salvar", key=f"salvar_{i}"):
                salvar_resultado(id_liga, numero_rodada, i, gm, gv)

    # Classificação
    st.markdown("---")
    st.subheader("🏆 Classificação Atualizada")

    classificacao = calcular_classificacao(times, id_liga, numero_rodada)
    df = pd.DataFrame(classificacao)
    df.index = range(1, len(df) + 1)
    df.reset_index(inplace=True)
    df.rename(columns={"index": "Posição"}, inplace=True)

    def highlight(row):
        idx = row["Posição"]
        if idx == 1:
            return ["background-color: #d4edda"] * len(row)
        elif idx <= 4:
            return ["background-color: #c3e6cb"] * len(row)
        elif idx > len(df) - 2:
            return ["background-color: #f8d7da"] * len(row)
        return [""] * len(row)

    st.dataframe(df.style.apply(highlight, axis=1), use_container_width=True)
else:
    st.warning("⚠️ Nenhum jogo encontrado para essa rodada.")
