errorCodes = [
    { 'code': 0x000000, 'str_code': 'UNKNOWN_CODE', 'description': 'Unknown error code (&unkwn_err&).'},
    { 'code': 0x000100, 'str_code': 'COMMAND_NOT_FOUND', 'description': '\'&cmd_name&\' is not recognized as a command.'},
    { 'code': 0x000101, 'str_code': 'MISSING_ARGUMENTS', 'description': 'Arguments missing for \'&cmd_name&\'.'},
    { 'code': 0x000102, 'str_code': 'MALFORMED_VARIABLE_DECLARATION', 'description': 'Variable \'&cmd_name&\' is malformed.'},
    { 'code': 0x000400, 'str_code': 'COMMAND_DEFAULT_FUNCTION_MISSING', 'description': 'Function \'default()\' in \'&cmd_name&\' is missing.'},
    { 'code': 0x000800, 'str_code': 'INTERNAL_COMMAND_EXCEPTION', 'description': '\'&cmd_name\' failed to execute.'}
]

def getErrorByCode(target_code: int):
    for err in errorCodes:
        if err['code'] == target_code:
            return err
        
    return None

def ePrint(cmd_name: str, target_code: int, exc: Exception | None = None):
    err = getErrorByCode(target_code)
    if not err:
        err = getErrorByCode(0x000000)
    
    description = err['description']
    description = description.replace('&cmd_name&', cmd_name)
    description = description.replace('&unkwn_err&', str(target_code))
    message = f"pastel ERR! {err['str_code']} ({hex(err['code'])}): {description}"

    if exc:
        message += f" Exception: {exc}"

    print(message.strip())
