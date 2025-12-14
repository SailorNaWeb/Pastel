from src.modules import *

@dataclass
class Token:
    tokenType: str
    tokenValue: Union[str, dict]

class Lexer:
    def __init__(self, source: str):
        self.source = source.strip()

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        rawTokens = shlex.split(self.source, posix=True)

        expectingRedirect = None
        expectCommand = True

        for item in rawTokens:
            if item in ('>', '>>'):
                expectingRedirect = item
                continue

            if expectingRedirect:
                tokens.append(Token("REDIRECT", {"op": expectingRedirect, "target": item}))
                expectingRedirect = None
                continue

            if item == '|':
                tokens.append(Token("PIPE", item))
                expectCommand = True
                continue

            if item.startswith('@'):
                tokens.append(Token("VARIABLE", item))
            elif item.startswith('--'):
                tokens.append(Token("LONG_FLAG", item[2:]))
            elif item.startswith('-'):
                tokens.append(Token("FLAG", item[1:]))
            elif expectCommand:
                tokens.append(Token("COMMAND", item))
                expectCommand = False
            else:
                tokens.append(Token("ARG", item))

        return tokens
