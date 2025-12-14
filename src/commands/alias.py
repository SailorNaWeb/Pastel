from src.modules import *

class CommandManifest:
    NAME = 'alias'
    DESCRIPTION = 'Manages command aliases in the current Pastel session.'
    ARGS = [
        {
            'name': 'AliasOperation',
            'type': str,
            'required': True,
            'description': "Can be 'add' (to create new aliases), 'del' (to delete existing aliases), and 'list' (to list all current aliases)"
        },
        {
            'name': 'AliasName',
            'type': str,
            'required': False,
            'description': 'Alias name'
        },
        {
            'name': 'AliasCommand',
            'type': str,
            'required': False,
            'description': "Command expansion (only for 'add')"
        }
    ]
    FLAGS = []

    @staticmethod
    def execute(args=None, flags=None, stdin=None):
        aliasOp = args[0]

        if aliasOp == 'add':
            if len(args) < 2:
                Logger.warn(f"Argument '{CommandManifest.ARGS[1]['name']}' not provided.")
                return
            
            if len(args) < 3:
                Logger.warn(f"Argument '{CommandManifest.ARGS[2]['name']}' not provided.")
                return
                
            env.session.setAlias(args[1], args[2], Prompt.instance.moduleManager.listCommands())
        
        if aliasOp == 'del':
            if len(args) < 2:
                Logger.warn(f"Argument '{CommandManifest.ARGS[1]['name']}' not provided.")
                return
                
            env.session.deleteAlias(args[1])
        
        if aliasOp == 'list':
            aliases = env.session.listAliases()
            if aliases:
                return "\n".join([f"{k}='{v}'" for k, v in aliases.items()])
            else:
                Logger.warn('No aliases defined in this session.')