from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

# Inicializa as extensões para o visual e tempo do professor
from flask_bootstrap import Bootstrap
from flask_moment import Moment

bootstrap = Bootstrap(app)
moment = Moment(app)


# --- ROTAS DE ERRO ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# --- ROTAS DA APLICAÇÃO ---

# 1. Página Inicial (Home)
@app.route('/')
def index():
    # Passa o horário atual para o Flask-Moment trabalhar na página principal
    return render_template('index.html', current_time=datetime.utcnow())


# 2. Página de Identificação do Aluno (Aceita Nome, Prontuário e Instituição)
@app.route('/user/<name>/<prontuario>/<institution>')
def user(name, prontuario, institution):
    # Envia os dados dinâmicos da URL direto para o template user.html
    return render_template(
        'user.html', 
        name=name, 
        prontuario=prontuario, 
        institution=institution
    )


# 3. Página de Contexto da Requisição (Navegador, IP e Host)
@app.route('/contextorequisicao')
def contextorequisicao():
    # Captura os dados do acesso do usuário através do objeto 'request'
    user_agent = request.headers.get('User-Agent')
    remote_addr = request.remote_addr
    host = request.host
    
    # Envia os dados capturados para o template contexto.html
    return render_template(
        'contexto.html', 
        user_agent=user_agent, 
        remote_addr=remote_addr, 
        host=host,
        current_time=datetime.utcnow()
    )


if __name__ == '__main__':
    app.run(debug=True)
