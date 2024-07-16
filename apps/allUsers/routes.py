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

@blueprint.route('/edit_user', methods=['POST'])
@login_required
def edit_user():
    user_id = request.form.get('id')
    username = request.form.get('username')
    email = request.form.get('email')

    user = Users.query.get(user_id)
    if user:
        user.username = username
        user.email = email
        db.session.commit()
        flash('User updated successfully!', 'success')
    else:
        flash('User not found.', 'danger')

    return redirect(url_for('allUsers_blueprint.all_users'))

@blueprint.route('/delete/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = Users.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True}), 200
    return jsonify({'success': False, 'message': 'User not found'}), 404

@blueprint.route('/abilitare/<int:user_id>', methods=['POST'])
@login_required
def abilitare_user(user_id):
    if not current_user.is_authenticated:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401

    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Admin privileges required'}), 403

    user = Users.query.get(user_id)
    if user:
        data = request.get_json()
        user.is_admin = data['is_admin'] == 'True'
        db.session.commit()
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'message': 'User not found'}), 404
