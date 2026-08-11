from datetime import datetime
# Adicionado o "request" no import abaixo
from flask import Flask, render_template, request 
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)

bootstrap = Bootstrap(app)
moment = Moment(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
     return render_template('index.html', current_time=datetime.utcnow())


@app.route('/user/<name>/<prontuario>/<institution>')
def user(name, prontuario, institution):
    # Envia todas as variáveis dinâmicas capturadas para o template
    return render_template(
        'user.html', 
        name=name, 
        prontuario=prontuario, 
        institution=institution
    )


@app.route('/contextorequisicao')
def contextorequisicao():
    user_agent = request.headers.get('User-Agent')
    remote_addr = request.remote_addr
    host = request.host
    
    # Envia os dados estruturados e o horário atual para o template
    return render_template(
        'contexto.html', 
        name="Gabriel Oniz",  
        user_agent=user_agent, 
        remote_addr=remote_addr, 
        host=host,
        current_time=datetime.utcnow()
    )
