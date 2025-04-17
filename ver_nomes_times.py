import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase
cred = credentials.Certificate("credenciais.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# IDs informados
ids_times = [
    "0fgitv421Pe4OWu6OYnm",
    "648H5LX98Rkd0DemlWEX",
    "6ScPtoiLBn27re1nLaOZ",
    "6lLrThoafAocWJosvLh0",
    "7DzNqRL8bDu4bSMLpufj",
    "91zvcBPDxfbWUuoZdYqd",
    "9GP2DYELgPYVtonYZpKW",
    "BVwhAm54WYzY095vOUyT",
    "ENxH4QPxPvpyTFqMP4w8",
    "Lqw71T9zWpqm8Iub2cLq"
]

print("📋 Nomes dos times cadastrados:")
for id_time in ids_times:
    doc = db.collection("times").document(id_time).get()
    if doc.exists:
        dados = doc.to_dict()
        print(f"{id_time} => {dados.get('nome', 'NOME NÃO ENCONTRADO')}")
    else:
        print(f"{id_time} => ❌ Documento não encontrado")
