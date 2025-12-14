from src.modules import *

class Session:
    def __init__(self):
        self.id = f"0x{secrets.token_hex(8)}"
        self.datetime = datetime.datetime.now()
        self.aliases: Dict[str, str] = {}
        self.variables: Dict[str, Any] = {}
        self.logs: List[str] = []

    def addToLogs(self, log: str):
        self.logs.append(log)

    def setVariable(self, key: str, value: Any):
        if not key.isidentifier():
            Errors.PastelSyntaxError(f"Invalid variable name: '{key}'.").raiseError()
        self.variables[key] = value

    def getVariable(self, key: str, default: Any = None):
        return self.variables.get(key, default)

    def deleteVariable(self, key: str):
        if key in self.variables:
            del self.variables[key]

    def listVariables(self) -> Dict[str, Any]:
        return dict(self.variables)
    
    def setAlias(self, name: str, command: str, availableCommands: List[str]):
        if command in availableCommands:
            self.aliases[name] = command
        else:
            Errors.PastelCommandError(f'Cannot create alias: command {command} not found.')

    def getAlias(self, name: str):
        return self.aliases.get(name)

    def deleteAlias(self, name: str):
        if name in self.aliases:
            del self.aliases[name]

    def listAliases(self):
        return dict(self.aliases)

    def reset(self):
        self.id = f"0x{secrets.token_hex(8)}"
        self.datetime = datetime.datetime.now()
        self.variables = {}
        self.logs = []

class Env:
    def __init__(self):
        self.session: Session = Session()

    @staticmethod
    def getCommitHash() -> str:
        try:
            commitHash = subprocess.check_output(['git', 'describe', '--tags', '--always', '--dirty'], stderr=subprocess.DEVNULL).decode('utf-8').strip()
            return commitHash
        except (subprocess.CalledProcessError, FileNotFoundError):
            return 'unknown'
