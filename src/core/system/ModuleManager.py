from src.modules import *

class ModuleManager:
    def __init__(self, shellCwd: str):
        self.shellCwd = shellCwd
        self.cache = {}

    def load(self, commandName: str):
        if commandName in self.cache:
            return self.cache[commandName]

        commandsDir = os.path.join(self.shellCwd, 'src', 'commands')
        modulePath = os.path.join(commandsDir, f"{commandName}.py")

        if not os.path.exists(modulePath):
            return None

        spec = importlib.util.spec_from_file_location(f"commands.{commandName}", modulePath)
        if spec is None:
            Errors.PastelInternalError(f"Failed to create spec to '{commandName}'.").raiseError()
            return None

        module = importlib.util.module_from_spec(spec)
        sys.modules[f"commands.{commandName}"] = module

        try:
            spec.loader.exec_module(module)
            self.cache[commandName] = module
            return module
        except Exception as e:
            Errors.PastelInternalError(f"An internal error occurred while executing '{commandName}':\n{e}").raiseError()
            return None

    def getManifest(self, commandName: str):
        module = self.load(commandName)
        if module and hasattr(module, "CommandManifest"):
            return module.CommandManifest
        return None

    def listCommands(self):
        commandsDir = os.path.join(self.shellCwd, "src", "commands")
        return [f.replace('.py', '') for f in os.listdir(commandsDir) if f.endswith('.py')]
