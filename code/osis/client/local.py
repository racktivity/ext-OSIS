from osis.server.base import BaseServer

import logging

logger = logging.getLogger('osis.client.local') #pylint: disable-msg=C0103



class LocalTransport(BaseServer):
    """
    Local transport to the Osis server
    """
    