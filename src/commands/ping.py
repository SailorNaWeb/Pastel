from src.modules import *
from decimal import Decimal, ROUND_DOWN

commandName = os.path.basename(__file__).replace('.py', '')

def default(args=None, flags=None):
    ArgsUtils.boundArgs(commandName, args, 0, 3)
    
    host = ArgsUtils.getArgument(args, 0, 'google.com')
    port = ArgsUtils.getArgument(args, 1, 80)
    timeout = ArgsUtils.getArgument(args, 2, 2)

    start = time.time()
    try:
        sock = socket.create_connection((host, port), timeout)
        sock.close()
        
        end = time.time()
        ping = Decimal((end - start) * 1000).quantize(Decimal('0.00'), rounding=ROUND_DOWN)

        if ping < 50:
            pingColor = '%CYAN%'
        elif ping < 100:
            pingColor = '%GREEN%'
        elif ping < 200:
            pingColor = '%YELLOW%'
        else:
            pingColor = '%RED%'
       
        return StringUtils.addColor(f"{host}:{port} > {pingColor}{ping}ms%RESET%")
    except socket.timeout:
        Errors.PastelNetworkError('Connection timedout.')
    