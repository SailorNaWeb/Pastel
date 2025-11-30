from packages.modules import *

session = {
    'id': None,
    'sessionVariables': []
}

def newSession():
    session['id'] = f'0x{str(secrets.token_hex(3)).upper()}'
    session['sessionVariables'].clear()