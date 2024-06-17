# -*- encoding: utf-8 -*-

from flask_login import UserMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

from datetime import datetime

from zoneinfo import ZoneInfo


class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    #by default, all news accounts will have 'null' value and later will be assigned whether they are 'user' or 'admin'
    is_admin = db.Column(db.Boolean, nullable=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)
    

class TicketSupervisor(db.Model, UserMixin):

    __tablename__ = 'TicketSupervisor'

    id = db.Column(db.Integer, primary_key=True)
    utente_apertura = db.Column(db.String(64), nullable=False)
    utente_segnalato = db.Column(db.String(64), nullable=False)
    id_task = db.Column(db.String(64), nullable=False)
    note = db.Column(db.Text, nullable=True)
    tag = db.Column(db.String(64), nullable=True)
    #data_apertura = db.Column(db.DateTime, default=datetime.now(ZoneInfo('Europe/Madrid')).strftime('%m/%d/%Y'))
    data_apertura = db.Column(db.DateTime, default=datetime.now(ZoneInfo('Europe/Madrid')))
    data_chiusura = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<TicketSupervisor {self.id_task}>'


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None