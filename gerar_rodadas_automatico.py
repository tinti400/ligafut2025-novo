import firebase_admin
from firebase_admin import credentials, firestore
import itertools
import random

# Conectar ao Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

id_liga = "VUnsRMAPOc9Sj9n5BenE"

# Buscar times válidos
times_ref = db.collection("times").stream()
ids_times = [doc.id for doc in times_ref]

print("Times encontrados para gerar rodadas:")
print(ids_times)

# Gera os confrontos turno e returno
confrontos = list(itertools.combinations(ids_times, 2))

# Embaralha os confrontos para dar aleatoriedade
random.shuffle(confrontos)

rodadas = []
rodada = []
rodada_numero = 1

for i, confronto in enumerate(confrontos):
    mandante, visitante = confronto
    rodada.append({
        'mandante': mandante,
        'visitante': visitante
    })
    if len(rodada) == len(ids_times) // 2:
        rodadas.append({'numero': rodada_numero, 'jogos': rodada})
        rodada_numero += 1
        rodada = []

# Duplicar as rodadas para o returno (invertendo mandante e visitante)
for rodada in rodadas.copy():
    jogos_returno = []
    for jogo in rodada['jogos']:
        jogos_returno.append({
            'mandante': jogo['visitante'],
            'visitante': jogo['mandante']
        })
    rodadas.append({'numero': rodada_numero, 'jogos': jogos_returno})
    rodada_numero += 1

# Salvar as rodadas no Firestore
for rodada in rodadas:
    doc_ref = db.collection("ligas").document(id_liga).collection("rodadas_divisao_1").document(f"rodada_{rodada['numero']}")
    doc_ref.set(rodada)
    print(f"Rodada {rodada['numero']} criada.")

print("✅ Todas as rodadas foram geradas com sucesso!")
