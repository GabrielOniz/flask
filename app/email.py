from threading import Thread
from flask import current_app, render_template
# from flask_mail import Message
# from . import mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import requests
from datetime import datetime
import os

# def send_async_email(app, msg):
    # with app.app_context():
        # mail.send(msg)


# def send_email(to, subject, template, **kwargs):
    # app = current_app._get_current_object()
    # msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
    #              sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    # msg.html = render_template(template + '.html', **kwargs)
    # thr = Thread(target=send_async_email, args=[app, msg])
    # thr.start()
    # return thr

def send_simple_message(to, subject, newUser):
    app = current_app._get_current_object()
    print('Enviando mensagem (POST)...', flush=True)
    print('URL: ' + str(app.config['API_URL']), flush=True)
    print('api: ' + str(app.config['API_KEY']), flush=True)
    print('from: ' + str(app.config['API_FROM']), flush=True)
    print('to: ' + str(to), flush=True)
    print('subject: ' + str(app.config['FLASKY_MAIL_SUBJECT_PREFIX']) + ' ' + subject, flush=True)
    print('text: ' + "Novo usuário cadastrado: " + newUser, flush=True)

    resposta = requests.post(app.config['API_URL'],
                             auth=("api", app.config['API_KEY']), data={"from": app.config['API_FROM'],
                                                                        "to": to,
                                                                        "subject": app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                                                                        "text": "Novo usuário cadastrado: " + newUser})

    print('Enviando mensagem (Resposta)...' + str(resposta) + ' - ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), flush=True)
    return resposta


def sendgrid_send_message(to_emails_list, subject, new_user_name):

    message = Mail(
    from_email= str(current_app.config['FLASKY_ADMIN']),
    to_emails= to_emails_list,
    subject=subject,
    html_content=f'<p>Novo usuário cadastrado na aplicação: <strong>{new_user_name}</strong></p>')

    try:

        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)

    except Exception as e:
        print(str(e), flush=True)