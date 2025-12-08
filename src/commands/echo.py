from src.modules import *

commandName = os.path.basename(__file__).replace('.py', '')

def default(args=None, flags=None):
    ArgsUtils.boundArgs(commandName, args, 1)

    return str(' '.join(map(str, args)))