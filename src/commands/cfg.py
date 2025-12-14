from src.modules import *

class CommandManifest:
    NAME = 'cfg'
    DESCRIPTION = 'Modifies your personal configs.'
    ARGS = [
        {
            'name': 'ConfKey',
            'type': str,
            'required': True,
            'description': 'The config key to be modified'
        },
        {
            'name': 'ConfValue',
            'type': Any,
            'required': True,
            'description': 'Value to be assigned to the key'
        }
    ]
    FLAGS = [
        {
            'name': 'force',
            'type': bool,
            'description': 'Forces the assignment of the key'
        }
    ]

    @staticmethod
    def execute(args=None, flags=None, stdin=None):
        Prompt.instance.configManager.set(args[0], args[1], True if 'force' in flags else False)