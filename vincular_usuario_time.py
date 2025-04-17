import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")  # seu arquivo de credenciais
    firebase_admin.initialize_app(cred)

db = firestore.client()

print("==== VINCULAR USUÁRIO A UM TIME ====")
id_time = input("Digite o ID do time que deseja vincular: ").strip()
id_usuario = input("Digite o ID do usuário que deseja vincular: ").strip()

# Referência do documento do time
time_ref = db.collection("times").document(id_time)

# Atualiza o campo id_usuario
time_ref.update({
    "id_usuario": id_usuario
})

print(f"Usuário {id_usuario} vinculado ao time {id_time} com sucesso!")
