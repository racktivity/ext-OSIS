from osis.server.base import BaseServer, TaskletBasedMixin

import logging

logger = logging.getLogger('osis.client.local') #pylint: disable-msg=C0103



class LocalTransport(TaskletBasedMixin, BaseServer):
    """
    Local transport to the Osis server
    """
    
    def findAsView(self, type_, filter_, view):
        '''Perform a filter operation on the server

        @param type_: Root object type name
        @type type_: string
        @param filter_: Filter definition
        @type filter_: L{OsisFilterObject}
        @param view: View to return
        @type view: string

        @return: List of GUIDs or OsisList of data
        @rtype: list
        '''
        filter_data = filter_.filters

        return BaseServer.findAsView(self, type_, filter_data, view)

   
