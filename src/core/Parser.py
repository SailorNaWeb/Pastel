from src.modules import *

class CommandParser:
    def __init__(self, rawCommand: str, env: Env = None):
        self.rawCommand = rawCommand.strip()
        self.name: str = ''
        self.args: list = []
        self.flags: list[str] = []
        self.isVariable: bool = False
        self.env = env
        self._parse()

    def _parse(self):
        try:
            tokens = self._tokenize(self.rawCommand)
            if not tokens:
                return

            self.name = tokens[0]

            if self.name.startswith('@'):
                self.isVariable = True

            for item in tokens[1:]:
                if item.startswith('-') and not self.isVariable:
                    self.flags.append(item)
                else:
                    self.args.append(self._resolveValue(item))
        except Errors.PastelBaseError as e:
            print(e)

    def _tokenize(self, command: str) -> list[str]:
        try:
            return shlex.split(command)
        except Exception as e:
            Errors.PastelSyntaxError(e).raiseError()

    def _resolveValue(self, value: str):
        if self.env and value.startswith('@'):
            if value in self.env.session.variables:
                return self.env.session.variables[value]
        return self._convertValue(value)

    def _convertValue(self, value: str):
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

        mathOps = ['+', '-', '*', '/', '//', '**', '%']
        if any(op in value for op in mathOps):
            try:
                tree = ast.parse(value, mode='eval')
                return eval(compile(tree, filename='<expr>', mode='eval'))
            except Exception:
                pass

        try:
            return ast.literal_eval(value)
        except Exception:
            pass

        return value

    def declareVariable(self, env: Env):
        if self.isVariable:
            if self.args:
                env.session.variables[self.name] = (self.args[0] if len(self.args) == 1 else self.args)
            else:
                Errors.PastelSyntaxError(f'Malformed variable declaration.').raiseError()

    def toDict(self) -> dict:
        return { 'name': self.name, 'args': self.args, 'flags': self.flags }

    def __repr__(self):
        return f'<Command name={self.name} args={self.args} flags={self.flags}>'
