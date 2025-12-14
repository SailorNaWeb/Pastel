from src.modules import *

class CommandManifest:
    NAME = 'help'
    DESCRIPTION = 'Displays information about available commands.'
    ARGS = [
        {
            'name': 'CommandName',
            'type': str,
            'required': False,
            'description': 'Name of a specific command to show details'
        }
    ]
    FLAGS = []

    @staticmethod
    def execute(args=None, flags=None, stdin=None):
        manager = Prompt.instance.moduleManager
        requestedCommandName = args[0] if args and args[0] else None

        if requestedCommandName:
            manifest = manager.getManifest(requestedCommandName)
            if manifest:
                return StringUtils.addColor(CommandManifest._buildCommandInfo(manifest))
            else:
                Logger.warn(f"Command '{requestedCommandName}' not found.")
                return

        Logger.info("To get help with a specific command, type %GREEN%'help [CommandName]'%CYAN%.%RESET%\n")
        
        output = ''
        for cmdName in manager.listCommands():
            manifest = manager.getManifest(cmdName)
            if manifest:
                output += CommandManifest._buildSimpleInfo(manifest) + '\n'

        if not output:
            return 'No valid commands found.'

        return StringUtils.addColor(output)

    @staticmethod
    def _buildCommandInfo(manifest):
        name = getattr(manifest, 'NAME', None)
        description = getattr(manifest, 'DESCRIPTION', None)
        if not name or not description:
            return ''

        output = f"%BRIGHT_BLUE%{name}%RESET%: {description}\n"
        output += f"    %GREEN%Usage:%RESET% {StringUtils.buildUsage(manifest)}\n"

        if getattr(manifest, 'ARGS', None):
            output += '\n%YELLOW%Arguments:%RESET%\n' + '\n'.join(
                f"  - {arg['name']} ({'required' if arg.get('required') else 'optional'}, {StringUtils.getFriendlyTypeName(arg['type'])}): {arg['description']}"
                for arg in manifest.ARGS
            )
        if getattr(manifest, 'FLAGS', None):
            output += '\n%CYAN%Flags:%RESET%\n' + '\n'.join(
                f"  -{flag['name']}: {flag['description']}" for flag in manifest.FLAGS
            )
        return output

    @staticmethod
    def _buildSimpleInfo(manifest):
        name = getattr(manifest, 'NAME', None)
        description = getattr(manifest, 'DESCRIPTION', None)

        if not name or not description:
            return ''

        return f"%BRIGHT_BLUE%{name}%RESET%: {description}"
