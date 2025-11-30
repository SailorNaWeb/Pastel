from packages.modules import *
import utils.env as EnvUtils

def parse(command: str):
    cmdDict = command.split(' ')

    commandName = cmdDict[0]
    args = []
    flags = []

    for item in cmdDict[1:]:
        if item.startswith('-') and not commandName.startswith('$'):
            flags.append(item)
        else:
            args.append(item)

    parsedDict = { 'name': commandName, 'args': args, 'flags': flags }
    return parsedDict