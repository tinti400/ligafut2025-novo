import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")  # Nome do seu arquivo JSON
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Exemplo de leilão livre
leilao_exemplo = {
    "id_time": "ID_DO_TIME_QUE_TA_LEILOANDO",  # ID do time dono do jogador
    "jogador": {
        "nome": "Nome do Jogador",
        "posicao": "ATA",
        "overall": 70,
        "valor": 5000000
    },
    "lance_atual": 5000000,  # Começa com o valor do jogador
    "comprador_atual": "",  # Fica vazio até alguém dar o primeiro lance
    "ativo": True,  # Leilão está ativo
    "tempo_restante": 120  # Em segundos (2 minutos)
}

# Criar o documento
db.collection("leiloes_livres").add(leilao_exemplo)

print("Coleção 'leiloes_livres' criada com sucesso e leilão exemplo inserido!")
