from src.modules import *

commandName = os.path.basename(__file__).replace('.py', '')

# a sailor vai me matar :sob:

class Options:
    HELP = 'help'
    EDIT_THEME = 'edit-theme'
    TITLE = 'title'

def default(args=None, flags=None):
    HELP_MESSAGE = StringUtils.addColor('''
%BG_BLUE%  Config Hub  %RESET%
    %BRIGHT_BLUE%Welcome to Pastel's Config Hub!%RESET%
    
    %GREEN%Usage%RESET%: %YELLOW%pastel %CYAN%<option> <attr> <value>%RESET%
''')
    
    category = ArgsUtils.getArgument(args, 0)
    attr = ArgsUtils.getArgument(args, 1)
    value = ArgsUtils.getArgument(args, 2)

    if not category or not attr or category == Options.HELP:
        return HELP_MESSAGE

    match category:
        case Options.EDIT_THEME:
            match attr:
                case Options.TITLE:
                    if value:
                        Prompt.instance.updateConfig(Options.TITLE, value)
                    else:
                        value = input(f">> Insert value for '{attr}': ")
                        Prompt.instance.updateConfig(Options.TITLE, value)
