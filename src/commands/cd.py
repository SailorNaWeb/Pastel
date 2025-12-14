from src.modules import *

class CommandManifest:
    NAME = 'cd'
    DESCRIPTION = 'Changes your current directory.'
    ARGS = [
        {
            'name': 'DirName',
            'required': True,
            'type': str,
            'description': 'Directory to be acessed'
        }
    ]
    FLAGS = []

    def execute(args=None, flags=None, stdin=None):
        try:
            os.chdir(args[0])
        except FileNotFoundError:
            Errors.PastelOSError(f"Directory '{args[0]}' not found.").raiseError()
        except PermissionError:
            Errors.PastelOSError(f"Not enough permissions to access '{args[0]}'")