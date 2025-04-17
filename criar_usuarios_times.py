import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Buscar os times cadastrados
times_ref = db.collection("times").stream()

for time in times_ref:
    dados = time.to_dict()
    nome_time = dados.get("nome", "").lower().replace(" ", "")
    id_time = time.id

    usuario = f"{nome_time}@ligafut.com"
    senha = "123456"

    # Verificar se o usuário já existe
    usuarios_ref = db.collection("usuarios")
    usuarios_query = usuarios_ref.where("usuario", "==", usuario).get()

    if usuarios_query:
        print(f"Usuário {usuario} já existe. Pulando...")
    else:
        novo_usuario = {
            "usuario": usuario,
            "senha": senha,
            "id_time": id_time
        }
        db.collection("usuarios").add(novo_usuario)
        print(f"Usuário {usuario} criado com sucesso!")

print("Todos os usuários foram criados com sucesso!")
