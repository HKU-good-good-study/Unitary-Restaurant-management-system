import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

secret_key: str = 'secret'

def generate_token(username: str) -> str:
    payload: Dict[str, Any] = {
        'username': username,
        'exp': datetime.now() + timedelta(days=1)
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # Handle expired token
        return None
    except jwt.InvalidTokenError:
        # Handle invalid token
        return None