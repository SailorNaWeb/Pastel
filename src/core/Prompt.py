import json
import os

from src.modules import *

class Prompt:
    prompt = None

    def __init__(self):
        
        with open("src/config/core.json", "r") as core_file: # Fazer um try catch pra pegar exception dps, sepá fazer um gerador do core se ele nn existir
            self.core_data = json.load(core_file)
            
            with open("src/config/" + self.core_data["config"] + ".json", "r") as config_file:
                self.config_data = json.load(config_file)

        self.entry = ''
        Prompt.prompt = self
        self._host()

    def _host(self):
        env.session.new()
        
        while True:
            # Vou deixar aqui dentro, mas seria legal fazer um sistema de eventos para fazer ele atualizar somento quando fosse atualizado

            cliPrompt = StringUtils.addColor(f'%BG_BRIGHT_MAGENTA%%BOLD% @{self.config_data["title"]} %RESET%%BG_BLUE% ({os.getcwd()}) %RESET% %GREEN%$%RESET% ')
            
            self.entry = input(cliPrompt)
            command = CommandParser(self.entry, env)

            if command.name.strip() == '':
                continue
            elif command.isVariable:
                command.declareVariable(env)
            else:
                self.loadCommand(command)
    
    def updateConfig(self, variable, value):
        self.config_data[variable] = value # Tem q fazer umas verificações aqui

        with open("src/config/" + self.core_data["config"] + ".json", "w") as config_file:
            config_file.write(json.dumps(self.config_data))

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
