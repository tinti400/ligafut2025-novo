import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Dicionário com e-mail do usuário e o ID do time correspondente
usuarios_times = {
    "brunotinti400@gmail.com": "6ScPtoiLBn27re1nLaOZ",  # Exemplo: Cruzeiro
    "baiano@bahia": "9GP2DYELgPYVtonYZpKW",      # Exemplo: Botafogo
    # Adicione os demais usuários aqui...
}

usuarios_ref = db.collection("usuarios")
usuarios = usuarios_ref.stream()

for doc in usuarios:
    dados = doc.to_dict()
    email = dados.get("usuario")

    if email in usuarios_times:
        id_time = usuarios_times[email]
        usuarios_ref.document(doc.id).update({"id_time": id_time})
        print(f"ID do time atualizado para o usuário: {email}")
    else:
        print(f"Usuário {email} não encontrado no dicionário. Não atualizado.")

print("Atualização concluída!")
