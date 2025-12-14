from dataclasses import dataclass
from src.utils.StringUtils import StringUtils

@dataclass
class PastelBaseError(BaseException):
    category: str
    message: str

    def __str__(self):
        return StringUtils.addColor(f'%BOLD%%BG_BRIGHT_RED% @pastel ERR! %RESET%%BOLD%%BG_BRIGHT_BLACK% {self.category} %RESET% : %BRIGHT_RED%{self.message}%RESET%')
    
    def raiseError(self) -> str:
        raise self
    
class PastelSyntaxError(PastelBaseError):
    def __init__(self, message: str):
        super().__init__('SyntaxError', message)


class PastelCommandError(PastelBaseError):
    def __init__(self, message: str):
        super().__init__('CommandError', message)


class PastelNetworkError(PastelBaseError):
    def __init__(self, message: str):
        super().__init__('NetworkError', message)


class PastelOSError(PastelBaseError):
    def __init__(self, message: str):
        super().__init__('OSError', message)


class PastelInternalError(PastelBaseError):
    def __init__(self, message: str):
        super().__init__('InternalError', message)
