from src.modules import *
from src.core import Prompt

# Um adentro aqui, é sempre bom usar "magic values" (sla se o termo existe, derivei de "magic numbers"), q é basicamente você colocar valos fixos
# (nesse caso opções de um switch case) em variáveis bem definidas, deixa mais bonito :)

class Options:
    EDIT_THEME = "et"
    TITLE = "title"
    HELP = "h"

MENU_AJUDA = "Bem-vindo ao centro de configuração do pastel\nComandos:\n\net : Configuração do tema\n\t uso: pastel et [elemento a ser editado]\nh : Mostra esse menu\n"

commandName = os.path.basename(__file__).replace('.py', '')

def default(args: None, flags: None) :
    if len(args) > 0 :
        match args[0]:
            case Options.HELP:
                print(MENU_AJUDA)
            case Options.EDIT_THEME:
                if len(args) > 1:
                    match args[1]:
                        case Options.TITLE:
                            if len(args) > 2:
                                changeTitle(args[2])
                            else :
                                print("Insira o novo título: ")
                                title = input()
                                changeTitle(title)

    else :
        print(MENU_AJUDA)

def changeTitle(title):
    Prompt.Prompt.prompt.updateConfig("title", title)
