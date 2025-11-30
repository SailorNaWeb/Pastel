from packages.modules import *

def main():
    EnvUtils.newSession()

    version = '1.0.0'

    print(f'Pastel - v{version} | Session ID: {EnvUtils.session['id']}\n')

    while True:
        entry = input('@pastel> ').strip()
        command = Parser.parse(entry)

        if command['name'] == 'exit':
            break
        elif command['name'].strip() == '':
            continue
        elif command['name'].startswith('$'):
            if command['args']:
                EnvUtils.session['sessionVariables'].append((command['name'], command['args']))
            else:
                ErrUtils.ePrint(command['name'], 0x000102)
        else:
            try:
                module_name = f"commands.{command['name']}"
                
                if not os.path.exists(os.path.join('commands', f"{command['name']}.py")):
                    ErrUtils.ePrint(command['name'], 0x000100)
                    continue

                spec = importlib.util.spec_from_file_location(module_name, os.path.join('commands', f"{command['name']}.py"))
                module = importlib.util.module_from_spec(spec)
                
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                
                if hasattr(module, 'default'):
                    module.default(command['args'], command['flags']) 
                else:
                    ErrUtils.ePrint(command['name'], 0x000400)

            except Exception as e:
                ErrUtils.ePrint(command['name'], 0x000800, e)

if __name__ == '__main__':
    main()