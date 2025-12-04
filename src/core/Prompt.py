import json
import os

from src.modules import *

class Prompt:

    def __init__(self):
        
        with open("src/config/core.json", "r") as core_file: # Fazer um try catch pra pegar exception dps, sepá fazer um gerador do core se ele nn exisitir
            core_data = json.load(core_file)
            
            with open("src/config/" + core_data["config"] + ".json", "r") as config_file:
                self.config_data = json.load(config_file)

        self.entry = ''
        self._host()

    def _host(self):
        env.session.new()
        cliPrompt = StringUtils.addColor(f'%BG_BRIGHT_MAGENTA%%BOLD% @{self.config_data["title"]} %RESET%%BG_BLUE% ({os.getcwd()}) %RESET% %GREEN%$%RESET% ')

        while True:
            self.entry = input(cliPrompt)
            command = CommandParser(self.entry, env)

            if command.name.strip() == '':
                continue
            elif command.isVariable:
                command.declareVariable(env)
            else:
                self.loadCommand(command)

    @staticmethod
    def loadCommand(command):
        try:
            moduleName = f"commands.{command.name}"
            modulePath = os.path.join('src', 'commands', f"{command.name}.py")

            if not os.path.exists(modulePath):
                ErrorUtils.ePrint(command.name, 0x010000)
                return

            spec = importlib.util.spec_from_file_location(moduleName, modulePath)
            module = importlib.util.module_from_spec(spec)
                    
            sys.modules[moduleName] = module
            spec.loader.exec_module(module)
                    
            if hasattr(module, 'default'):
                    module.default(command.args, command.flags) 
            else:
                ErrorUtils.ePrint(command.name, 0x040000)

        except Exception as e:
            ErrorUtils.ePrint(command.name, 0x040001, e)
