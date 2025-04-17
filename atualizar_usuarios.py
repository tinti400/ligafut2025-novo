import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa o Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Dados do usuário que deseja atualizar
email_usuario = "brunotinti400@gmail.com"

# Novo time que deseja vincular
novo_id_time = "ID_DO_TIME"  # Exemplo: "6lLrThoafAocWJosvLh0"
novo_nome_time = "Flamengo"  # Nome do time

# Caminho da coleção de usuários
usuarios_ref = db.collection("usuarios").where("email", "==", email_usuario).stream()

# Atualiza o usuário encontrado
for usuario in usuarios_ref:
    usuario.reference.update({
        "id_time": novo_id_time,
        "nome_time": novo_nome_time
    })
    print(f"Usuário {email_usuario} atualizado com sucesso!")

print("Processo finalizado!")

