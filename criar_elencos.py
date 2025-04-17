import firebase_admin
from firebase_admin import credentials, firestore

# Inicialização do Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")  # Troque se o nome for diferente
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Busca os times existentes
times_ref = db.collection("times")
times_docs = times_ref.stream()

for doc in times_docs:
    time_id = doc.id
    print(f"Criando elenco para o time: {time_id}")

    # Exemplo de jogadores iniciais - você pode personalizar depois
    jogadores = [
        {"nome": "Jogador 1", "posição": "Goleiro", "overall": 65, "valor": 5000000},
        {"nome": "Jogador 2", "posição": "Zagueiro", "overall": 66, "valor": 6000000},
        {"nome": "Jogador 3", "posição": "Meia", "overall": 67, "valor": 7000000},
        {"nome": "Jogador 4", "posição": "Atacante", "overall": 68, "valor": 8000000},
    ]

    elenco_ref = db.collection("times").document(time_id).collection("elenco")

    # Inserindo os jogadores no elenco
    for jogador in jogadores:
        elenco_ref.add(jogador)

print("✅ Elencos criados com sucesso!")
