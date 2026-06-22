"""
Token-based authentication utilities.
Tokens live in memory (token_str -> {user_id, expires}).
"""

import uuid
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional, Dict, Any

from flask import request, jsonify

_tokens: Dict[str, Dict[str, Any]] = {}
TOKEN_TTL_HOURS = 24 * 7  # 1 week


def generate_token(user_id: str) -> str:
    token = str(uuid.uuid4())
    _tokens[token] = {'user_id': user_id, 'expires': datetime.now() + timedelta(hours=TOKEN_TTL_HOURS)}
    return token


def revoke_token(token: str):
    _tokens.pop(token, None)


def get_current_user():
    """Extract and validate Bearer token from request. Returns User or None."""
    from ..models.user import UserManager
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None
    token = auth[7:]
    entry = _tokens.get(token)
    if not entry or datetime.now() > entry['expires']:
        _tokens.pop(token, None)
        return None
    return UserManager.get_by_id(entry['user_id'])


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'success': False, 'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'success': False, 'error': 'Authentication required'}), 401
        if user.role != 'admin':
            return jsonify({'success': False, 'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated
