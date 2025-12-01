from packages.modules import *

def main():
    env.session.new()
    print(f'Pastel - {env.getCommitHash()} | Session ID: {env.session.id}\n')

    while True:
        entry = input('@pastel> ').strip()
        command = CommandParser(entry, env)

        if command.name.strip() == '':
            continue
        elif command.isVariable:
            command.declareVariable(env)
        else:
            try:
                moduleName = f"commands.{command.name}"
                
                if not os.path.exists(os.path.join('commands', f"{command.name}.py")):
                    errorUtils.ePrint(command.name, 0x000100)
                    continue

                spec = importlib.util.spec_from_file_location(moduleName, os.path.join('commands', f"{command.name}.py"))
                module = importlib.util.module_from_spec(spec)
                
                sys.modules[moduleName] = module
                spec.loader.exec_module(module)
                
                if hasattr(module, 'default'):
                    module.default(command.args, command.flags) 
                else:
                    errorUtils.ePrint(command.name, 0x000400)

            except Exception as e:
                errorUtils.ePrint(command.name, 0x000800, e)

if __name__ == '__main__':
    main()