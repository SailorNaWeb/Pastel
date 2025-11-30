from packages.modules import *

def default(args=None, flags=None):
    if args:
        print(' '.join(args))
    else:
        ErrUtils.ePrint(os.path.basename(__file__).replace('.py', ''), 0x000101)