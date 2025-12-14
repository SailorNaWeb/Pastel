from src.utils.StringUtils import StringUtils

class Logger:
    @staticmethod
    def info(message: str):
        print(StringUtils.addColor(f"%BOLD%%BG_BLUE% @pastel INFO! %RESET% : %CYAN%{message}%RESET%"))

    @staticmethod
    def warn(message: str):
        print(StringUtils.addColor(f"%BOLD%%BG_YELLOW% @pastel WARN! %RESET% : %YELLOW%{message}%RESET%"))

    @staticmethod
    def success(message: str):
        print(StringUtils.addColor(f"%BOLD%%BG_GREEN% @pastel OK! %RESET% : %GREEN%{message}"))