import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa o Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def excluir_tecnicos_sem_time():
    tecnicos_ref = db.collection("tecnicos")
    times_ref = db.collection("times")

    # Buscar todos os IDs dos times existentes
    times_docs = times_ref.stream()
    times_ids = [doc.id for doc in times_docs]

    # Buscar todos os técnicos
    tecnicos_docs = tecnicos_ref.stream()

    excluidos = 0
    for tecnico in tecnicos_docs:
        dados = tecnico.to_dict()
        id_time = dados.get("id_time")

        # Verifica se o id_time do técnico está na lista de times existentes
        if id_time not in times_ids:
            print(f"Excluindo técnico {tecnico.id} - ID Time inexistente: {id_time}")
            tecnico.reference.delete()
            excluidos += 1

    print(f"\nProcesso finalizado! Técnicos excluídos: {excluidos}")

# Executar
excluir_tecnicos_sem_time()
