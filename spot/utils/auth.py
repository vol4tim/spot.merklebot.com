import datetime
import hashlib
from settings.settings import ADMIN_ACCOUNTS, AUTH_SECRET
from substrateinterface import Keypair, KeypairType


def generate_auth_token(account):
    today = datetime.datetime.now().date()
    token = hashlib.sha1((AUTH_SECRET + str(today) + account).encode()).hexdigest()
    return token


def verify_token_sign(address, signed_token, token=None):
    if not token:
        token = generate_auth_token(address)
    keypair_public = Keypair(ss58_address=address,
                             crypto_type=KeypairType.SR25519)
    is_verified = keypair_public.verify(token, signed_token)
    return is_verified


def check_if_admin(address):
    return address in ADMIN_ACCOUNTS
