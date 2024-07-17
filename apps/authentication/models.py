# -*- encoding: utf-8 -*-

from flask_login import UserMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass

from datetime import datetime

from zoneinfo import ZoneInfo

from sqlalchemy.dialects.postgresql import JSON

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    # by default, all news accounts will have 'null' value and later will be assigned whether they are 'user' or 'admin'
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

    __tablename__ = 'ticket_supervisor'
    id = db.Column(db.Integer, primary_key=True)
    utente_apertura = db.Column(db.String(100), nullable=False)
    utente_segnalato = db.Column(db.String(100), nullable=False)
    id_task = db.Column(db.String(64), nullable=False)
    note = db.Column(db.Text, nullable=True)
    tag = db.Column(db.String(150), nullable=True)
    data_apertura = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo('Europe/Rome')))
    data_chiusura = db.Column(db.DateTime, nullable=True) # by default the value is null
    # image = db.Column(db.String(256), nullable=True) 
    image = db.Column(db.JSON, nullable=True)  # store images as JSON array into database
    
    def __repr__(self):
        return f'<TicketSupervisor {self.id_task}>'
    
    # in order to see the date and time correctly in DD-MM-YYYY & H:M format, it's necessary to format the data using .strftime() method 
    def formatted_data_apertura(self):
        return self.data_apertura.strftime('%d/%m/%Y, %H:%M')
    
    def formatted_data_chiusura(self):
        return self.data_chiusura.strftime('%d/%m/%Y, %H:%M') if self.data_chiusura else 'None'
    
    # in order to be able to show the images using the routes, it's necessary to format the data and remove the square brackets
    def formatted_image(self):
        return self.image.replace('[', '').replace(']', '') if self.image else 'None'
    
@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None