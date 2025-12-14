from src.modules import *

class Prompt:
    @dataclass
    class Result:
        category: str
        value: any

        def __str__(self):
            if isinstance(self.value, list):
                return "\n".join(str(v) for v in self.value)
            if isinstance(self.value, dict):
                maxKeyLen = max((len(str(k)) for k in self.value.keys()), default=0)
                return "\n".join(f"{str(k).ljust(maxKeyLen)} : {v}" for k, v in self.value.items())
            return str(self.value)

    def __init__(self, env: Env):
        self.env = env
        self.entry = ''
        self.shellCwd = os.getcwd()
        self.moduleManager = ModuleManager(self.shellCwd)
        self.configManager = ConfigManager(self.shellCwd)

        Prompt.instance = self

    def run(self):
        self._host()

    def readEntry(self, cliPrompt: str):
        return input(cliPrompt)

    def buildPrompt(self):
        return StringUtils.addColor(
            f"%BG_BRIGHT_MAGENTA%%BOLD% @{self.configManager.get('title')} %RESET%"
            f"%BG_BLUE% ({os.getcwd()}) %RESET% %GREEN%$%RESET% "
        )

    def _host(self):

        while True:
            cliPrompt = self.buildPrompt()
            self.entry = self.readEntry(cliPrompt)
            parser = Parser(self.entry, self.env)

            try:
                if not parser.pipeline:
                    continue

                result = self.runPipeline(parser.pipeline)
                self.env.session.addToLogs(parser.rawCommand)

                if result is not None:
                    print(Prompt.Result('Pipeline', result))

            except Errors.PastelBaseError as e:
                print(e)

    def runPipeline(self, pipeline: list):
        stdin = None
        for cmd in pipeline:
            if cmd["isVariable"]:
                self.declareVariable(cmd)
                continue

            module = self.moduleManager.load(cmd["name"])
            if not module or not hasattr(module, 'CommandManifest'):
                Errors.PastelCommandError(f"'{cmd['name']}' is not a valid command.").raiseError()

            manifest = self.moduleManager.getManifest(cmd["name"])

            if hasattr(manifest, 'ARGS'):
                requiredArgs = [arg for arg in manifest.ARGS if arg.get('required')]
                if len(cmd["args"]) < len(requiredArgs):
                    missing = [arg['name'] for arg in requiredArgs[len(cmd["args"]):]]
                    Errors.PastelSyntaxError(
                        f"Missing required argument(s) for '{cmd['name']}': {', '.join(missing)}"
                    ).raiseError()

            if hasattr(manifest, 'execute'):
                stdin = manifest.execute(cmd["args"], cmd["flags"], stdin=stdin)
            else:
                Errors.PastelInternalError(f"Missing entrypoint in '{cmd['name']}'").raiseError()

            if cmd["redirects"]:
                for redir in cmd["redirects"]:
                    op = redir["op"]
                    target = redir["target"]
                    mode = "w" if op == ">" else "a"
                    with open(target, mode, encoding="utf-8") as f:
                        f.write(str(stdin) + "\n")

        return stdin


    def declareVariable(self, cmd: dict):
        if cmd["args"]:
            self.env.session.setVariable(cmd["name"], cmd["args"][0] if len(cmd["args"]) == 1 else cmd["args"])
        else:
            Errors.PastelSyntaxError("Malformed variable declaration.").raiseError()
