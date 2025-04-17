import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa o Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")  # troque pelo nome do seu JSON
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Criar coleção e documento do mercado
mercado_ref = db.collection("configuracoes").document("mercado")

# Definindo o status inicial como 'fechado'
mercado_ref.set({
    "status": "fechado"
})

print("✅ Coleção 'configuracoes' e documento 'mercado' criado com sucesso no Firestore!")
