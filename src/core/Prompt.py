from src.modules import *

class Prompt:
    @dataclass
    class Result:
        category: str
        value: Any

        def __str__(self):
            if isinstance(self.value, list):
                return "\n".join(str(v) for v in self.value)
            
            if isinstance(self.value, dict):
                maxKeyLen = max((len(str(k)) for k in self.value.keys()), default=0)
                return "\n".join(f"{str(k).ljust(maxKeyLen)} : {v}" for k, v in self.value.items())
            
            return str(self.value)

    def __init__(self):
        Prompt.instance = self
        self.shellCwd = os.getcwd()
        self.entry = ''

        # gerador de core feito :>
        try: # tenta abrir arquivo do core
            with open(f'{self.shellCwd}/src/config/core.json', 'r') as coreFile:
                self.coreData = json.load(coreFile)
        except FileNotFoundError: # se não existir, cria um core basico
            self.coreData = {'config': 'default'}
            with open(f'{self.shellCwd}/src/config/core.json', 'w') as coreFile:     
                json.dump(self.coreData, coreFile, indent=4)
            
        with open('src/config/' + self.coreData['config'] + '.json', 'r') as configFile:
            self.configData = json.load(configFile)
        
        self._host()

    def _host(self):
        env.session.new()

        while True:
            cliPrompt = StringUtils.addColor(f"%BG_BRIGHT_MAGENTA%%BOLD% @{self.configData['title']} %RESET%%BG_BLUE% ({os.getcwd()}) %RESET% %GREEN%$%RESET% ")

            self.entry = input(cliPrompt)
            command = CommandParser(self.entry, env)

            try:
                if command.name.strip() == '':
                    continue
                elif command.isVariable:
                    command.declareVariable(env)
                else:
                    self.loadCommand(command)
            except Errors.PastelBaseError as e:
                print(e)

    def updateConfig(self, variable, value):
        self.configData[variable] = value # Tem q fazer umas verificações aqui

        with open(f"{self.shellCwd}/src/config/" + self.coreData["config"] + ".json", "w") as configFile:
            json.dump(self.configData, configFile, indent=4)

    def loadCommand(self, command):
        try:
            moduleName = f"commands.{command.name}"
            modulePath = os.path.join(self.shellCwd, 'src', 'commands', f"{command.name}.py")

            if not os.path.exists(modulePath):
                Errors.PastelCommandError(f"'{command.name}' is not a valid command.").raiseError()

            spec = importlib.util.spec_from_file_location(moduleName, modulePath)
            module = importlib.util.module_from_spec(spec)
                    
            sys.modules[moduleName] = module
            spec.loader.exec_module(module)
                    
            if hasattr(module, 'default'):
                result = module.default(command.args, command.flags)
                if result is not None: 
                    print(Prompt.Result(command.name, result))
            else:
                Errors.PastelInternalError(f"Missing 'default()' function in '{command.name}'").raiseError()

        except Exception as e:
            Errors.PastelInternalError(f"An internal error occurred while executing '{command.name}':\n{e}").raiseError()
