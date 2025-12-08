import src.core.Errors as Errors
from typing import *

class ArgsUtils:
    @staticmethod
    def boundArgs(commandName: str, args: list, minArgs: int, maxArgs: int = None) -> bool:
        if len(args) < minArgs:
            Errors.PastelCommandError(f"Missing arguments for '{commandName}'.").raiseError()
            return False

        if maxArgs is not None and len(args) > maxArgs:
            Errors.PastelCommandError(f"Exceeded maximum arguments for '{commandName}'.").raiseError()
            return False
        
        return True

    @staticmethod
    def getArgument(args: list, index: int, default=None):
        return args[index] if index < len(args) else default
