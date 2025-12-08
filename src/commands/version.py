from src.modules import *

commandName = os.path.basename(__file__).replace('.py', '')

def default(args=None, flags=None):
    ArgsUtils.boundArgs(commandName, args, 0)
    
    message = env.getCommitHash()
    return message