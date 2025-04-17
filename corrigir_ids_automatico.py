import firebase_admin
from firebase_admin import credentials, firestore

# Conectar ao Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")  # Seu arquivo JSON
    firebase_admin.initialize_app(cred)

db = firestore.client()

id_liga = "VUnsRMAPOc9Sj9n5BenE"  # ID da sua Liga

# Buscar todos os times cadastrados
times_ref = db.collection("times").stream()
ids_times = [doc.id for doc in times_ref]

print("IDs de Times válidos encontrados:")
print(ids_times)
print("=" * 50)

# Buscar rodadas
rodadas_ref = db.collection("ligas").document(id_liga).collection("rodadas_divisao_1").stream()

for rodada in rodadas_ref:
    dados = rodada.to_dict()
    numero = dados.get("numero", rodada.id)
    print(f"\nCorrigindo Rodada {numero}...")

    jogos_corrigidos = []

    for jogo in dados.get("jogos", []):
        mandante = jogo.get("mandante")
        visitante = jogo.get("visitante")

        if mandante in ids_times and visitante in ids_times:
            jogos_corrigidos.append(jogo)
        else:
            print(f"Removendo jogo inválido: {mandante} x {visitante}")

    rodada_ref = db.collection("ligas").document(id_liga).collection("rodadas_divisao_1").document(rodada.id)
    rodada_ref.update({"jogos": jogos_corrigidos})

print("\n✅ Todas as rodadas foram corrigidas automaticamente!")
