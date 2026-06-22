"""
Authentication API: login, register, logout, me, model-request management.
"""

from flask import Blueprint, request, jsonify
from ..models.user import UserManager
from ..utils.auth_utils import generate_token, revoke_token, get_current_user, login_required, admin_required

auth_bp = Blueprint('auth', __name__)

# In-memory model change requests: [{id, user_id, username, requested_model, status, created_at}]
_model_requests = []


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password required'}), 400
    user = UserManager.get_by_username(username)
    if not user or not user.is_active or not user.check_password(password):
        return jsonify({'success': False, 'error': 'Invalid username or password'}), 401
    token = generate_token(user.user_id)
    return jsonify({'success': True, 'data': {'token': token, 'user': user.to_dict()}})


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password required'}), 400
    if len(username) < 3:
        return jsonify({'success': False, 'error': 'Username must be at least 3 characters'}), 400
    if len(password) < 6:
        return jsonify({'success': False, 'error': 'Password must be at least 6 characters'}), 400
    try:
        user = UserManager.create_user(username=username, email=email, password=password)
        token = generate_token(user.user_id)
        return jsonify({'success': True, 'data': {'token': token, 'user': user.to_dict()}}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 409


@auth_bp.route('/logout', methods=['POST'])
def logout():
    auth = request.headers.get('Authorization', '')
    if auth.startswith('Bearer '):
        revoke_token(auth[7:])
    return jsonify({'success': True})


@auth_bp.route('/me', methods=['GET'])
@login_required
def me():
    user = get_current_user()
    return jsonify({'success': True, 'data': user.to_dict()})


@auth_bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    users = UserManager.list_users()
    return jsonify({'success': True, 'data': [u.to_dict() for u in users]})


# ---- Model change requests ----

@auth_bp.route('/model-request', methods=['POST'])
@login_required
def request_model_change():
    """User submits a request to change the LLM model."""
    import uuid as _uuid
    from datetime import datetime as _dt
    user = get_current_user()
    data = request.get_json() or {}
    model = data.get('model', '').strip()
    if not model:
        return jsonify({'success': False, 'error': 'model is required'}), 400
    req = {
        'id': str(_uuid.uuid4()),
        'user_id': user.user_id,
        'username': user.username,
        'requested_model': model,
        'status': 'pending',
        'created_at': _dt.now().isoformat(),
    }
    _model_requests.append(req)
    return jsonify({'success': True, 'data': req}), 201


@auth_bp.route('/model-requests', methods=['GET'])
@admin_required
def get_model_requests():
    """Admin views all pending model change requests."""
    return jsonify({'success': True, 'data': list(reversed(_model_requests))})


@auth_bp.route('/model-requests/<req_id>/approve', methods=['POST'])
@admin_required
def approve_model_request(req_id: str):
    """Admin approves a model request and applies it."""
    from ..config import Config
    req = next((r for r in _model_requests if r['id'] == req_id), None)
    if not req:
        return jsonify({'success': False, 'error': 'Request not found'}), 404
    req['status'] = 'approved'
    Config.set_runtime_model(req['requested_model'])
    return jsonify({'success': True, 'data': req})


@auth_bp.route('/model-requests/<req_id>/deny', methods=['POST'])
@admin_required
def deny_model_request(req_id: str):
    """Admin denies a model request."""
    req = next((r for r in _model_requests if r['id'] == req_id), None)
    if not req:
        return jsonify({'success': False, 'error': 'Request not found'}), 404
    req['status'] = 'denied'
    return jsonify({'success': True, 'data': req})
