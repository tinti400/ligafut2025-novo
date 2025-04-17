
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa o Firebase
cred = credentials.Certificate("liga-fut-12345.json")  # Substitua pelo nome do seu JSON
firebase_admin.initialize_app(cred)
db = firestore.client()

# Lista com os 10 técnicos e times da Divisão 1
dados = [
    {"tecnico": "Danilo", "email": "danilo@email.com", "time": "Flamengo"},
    {"tecnico": "Carlos", "email": "carlos@email.com", "time": "Palmeiras"},
    {"tecnico": "Lucas", "email": "lucas@email.com", "time": "São Paulo"},
    {"tecnico": "Marcos", "email": "marcos@email.com", "time": "Grêmio"},
    {"tecnico": "Felipe", "email": "felipe@email.com", "time": "Internacional"},
    {"tecnico": "Rafael", "email": "rafael@email.com", "time": "Cruzeiro"},
    {"tecnico": "Thiago", "email": "thiago@email.com", "time": "Atlético-MG"},
    {"tecnico": "Vinícius", "email": "vinicius@email.com", "time": "Botafogo"},
    {"tecnico": "Pedro", "email": "pedro@email.com", "time": "Fortaleza"},
    {"tecnico": "André", "email": "andre@email.com", "time": "Bahia"}
]

ids_tecnicos = []
ids_times = []

# Cria os times e técnicos
for d in dados:
    # Cria o time
    time_ref = db.collection("times").add({
        "nome": d["time"],
        "tecnico": d["tecnico"],
        "saldo": 100_000_000
    })
    time_id = time_ref[1].id
    ids_times.append(time_id)

    # Cria o técnico
    tecnico_ref = db.collection("tecnicos").add({
        "nome": d["tecnico"],
        "email": d["email"],
        "time_id": time_id,
        "saldo": 100_000_000
    })
    tecnico_id = tecnico_ref[1].id
    ids_tecnicos.append(tecnico_id)

# Cria a liga com os 10 times na Divisão 1
liga = {
    "nome": "Liga Elite",
    "ano": 2025,
    "administradores": [ids_tecnicos[0]],  # Danilo como admin
    "divisao_1": ids_times,
    "divisao_2": []
}

db.collection("ligas").add(liga)

print("✅ Técnicos, Times e Liga criados com sucesso!")
