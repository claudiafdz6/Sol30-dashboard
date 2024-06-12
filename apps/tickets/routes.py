from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from apps import db
from apps.tickets.forms import TicketForm
from apps.authentication.models import TicketSupervisor

blueprint = Blueprint('tickets_blueprint', __name__)

@blueprint.route('/tickets', methods=['GET', 'POST'])
@login_required
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
                # data_apertura=form.data_apertura.data,  # <-- default=datetime.utcnow su model
                # data_chiusura=form.data_chiusura.data # <-- aggiorniamo la data alla chiusura
            )
            db.session.add(new_ticket)
            db.session.commit()
            flash('Ticket added', 'success')
        else:
            flash('You are not authorized to add new tickets.', 'danger')
        return redirect(url_for('tickets_blueprint.tickets'))
    

    if request.method == 'GET':
        tickets = TicketSupervisor.query.all()
        return render_template('home/index.html', tickets=tickets, form=form)
 