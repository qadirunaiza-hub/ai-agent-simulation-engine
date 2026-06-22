"""
User model and file-based storage for MiroFish authentication.
Users stored at backend/uploads/users.json
Default admin: username=admin, password=admin@123
"""

import os
import json
import uuid
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

USERS_FILE = os.path.join(os.path.dirname(__file__), '../../uploads/users.json')
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin@123'


@dataclass
class User:
    user_id: str
    username: str
    email: str
    password_hash: str
    role: str  # 'admin' or 'user'
    created_at: str
    is_active: bool = True

    def to_dict(self) -> Dict:
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at,
            'is_active': self.is_active,
        }

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class UserManager:
    _users: Optional[Dict[str, 'User']] = None

    @classmethod
    def _load(cls) -> Dict[str, 'User']:
        if cls._users is not None:
            return cls._users
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            cls._users = {uid: User(**u) for uid, u in data.items()}
        else:
            cls._users = {}
        return cls._users

    @classmethod
    def _save(cls):
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        data = {uid: asdict(u) for uid, u in cls._users.items()}
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def seed_admin(cls):
        """Ensure default admin user exists."""
        users = cls._load()
        existing_admin = next((u for u in users.values() if u.role == 'admin'), None)
        if not existing_admin:
            admin = User(
                user_id=str(uuid.uuid4()),
                username=ADMIN_USERNAME,
                email='admin@mirofish.local',
                password_hash=generate_password_hash(ADMIN_PASSWORD),
                role='admin',
                created_at=datetime.now().isoformat(),
                is_active=True,
            )
            users[admin.user_id] = admin
            cls._save()

    @classmethod
    def get_by_username(cls, username: str) -> Optional['User']:
        return next((u for u in cls._load().values() if u.username == username), None)

    @classmethod
    def get_by_id(cls, user_id: str) -> Optional['User']:
        return cls._load().get(user_id)

    @classmethod
    def create_user(cls, username: str, email: str, password: str, role: str = 'user') -> 'User':
        users = cls._load()
        if any(u.username == username for u in users.values()):
            raise ValueError(f'Username already taken: {username}')
        user = User(
            user_id=str(uuid.uuid4()),
            username=username,
            email=email or f'{username}@mirofish.local',
            password_hash=generate_password_hash(password),
            role=role,
            created_at=datetime.now().isoformat(),
            is_active=True,
        )
        users[user.user_id] = user
        cls._save()
        return user

    @classmethod
    def list_users(cls) -> List['User']:
        return list(cls._load().values())
