import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ID do time
id_time = "648H5LX98Rkd0Dem"
nome_time = "Palmeiras"

# Criar time na coleção 'times'
db.collection("times").document(id_time).set({
    "nome": nome_time,
    "saldo": 250_000_000
})

print(f"✅ Time '{nome_time}' criado com sucesso!")
