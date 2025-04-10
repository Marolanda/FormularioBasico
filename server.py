from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

def validar_dados(nome, email, senha):
    erros = []

    if len(nome) < 3:
        erros.append("O nome deve ter pelo menos 3 caracteres.")

    email_valido = re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email)
    if not email_valido:
        erros.append("E-mail inválido.")

    senha_valida = re.match(r'^(?=.*[A-Z])(?=.*\d).{8,}$', senha)
    if not senha_valida:
        erros.append("A senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula e um número.")

    return erros

import os
import json

@app.route("/cadastro", methods=["POST"])
def cadastro():
    dados = request.get_json()
    nome = dados.get("nome", "").strip()
    email = dados.get("email", "").strip()
    senha = dados.get("senha", "")

    mensagens = []

    if len(nome) < 3:
        mensagens.append("O nome deve ter pelo menos 3 caracteres.")
    
    email_valido = re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email)
    if not email_valido:
        mensagens.append("E-mail inválido.")

    senha_valida = re.match(r"^(?=.*[A-Z])(?=.*\d).{8,}$", senha)
    if not senha_valida:
        mensagens.append("A senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula e um número.")

    if mensagens:
        return jsonify({"status": "erro", "mensagens": mensagens}), 400

    # 🔸 Salva no arquivo usuarios.json
    usuario = {"nome": nome, "email": email, "senha": senha}

    if not os.path.exists("usuarios.json"):
        with open("usuarios.json", "w") as f:
            json.dump([usuario], f, indent=4)
    else:
        with open("usuarios.json", "r+") as f:
            dados_existentes = json.load(f)
            dados_existentes.append(usuario)
            f.seek(0)
            json.dump(dados_existentes, f, indent=4)

    return jsonify({"status": "sucesso", "mensagem": "Cadastro validado e salvo com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)
