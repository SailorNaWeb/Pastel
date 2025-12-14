from src.modules import *

class CommandManifest:
    NAME = 'exit'
    DESCRIPTION = 'Exits the current Pastel session.'
    ARGS = []
    FLAGS = []

    @staticmethod
    def execute(args=None, flags=None, stdin=None):
        return sys.exit(0)