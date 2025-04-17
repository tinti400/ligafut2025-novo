import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase
cred = credentials.Certificate("credenciais.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

novos_usuarios = [
    {"usuario": "atletico-mg@ligafut.com", "senha": "123", "id_time": "0fgitv421Pe4OWu6OYnm", "nome_time": "Atlético-MG"},
    {"usuario": "gremio@ligafut.com", "senha": "123", "id_time": "91zvcBPDxfbWUuoZdYqd", "nome_time": "Grêmio"},
    {"usuario": "saopaulo@ligafut.com", "senha": "123", "id_time": "BVwhAm54WYzY095vOUyT", "nome_time": "São Paulo"}
]

print("⏳ Criando usuários...")

for user in novos_usuarios:
    doc_ref = db.collection("usuarios").document()
    doc_ref.set(user)
    print(f"✅ Usuário {user['usuario']} criado com sucesso!")

print("🏁 Cadastro finalizado!")
