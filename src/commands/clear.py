from src.modules import *

class CommandManifest:
    NAME = 'clear'
    DESCRIPTION = 'Cleans the terminal screen.'
    ARGS = []
    FLAGS = []

    @staticmethod
    def execute(args=None, flags=None, stdin=None):
        return '\033[3J\033[H\033[2J'