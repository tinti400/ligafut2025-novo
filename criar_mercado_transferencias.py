import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa o Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")  # Use o seu arquivo .json correto
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Criar coleção mercado_transferencias vazia com documento de exemplo
doc_ref = db.collection('mercado_transferencias').document('exemplo')
doc_ref.set({
    'nome': 'Jogador Exemplo',
    'posicao': 'Meio-Campo',
    'overall': 65,
    'valor': 4000000
})

print('Coleção mercado_transferencias criada com sucesso!')
