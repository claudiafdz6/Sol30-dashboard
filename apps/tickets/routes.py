from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from apps import db
from apps.tickets.forms import TicketForm
from apps.authentication.models import TicketSupervisor
from datetime import datetime
from zoneinfo import ZoneInfo
import os
from flask import current_app
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename
import json
import uuid


blueprint = Blueprint('tickets_blueprint', __name__)

@blueprint.route('/tickets', methods=['GET', 'POST'])
@login_required
def tickets():
    form = TicketForm()
    if request.method == 'POST':
        if current_user.is_admin:
            files = request.files.getlist('file')
            filenames = []
            if files:
                for file in files:
                    if file:
                        filename = secure_filename(file.filename)
                        unique_filename = generate_unique_filename(filename)
                        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                        file.save(file_path)
                        filenames.append(os.path.join('static/assets/img/', unique_filename))

            new_ticket = TicketSupervisor(
                utente_apertura=current_user.username,
                utente_segnalato=form.utente_segnalato.data,
                id_task=form.id_task.data,
                note=form.note.data,
                tag=form.tag.data,
                image=filenames if filenames else []  # save image paths as JSON array
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
                ticket.utente_segnalato = request.form['utente_segnalato']
                ticket.id_task = request.form['id_task']
                ticket.tag = request.form['tag']
                ticket.note = request.form['note']
                
                files = request.files.getlist('file')

                if isinstance(ticket.image, str):
                    filenames = json.loads(ticket.image)
                else:
                    filenames = ticket.image if ticket.image else []
 
                if files:
                    for file in files:
                        if file:
                            filename = secure_filename(file.filename)
                            unique_filename = generate_unique_filename(filename)
                            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                            file.save(file_path)
                            filenames.append(os.path.join('static/assets/img/', unique_filename))
                if len(filenames) > 1:
                    ticket.image = json.dumps(filenames)
                else:
                    ticket.image = filenames

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

# to upload photo into DB
@blueprint.route('/upload_photo', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		file = request.files['file']
		upload = TicketSupervisor(data=file.read())
		db.session.add(upload)
		db.session.commit()
		return f'Uploaded'
	return render_template('index.html')

# to delete the photo from DB
@blueprint.route('/delete_photo/<int:ticket_id>', methods=['DELETE'])
@login_required
def delete_photo(ticket_id):
    if current_user.is_admin:
        ticket = TicketSupervisor.query.get(ticket_id)
        if ticket and ticket.image:
            # delete file system image
            #image_path = os.path.join(current_app.root_path, ticket.image)
            ticket_image_dict = ticket.image
            ticket_image_string = json.dumps(ticket_image_dict)

            image_path = os.path.join(current_app.root_path, ticket_image_string)

            if os.path.exists(image_path):
                os.remove(image_path)
            
            # remove image from DB
            ticket.image = []
            db.session.commit()
            return jsonify(success=True)
        else:
            return jsonify(success=False, message='Image not found to delete'), 404
    else:
        return jsonify(success=False, message='You are not authorized'), 403
    

def generate_unique_filename(filename):
    unique_id = uuid.uuid4().hex
    name, ext = os.path.splitext(filename)
    return f"{name}_{unique_id}{ext}"

