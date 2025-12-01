from packages.modules import *

class Session:
    def __init__(self):
        self.id = None
        self.variables = {}

    def new(self):
        self.id = f"0x{secrets.token_hex(3).upper()}"
        self.variables = {}

class Env:
    def __init__(self):
        self.session = Session()

    @staticmethod
    def getCommitHash():
        try:
            commitHash = subprocess.check_output(['git', 'describe', '--tags', '--always', '--dirty']).decode('utf-8').strip()
            return commitHash
        except Exception:
            return '0'
