import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase apenas uma vez
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
