import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Configurações
id_jogador = "yvnD4yCIbEr3VHBomk5L"  # <- Coloque aqui o ID do jogador que você quer colocar no leilão

# Atualiza o leilão ativo
leilao_ref = db.collection("configuracoes").document("leilao_sistema")

leilao_ref.set({
    "ativo": True,
    "leilao_ativo": id_jogador
})

print("Leilão criado com sucesso!")
