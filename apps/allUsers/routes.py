from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from apps import db
from apps.allUsers.forms import TicketForm
from apps.authentication.models import TicketSupervisor

blueprint = Blueprint('allUsers_blueprint', __name__)

@blueprint.route('/allUsers', methods=['GET', 'POST'])
@login_required
def allUsers():
    form = allUsers()
    if request.method == 'POST':
        if current_user.is_admin:
            show_allUsers = UserInformations()


def tickets():
    form = TicketForm()
    if request.method == 'POST':
        if current_user.is_admin:
            new_ticket = TicketSupervisor(
                utente_apertura=current_user.username,
                utente_segnalato=form.utente_segnalato.data,
                id_task=form.id_task.data,
                note=form.note.data,
                tag=form.tag.data,
            )
            db.session.add(new_ticket)
            db.session.commit()
            flash('The data has been modify', 'success')
        else:
            flash('You are not authorized to modify these data.', 'danger')
        return redirect(url_for('allUsers_blueprint.tickets'))
    

    if request.method == 'GET':
        tickets = TicketSupervisor.query.all()
        return render_template('home/allUsers.html', tickets=tickets, form=form)
 