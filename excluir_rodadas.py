import firebase_admin
from firebase_admin import credentials, firestore

# Conectar ao Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")  # Seu arquivo JSON
    firebase_admin.initialize_app(cred)

db = firestore.client()

id_liga = "VUnsRMAPOc9Sj9n5BenE"  # ID da sua Liga

# Referência das rodadas
rodadas_ref = db.collection("ligas").document(id_liga).collection("rodadas_divisao_1").stream()

print("Excluindo rodadas...")

for rodada in rodadas_ref:
    rodada.reference.delete()
    print(f"Rodada {rodada.id} excluída com sucesso.")

print("✅ Todas as rodadas foram excluídas.")
