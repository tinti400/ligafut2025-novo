import firebase_admin
from firebase_admin import credentials, firestore
import unicodedata

# Função para normalizar o nome
def normalizar(texto):
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8').lower().strip()

# Inicializar Firebase
cred = credentials.Certificate("credenciais.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Buscar todos os times e criar um dicionário nome_normalizado: id_time
times_ref = db.collection("times").stream()
times = {}

for time in times_ref:
    time_dict = time.to_dict()
    nome_time = time_dict.get("nome", "")
    nome_normalizado = normalizar(nome_time)
    times[nome_normalizado] = time.id

# Buscar todos os usuários
usuarios_ref = db.collection("usuarios").stream()

for usuario in usuarios_ref:
    usuario_dict = usuario.to_dict()
    usuario_id = usuario.id
    nome_time_usuario = usuario_dict.get("time", "")
    nome_usuario = usuario_dict.get("usuario", "sem_email")

    nome_normalizado_usuario = normalizar(nome_time_usuario)

    if nome_normalizado_usuario in times:
        id_time_correto = times[nome_normalizado_usuario]
        db.collection("usuarios").document(usuario_id).update({
            "id_time": id_time_correto
        })
        print(f"✅ Usuário {nome_usuario} atualizado com id_time: {id_time_correto}")
    else:
        print(f"❌ Usuário {nome_usuario} - Time não encontrado: {nome_time_usuario}")
