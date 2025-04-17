import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa o Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")  # ajuste o nome se o seu for diferente
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Lista de jogadores que serão inseridos
jogadores = [
    {"nome": "Diego Callai", "posicao": "GOL", "overall": 65, "valor": 2500000},
    {"nome": "Matheus Martins", "posicao": "MEI", "overall": 67, "valor": 4000000},
    {"nome": "Deivid Washington", "posicao": "ATA", "overall": 67, "valor": 3500000},
    {"nome": "Murillo", "posicao": "ZAG", "overall": 68, "valor": 4200000},
    {"nome": "Kendry Páez", "posicao": "MEI", "overall": 65, "valor": 2800000},
    {"nome": "Luis Marquinez", "posicao": "GOL", "overall": 67, "valor": 2200000},
    {"nome": "Iván Román", "posicao": "ZAG", "overall": 65, "valor": 1800000},
    {"nome": "Yaimar Medina", "posicao": "LAT", "overall": 69, "valor": 3000000},
    {"nome": "Allen Obando", "posicao": "ATA", "overall": 64, "valor": 1500000},
    {"nome": "Moisés Paniagua", "posicao": "MEI", "overall": 65, "valor": 2000000},
]

# Inserir jogadores no Firestore
for jogador in jogadores:
    db.collection("mercado_transferencias").add(jogador)

print("Jogadores inseridos com sucesso!")
