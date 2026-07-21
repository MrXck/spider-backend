import datetime

import jwt

JWT_SALT = 'fgdkljdlkfa#^&%^@$^!*^*($&@fdiskhgjfkdhfidofds*&^%&$%&'


def create_token(user_id, timeout=120):
    headers = {
        'type': 'jwt',
        'alg': 'HS256'
    }
    payload = {'data': user_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)}
    result = jwt.encode(payload=payload, key=JWT_SALT, algorithm='HS256', headers=headers)
    return result


def parse_payload(token):
    result = {
        'status': False,
        'data': None,
        'error': None
    }

    try:
        verified_payload = jwt.decode(token, JWT_SALT, algorithms='HS256')
        result['status'] = True
        result['data'] = verified_payload
    except jwt.exceptions.ExpiredSignatureError:
        result['error'] = 'token已失效'
    except jwt.DecodeError:
        result['error'] = 'token认证失败'
    except jwt.InvalidTokenError:
        result['error'] = '非法的token'
    return result
