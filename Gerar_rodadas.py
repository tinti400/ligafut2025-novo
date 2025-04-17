import firebase_admin
from firebase_admin import credentials, firestore
import random
import itertools

# Inicializar Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("credenciais.json")  # coloque o nome do seu JSON
    firebase_admin.initialize_app(cred)

db = firestore.client()

id_liga = "VUnsRMAPOc9Sj9n5BenE"  # ID da sua Liga

# Buscar times da coleção 'times'
def buscar_times():
    times_ref = db.collection("times")
    times = [doc.id for doc in times_ref.stream()]
    return times

# Excluir rodadas antigas
def excluir_rodadas_antigas():
    rodadas_ref = db.collection("ligas").document(id_liga).collection("rodadas_divisao_1")
    docs = rodadas_ref.stream()
    for doc in docs:
        doc.reference.delete()
    print("✅ Rodadas antigas excluídas.")

# Gerar confrontos turno
def gerar_turno(times):
    confrontos = list(itertools.combinations(times, 2))
    random.shuffle(confrontos)
    rodadas = []
    num_rodadas = (len(times) - 1) * 2  # Turno e returno
    jogos_por_rodada = len(times) // 2

    for i in range(num_rodadas // 2):
        rodada = confrontos[i * jogos_por_rodada:(i + 1) * jogos_por_rodada]
        rodadas.append(rodada)
    return rodadas

# Gerar returno invertendo mandantes e visitantes
def gerar_returno(rodadas_turno):
    return [[(visitante, mandante) for mandante, visitante in rodada] for rodada in rodadas_turno]

# Salvar rodadas no Firebase
def salvar_rodadas(rodadas):
    for i, rodada in enumerate(rodadas, 1):
        jogos = [{"mandante": mandante, "visitante": visitante, "gols_mandante": 0, "gols_visitante": 0} for mandante, visitante in rodada]
        db.collection("ligas").document(id_liga).collection("rodadas_divisao_1").document(f"rodada_{i}").set({
            "numero": i,
            "jogos": jogos
        })
    print("✅ Novas rodadas criadas com sucesso.")

# Execução
excluir_rodadas_antigas()
times = buscar_times()
print(f"📋 Times encontrados: {times}")

rodadas_turno = gerar_turno(times)
rodadas_returno = gerar_returno(rodadas_turno)

todas_rodadas = rodadas_turno + rodadas_returno
salvar_rodadas(todas_rodadas)
