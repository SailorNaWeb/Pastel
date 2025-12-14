from src.modules import *
from decimal import Decimal, ROUND_DOWN

class CommandManifest:
    NAME = 'ping'
    DESCRIPTION = 'Measures network latency via the TCP handshake duration.'
    ARGS = [
        {
            'name': 'NetworkAddress',
            'type': str,
            'required': True,
            'description': 'Hostname or IP address to measure'
        },
        {
            'name': 'Port',
            'type': int,
            'required': False,
            'description': 'The specific service port number to connect to (e.g., 80 for HTTP, 443 for HTTPS, 22 for SSH)'
        }
    ]

    @staticmethod
    def execute(args=None, flags=None, stdin=None):
        host = args[0]
        port = args[1] if len(args) > 1 else 80
        start = time.time()
        
        try:
            sock = socket.create_connection((host, port), 2)
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
        