from src.modules import *
from src.core.system.Lexer import Lexer, Token
class Parser:
    def __init__(self, rawCommand: str, env: Env = None):
        self.rawCommand = rawCommand.strip()
        self.pipeline: List[dict] = []
        self.env = env
        self._parse()

    def _parse(self):
        try:
            tokens = self._tokenize(self.rawCommand)
            if not tokens:
                return

            currentCmd = {"name": "", "args": [], "flags": [], "redirects": [], "isVariable": False}

            for token in tokens:
                if token.tokenType == "COMMAND":
                    if currentCmd["name"]:
                        self._finalizeArgs(currentCmd)
                        self.pipeline.append(currentCmd)
                        currentCmd = {"name": "", "args": [], "flags": [], "redirects": [], "isVariable": False}
                    currentCmd["name"] = token.tokenValue

                elif token.tokenType == "VARIABLE":
                    if not currentCmd["name"]:
                        currentCmd["name"] = token.tokenValue
                        currentCmd["isVariable"] = True
                    else:
                        currentCmd["args"].append(self._resolveValue(token.tokenValue))

                elif token.tokenType in ("FLAG", "LONG_FLAG"):
                    currentCmd["flags"].append(token.tokenValue)

                elif token.tokenType == "REDIRECT":
                    currentCmd["redirects"].append(token.tokenValue)

                elif token.tokenType == "PIPE":
                    if currentCmd["name"]:
                        self._finalizeArgs(currentCmd)
                        self.pipeline.append(currentCmd)
                    currentCmd = {"name": "", "args": [], "flags": [], "redirects": [], "isVariable": False}

                elif token.tokenType == "ARG":
                    currentCmd["args"].append(self._resolveValue(token.tokenValue))

            if currentCmd["name"]:
                self._finalizeArgs(currentCmd)
                self.pipeline.append(currentCmd)

        except Errors.PastelBaseError as e:
            print(e)
            raise

    def _tokenize(self, command: str) -> List[Token]:
        lexer = Lexer(command)
        return lexer.tokenize()

    def _resolveValue(self, value: str):
        if self.env and isinstance(value, str) and value.startswith('@'):
            return self.env.session.getVariable(value)
        return self._convertValue(value)

    def _convertValue(self, value: str):
        if isinstance(value, str):
            if value.lower() == 'true':
                return True
            if value.lower() == 'false':
                return False
            try:
                if '.' in value:
                    return float(value)
                return int(value)
            except ValueError:
                pass
            try:
                return ast.literal_eval(value)
            except Exception:
                pass
        return value

    def _finalizeArgs(self, cmd: dict):
        if cmd["args"]:
            expr = ''.join(str(a) for a in cmd["args"])
            if any(op in expr for op in ['+', '-', '*', '/', '//', '**', '%']):
                try:
                    tree = ast.parse(expr, mode='eval')
                    cmd["args"] = [eval(compile(tree, filename='<expr>', mode='eval'))]
                except Exception:
                    pass

    def toDict(self) -> dict:
        return {"pipeline": self.pipeline}

    def __repr__(self):
        return f'<Pipeline {self.pipeline}>'
