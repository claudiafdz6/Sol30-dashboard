from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from apps import db
from apps.tickets.forms import TicketForm
from apps.authentication.models import TicketSupervisor
from datetime import datetime
from zoneinfo import ZoneInfo
import os
from flask import current_app
from werkzeug.utils import secure_filename

blueprint = Blueprint('tickets_blueprint', __name__)

@blueprint.route('/tickets', methods=['GET', 'POST'])
@login_required
def tickets():
    form = TicketForm()
    if request.method == 'POST':
        if current_user.is_admin:
            file = request.files.get('file')
            filename = None
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                filename = os.path.join('static/assets/img/', filename)
                
            new_ticket = TicketSupervisor(
                utente_apertura=current_user.username,
                utente_segnalato=form.utente_segnalato.data,
                id_task=form.id_task.data,
                note=form.note.data,
                tag=form.tag.data,
                image=filename  # save the image path to the database
            )
            db.session.add(new_ticket)
            db.session.commit()
            flash('Ticket added', 'success')
        else:
            flash('You are not authorized to add new tickets.', 'danger')
        return redirect(url_for('tickets_blueprint.tickets'))
    
    tickets = TicketSupervisor.query.all()
    return render_template('home/index.html', tickets=tickets, form=form)


@blueprint.route('/edit_ticket', methods=['POST'])
@login_required
def edit_ticket():
    if current_user.is_admin:
        ticket_id = request.form['id']
        ticket = TicketSupervisor.query.get(ticket_id)
        if ticket:
            if ticket.data_chiusura:
                flash('It is not possible to edit a closed ticket', 'danger')
            else:
                ticket.note = request.form['note']
                file = request.files.get('file')
                if file:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    filename = os.path.join('static/assets/img/', filename)
                    ticket.image = filename
                db.session.commit()
                flash('Ticket updated successfully', 'success')
        else:
            flash('Ticket not found', 'danger')
    else:
        flash('You are not authorized to edit tickets', 'danger')
    return redirect(url_for('tickets_blueprint.tickets'))


@blueprint.route('/close_ticket', methods=['POST'])
@login_required
def close_ticket():
    if current_user.is_admin:
        data = request.get_json()
        ticket_id = data['id']
        ticket = TicketSupervisor.query.get(ticket_id)
        if ticket:
            if ticket.data_chiusura:
                return jsonify(success=False, message='Ticket is already closed'), 400
            ticket.data_chiusura = datetime.now(ZoneInfo('Europe/Rome'))
            db.session.commit()
            return jsonify(success=True)
        else:
            return jsonify(success=False, message='Ticket not found'), 404
    else:
        return jsonify(success=False, message='You are not authorized'), 403

#to upload photo into the bd
@blueprint.route('/upload_photo', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		file = request.files['file']
		upload = TicketSupervisor(data=file.read())
		db.session.add(upload)
		db.session.commit()
		return f'Uploaded'
	return render_template('index.html')
