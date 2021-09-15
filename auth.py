import json
import os
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
ALGORITHMS =  os.environ["ALGORITHMS"]
API_AUDIENCE =  os.environ["API_AUDIENCE"]


class AuthError(Exception):
    
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():

    auth = request.headers.get('Authorization', None)

    if auth is None:
        raise AuthError("authorization header does not exist", 401)

    split_auth = auth.split(' ')

    if split_auth[0] != 'Bearer' or len(split_auth) != 2:
        raise AuthError("component missing or invalid", 401)

    return split_auth[1]


def check_permissions(permission, payload):

    if 'permissions' not in payload:
        raise AuthError("component missing", 401)

    if permission not in payload['permissions']:
        raise AuthError("Forbidden", 403)

    return True


def verify_decode_jwt(token):
    url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    data=url.read()
    jwks_json = json.loads(data)
    header = jwt.get_unverified_header(token)

    if 'kid' not in header:
        raise AuthError("incorrect header", 401)

    keys={}
    for k in jwks_json['keys']:
        if k['kid'] == header['kid']:
            keys = {
                'kty': k['kty'],
                'kid': k['kid'],
                'use': k['use'],
                'n': k['n'],
                'e': k['e']
            }
    if keys:
        try:
            payload = jwt.decode(
                token,
                keys,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload


        except jwt.ExpiredSignatureError:
            raise AuthError("expired token", 401)

        except jwt.JWTClaimsError:
            raise AuthError("claim error", 401)

        except Exception:
            raise AuthError("unable to decode token for some unknown reason", 401)


    else:
        raise AuthError("key not found", 401)




def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
            except AuthError as ae:
                abort(ae.status_code,ae.error)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator