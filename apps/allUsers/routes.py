from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from apps.authentication.models import Users, db
from flask_login import login_required, current_user

blueprint = Blueprint('allUsers_blueprint', __name__, url_prefix='/allUsers')

@blueprint.route('/', methods=['GET'])
@login_required
def all_users():
    if request.method == 'GET':
        users = Users.query.all()
        return render_template('home/allUsers.html', users=users)

@blueprint.route('/', methods=['POST'])
def edit_user():
    if request.method == 'POST':
        if current_user.is_admin:
            user_id = request.form['id']
            user = Users.query.get(user_id)
            
            if user:
                user.username = request.form['username']
                user.email = request.form['email']
                user.is_admin = 'is_admin' in request.form

                db.session.commit()
                flash('User updated successfully', 'success')
            else:
                flash('User can not be found', 'danger')

            return redirect(url_for('allUsers_blueprint.edit_user'))

@blueprint.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'message': 'User not found'}), 404