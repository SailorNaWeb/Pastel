class CommandManifest:
    NAME = 'echo'
    DESCRIPTION = 'Prints arguments or variables provided by the user.'
    ARGS = [
        {
            'name': 'Text',
            'type': str,
            'required': True,
            'description': 'Text to be printed'
        },
    ]
    FLAGS = [
        {
            'name': 'upper',
            'type': bool,
            'description': 'Convert output to uppercase'
        },
        {
            'name': 'lower',
            'type': bool,
            'description': 'Convert output to lowercase'
        }
    ]

    @staticmethod
    def execute(args, flags, stdin=None):
        flatArgs = []
        if stdin:
            if isinstance(stdin, list):
                flatArgs.extend(map(str, stdin))
            else:
                flatArgs.append(str(stdin))

        for a in args:
            if isinstance(a, list):
                flatArgs.extend(map(str, a))
            else:
                flatArgs.append(str(a))

        text = ' '.join(flatArgs)

        if 'upper' in flags:
            return text.upper()
        if 'lower' in flags:
            return text.lower()
        return text
