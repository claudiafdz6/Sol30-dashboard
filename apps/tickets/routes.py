# from flask import Blueprint, render_template, request, redirect, url_for
# from flask_login import login_required, current_user
# from apps import db
# from apps.authentication.models import TicketSupervisor

# blueprint = Blueprint('tickets_blueprint', __name__)

# @blueprint.route('/tickets', methods=['GET', 'POST'])
# @login_required
# def tickets():
#     if request.method == 'POST':
#         utente_apertura = request.form['utente_apertura']
#         utente_segnalato = request.form['utente_segnalato']
#         id_task = request.form['id_task']
#         note = request.form.get('note')
#         tag = request.form.get('tag')
#         data_apertura = request.form['data_apertura']
        
#         new_ticket = TicketSupervisor(
#             utente_apertura=utente_apertura,
#             utente_segnalato=utente_segnalato,
#             id_task=id_task,
#             note=note,
#             tag=tag,
#             data_apertura=data_apertura
#         )
#         db.session.add(new_ticket)
#         db.session.commit()
#         return redirect(url_for('tickets_blueprint.tickets'))

#     tickets = TicketSupervisor.query.all()
#     return render_template('index.html', tickets=tickets)





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
    if form.validate_on_submit():
        new_ticket = TicketSupervisor(
            utente_apertura=form.utente_apertura.data,
            utente_segnalato=form.utente_segnalato.data,
            id_task=form.id_task.data,
            note=form.note.data,
            tag=form.tag.data,
            data_apertura=form.data_apertura.data,
            data_chiusura=form.data_chiusura.data
        )
        db.session.add(new_ticket)
        db.session.commit()
        flash('Ticket added successfully', 'success')
        return redirect(url_for('tickets_blueprint.tickets'))

    tickets = TicketSupervisor.query.all()
    return render_template('home/index.html', tickets=tickets, form=form)
