from packages.modules import *

def default(args=None, flags=None):
    if args:
        print(str(' '.join(map(str, args))))
    else:
        ErrorUtils.ePrint(os.path.basename(__file__).replace('.py', ''), 0x000101)