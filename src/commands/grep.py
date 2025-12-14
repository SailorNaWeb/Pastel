from src.modules import *
import os

class CommandManifest:
    NAME = 'grep'
    DESCRIPTION = 'Filters input, arguments, or files, returning only lines that contain the given pattern.'
    ARGS = [
        {
            'name': 'Pattern',
            'type': str,
            'required': True,
            'description': 'Text or expression to search for'
        },
        {
            'name': 'File',
            'type': str,
            'required': False,
            'description': 'Optional file path to search in'
        },
    ]
    FLAGS = [
        {
            'name': 'ignore-case',
            'type': bool,
            'description': 'Perform case-insensitive search'
        }
    ]

    @staticmethod
    def execute(args, flags, stdin=None):
        if not args:
            return ''

        pattern = str(args[0])
        lines = []
        
        if stdin:
            if isinstance(stdin, str):
                lines = stdin.splitlines()
            elif isinstance(stdin, list):
                lines = list(map(str, stdin))

        if len(args) > 1:
            filePath = str(args[1])
            
            if os.path.exists(filePath):
                if os.path.isfile(filePath):
                    with open(filePath, 'r', encoding='utf-8') as f:
                        lines.extend(f.read().splitlines())
                else:
                    Errors.PastelOSError(f"'{filePath}' is not a regular file.").raiseError()
            else:
                Errors.PastelOSError(f"File '{filePath}' doesn't exists.").raiseError()

        results = []
        for line in lines:
            if 'ignore-case' in flags:
                if pattern.lower() in line.lower():
                    results.append(line)
            else:
                if pattern in line:
                    results.append(line)

        return '\n'.join(results)
