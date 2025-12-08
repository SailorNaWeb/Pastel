from src.modules import *

commandName = os.path.basename(__file__).replace('.py', '')

def default(args=None, flags=None):
    ArgsUtils.boundArgs(commandName, args, 1)

    try:
        os.chdir(args[0])
    except FileNotFoundError:
        Errors.PastelOSError(f"Directory not found.")