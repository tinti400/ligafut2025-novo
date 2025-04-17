import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa o Firebase
cred = credentials.Certificate("liga-fut-12345.json")  # Substitua pelo nome do seu JSON
firebase_admin.initialize_app(cred)
db = firestore.client()

# Função para apagar todos os documentos de uma coleção
def limpar_colecao(nome_colecao):
    colecao_ref = db.collection(nome_colecao).stream()
    count = 0
    for doc in colecao_ref:
        db.collection(nome_colecao).document(doc.id).delete()
        count += 1
    print(f"🗑️ Apagados {count} documentos da coleção '{nome_colecao}'")

# Limpa as coleções desejadas
limpar_colecao("tecnicos")
limpar_colecao("times")
limpar_colecao("ligas")

print("✅ Banco de dados limpo com sucesso!")
