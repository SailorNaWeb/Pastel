from src.modules import *

commandName = os.path.basename(__file__).replace('.py', '')

def default(args=None, flags=None):
    ArgsUtils.boundArgs(commandName, args, 2)
    configName = ArgsUtils.getArgument(args, 0)
    configValue = ArgsUtils.getArgument(args, 1)

    Prompt.instance.updateConfig(configName, configValue)