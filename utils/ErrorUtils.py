from utils.Errors import *

class ErrorUtils:
    def __init__(self):
        self.errorCodes = ErrorCodes().errorCodes

    def getErrorByCode(self, targetCode: int) -> Error | None:
        for err in self.errorCodes:
            if err.code == targetCode:
                return err
        return None

    def ePrint(self, cmdName: str, targetCode: int, exc: Exception | None = None):
        err = self.getErrorByCode(targetCode) or self.getErrorByCode(0x000000)

        description = err.description.replace("&cmd_name&", cmdName).replace("&unkwn_err&", str(targetCode))
        message = f"pastel ERR! {err.stringCode} ({hex(err.code)}): {description}"

        if exc:
            message += f" Exception: {exc}"

        print(message.strip())
