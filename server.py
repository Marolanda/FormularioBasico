from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_cors import CORS
import json
import re
import os

app = Flask(__name__)
CORS(app)
app.secret_key = 'segredo_super_secreto'  # Pode ser qualquer string

# Função de validação
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

# Rota de cadastro
@app.route('/cadastro', methods=['POST'])
def cadastro():
    dados = request.get_json()
    nome = dados.get('nome', '').strip()
    email = dados.get('email', '').strip()
    senha = dados.get('senha', '')

    mensagens = validar_dados(nome, email, senha)

    if mensagens:
        return jsonify({"status": "erro", "mensagens": mensagens}), 400

    # Lê os usuários do arquivo
    try:
        with open('usuarios.json', 'r') as arquivo:
            usuarios = json.load(arquivo)
    except FileNotFoundError:
        usuarios = []

    # Verifica se o e-mail já existe
    for u in usuarios:
        if u['email'] == email:
            return jsonify({'status': 'erro', 'mensagens': ['Este e-mail já está cadastrado.']}), 400

    # Adiciona novo usuário (com permissão 'regular' por padrão)
    usuarios.append({'nome': nome, 'email': email, 'senha': senha, 'permissao': 'regular'})

    # Salva no arquivo usuarios.json
    with open('usuarios.json', 'w') as arquivo:
        json.dump(usuarios, arquivo, indent=4)

    return jsonify({"status": "sucesso", "mensagem": "Cadastro validado e salvo com sucesso!"})

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        try:
            with open('usuarios.json', 'r') as arquivo:
                usuarios = json.load(arquivo)
        except FileNotFoundError:
            usuarios = []

        # Verifica se o usuário existe e a senha bate
        for usuario in usuarios:
            if usuario['email'] == email and usuario['senha'] == senha:
                session['usuario'] = usuario['nome']
                session['permissao'] = usuario['permissao']  # Armazenando permissões
                flash(f'Login realizado com sucesso! Bem-vindo, {usuario["nome"]}.')
                return redirect('/area-protegida')

        flash('E-mail ou senha incorretos! Tente novamente.')
        return redirect('/login')

    return render_template('login.html')

# Rota protegida (só acessa quem estiver logado)
@app.route('/area-protegida')
def area_protegida():
    if 'usuario' in session:
        if session['permissao'] == 'admin':
            return f"<h2>Bem-vindo, {session['usuario']}! Você tem permissões de administrador.</h2><a href='/logout'>Sair</a>"
        else:
            return f"<h2>Bem-vindo, {session['usuario']}! Você tem permissões de usuário comum.</h2><a href='/logout'>Sair</a>"
    else:
        flash('Você precisa estar logado para acessar essa página.')
        return redirect('/login')


# Rota de logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('permissao', None)  # Limpa a permissão
    flash('Você saiu da sua conta.')
    return redirect('/login')

@app.route('/')
def exibir_cadastro():
    return render_template('cadastro.html')


if __name__ == '__main__':
    app.run(debug=True)
