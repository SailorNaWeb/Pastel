from src.modules import *

class ConfigManager:
    def __init__(self, shellCwd: str, coreFile: str = 'core.json'):
        self.configPath = os.path.join(shellCwd, 'src', 'config')
        self.coreFile = coreFile
        self.coreData = {}
        self.configData = {}
        self.loadCore()
        self.loadConfig()

    def loadCore(self):
        corePath = os.path.join(self.configPath, self.coreFile)
        if not os.path.exists(corePath):
            self.coreData = {'config': 'default'}
            self.saveFile(corePath, self.coreData)
        else:
            with open(corePath, "r") as f:
                self.coreData = json.load(f)

    def loadConfig(self):
        configFile = os.path.join(self.configPath, self.coreData['config'] + '.json')
        if not os.path.exists(configFile):
            Errors.PastelInternalError(f"Config file '{configFile}' not found.").raiseError()
        with open(configFile, 'r') as f:
            self.configData = json.load(f)

    def saveFile(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

    def get(self, key, default=None):
        return self.configData.get(key, default)

    def set(self, key, value, force=False):
        if key not in self.configData and not force:
            Errors.PastelCommandError(f"Invalid config key '{key}'.").raiseError()
        self.configData[key] = value
        configFile = os.path.join(self.configPath, self.coreData['config'] + '.json')
        self.saveFile(configFile, self.configData)

    def reload(self):
        self.loadCore()
        self.loadConfig()
