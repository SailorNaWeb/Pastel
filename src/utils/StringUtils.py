import re

class ANSIColors:
    RESET = '\033[0m'

    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'

    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    BG_BRIGHT_BLACK = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'

class StringUtils:
    @staticmethod
    def addColor(string: str) -> str:
        colorPattern = re.compile(r"%([A-Z_]+)%")
        
        def replacer(match):
            token = match.group(1)
            return getattr(ANSIColors, token, match.group(0))
        
        return colorPattern.sub(replacer, string)

    @staticmethod
    def getFriendlyTypeName(typeClass) -> str:
        typeMap = {
            str: "String",
            int: "Integer",
            float: "Float",
            bool: "Boolean",
            list: "List"
        }

        if typeClass is None:
            return "Any"

        if isinstance(typeClass, tuple):
            return "Tuple"

        if typeClass in typeMap:
            return typeMap[typeClass]
    
        if isinstance(typeClass, type):
            return typeClass.__name__.capitalize()

        if isinstance(typeClass, str):
            return typeClass

        return str(typeClass)


    
    @staticmethod
    def buildUsage(manifest):
        usage = manifest.NAME
        for arg in getattr(manifest, 'ARGS', []):
            if arg.get('required', False):
                usage += f" <{arg['name']}: {StringUtils.getFriendlyTypeName(arg['type'])}>"
            else:
                usage += f" [{arg['name']}: {StringUtils.getFriendlyTypeName(arg['type'])}]"
        
        for flag in getattr(manifest, "FLAGS", []):
            usage += f" [-{flag['name']}]"

        return usage