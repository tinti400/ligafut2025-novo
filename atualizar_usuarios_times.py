import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase
cred = credentials.Certificate("credenciais.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

usuarios_para_corrigir = {
    "atletico-mg@ligafut.com": {
        "id_time": "0fgitv421Pe4OWu6OYnm",
        "nome_time": "Atlético-MG"
    },
    "gremio@ligafut.com": {
        "id_time": "91zvcBPDxfbWUuoZdYqd",
        "nome_time": "Grêmio"
    },
    "saopaulo@ligafut.com": {
        "id_time": "BVwhAm54WYzY095vOUyT",
        "nome_time": "São Paulo"
    }
}

print("⏳ Atualizando usuários...")

usuarios_ref = db.collection("usuarios").stream()

for usuario in usuarios_ref:
    dados = usuario.to_dict()
    email = dados.get("usuario")

    if email in usuarios_para_corrigir:
        dados_update = usuarios_para_corrigir[email]
        usuario.reference.update(dados_update)
        print(f"✅ Usuário {email} atualizado com sucesso!")

print("🏁 Atualização finalizada!")
