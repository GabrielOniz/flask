from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User, Role
from ..email import sendgrid_send_message
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:

            user_role = Role.query.filter_by(name='User').first()

            if user_role is None:
                user_role = Role(name='User')
                db.session.add(user_role)
                db.session.commit()

            user = User(username=form.name.data, role=user_role)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            print('FLASKY_ADMIN: ' + str(current_app.config['FLASKY_ADMIN']), flush=True)
            if current_app.config['FLASKY_ADMIN']:
                #send_email(current_app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
                print('Enviando mensagem...', flush=True)
                sendgrid_send_message([str(current_app.config['FLASKY_ADMIN']), "flaskaulasweb@zohomail.com"], '[Flask App] Novo Usuário Cadastrado', form.name.data)
                print('Mensagem enviada...', flush=True)
        else:

            if user.role is None:
                user_role = Role.query.filter_by(name='User').first()

                if user_role is None:
                    user_role = Role(name='User')
                    db.session.add(user_role)
                    db.session.commit()

                user.role = user_role
                db.session.commit()

            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))

    users = User.query.all()
    roles = Role.query.all()

    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False), users=users, roles=roles)
