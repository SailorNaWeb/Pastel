from packages.modules import *

@dataclass
class Error:
    code: int
    stringCode: str
    description: str

class ErrorCodes:
    def __init__(self):
        self.errorCodes = [
            Error(0x000000, "UNKNOWN_CODE", "Unknown error code (&unkwn_err&)."),
            Error(0x000100, "COMMAND_NOT_FOUND", "'&cmd_name&' is not recognized as a command."),
            Error(0x000101, "MISSING_ARGUMENTS", "Arguments missing for '&cmd_name&'."),
            Error(0x000102, "MALFORMED_VARIABLE_DECLARATION", "Variable '&cmd_name&' is malformed."),
            Error(0x000400, "COMMAND_DEFAULT_FUNCTION_MISSING", "Function 'default()' in '&cmd_name&' is missing."),
            Error(0x000800, "INTERNAL_COMMAND_EXCEPTION", "'&cmd_name&' failed to execute.")
        ]