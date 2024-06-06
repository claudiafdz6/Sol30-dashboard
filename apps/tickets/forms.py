# -*- encoding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired

class TicketForm(FlaskForm):
    utente_apertura = StringField('Utente apertura', validators=[DataRequired()])
    utente_segnalato = StringField('Utente segnalato', validators=[DataRequired()])
    id_task = StringField('ID task', validators=[DataRequired()])
    note = TextAreaField('Note')
    tag = StringField('Tag')
    data_apertura = DateTimeField('Data apertura', format='%d-%m-%Y %H:%M:%S', validators=[DataRequired()])
    data_chiusura = DateTimeField('Data chiusura', format='%d-%m-%Y %H:%M:%S')