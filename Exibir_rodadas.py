import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa o Firebase
cred = credentials.Certificate("credenciais.json")  # Substitua com o nome correto do seu arquivo de credenciais
firebase_admin.initialize_app(cred)
db = firestore.client()

# Nome da liga (certifique-se de usar o nome correto)
nome_liga = "Liga Elite"

# Busca a liga
ligas_ref = db.collection("ligas")
ligas = ligas_ref.where("nome", "==", nome_liga).stream()

liga_encontrada = None
for liga in ligas:
    liga_encontrada = liga
    break

if not liga_encontrada:
    print(f"⚠️ Liga '{nome_liga}' não encontrada.")
    exit()

# Buscar rodadas
rodadas_ref = db.collection("ligas").document(liga_encontrada.id).collection("rodadas_divisao_1")
rodadas = rodadas_ref.stream()

print(f"📝 Rodadas da {nome_liga}:")

# Exibe as rodadas
for rodada in rodadas:
    rodada_data = rodada.to_dict()
    print(f"\nRodada {rodada_data['numero']}:")
    for jogo in rodada_data["jogos"]:
        print(f"{jogo['mandante']} vs {jogo['visitante']}")

print("\n✅ Rodadas exibidas com sucesso!")
