import xmlrpclib
from pymonkey import q
from pymonkey.config import ConfigManagementItem, ItemGroupClass

class OsisConnectionConfig(ConfigManagementItem):
    """
    Configuration of an Osis connection
    """
    CONFIGTYPE = "osisconnection"
    DESCRIPTION = "Osis connection"

    def ask(self):
        self.dialogAskString('server', 'Enter (IP) address of the Application Server', "127.0.0.1")
        self.dialogAskInteger('port', 'Enter port of the Application Server', 80)
        self.dialogAskString('path', 'Enter URL path of the XML-RPC transport of the Application Server', '/appserver/xmlrpc/')
        defaultDir = q.system.fs.joinPaths(q.dirs.baseDir, 'libexec','osis')
        self.params['model_path'] = self.params['model_path'] or defaultDir
        self.dialogAskString('model_path', 'Enter dir path of osis model', defaultDir)

    def show(self):
        # Here we do not want to show the password, so a customized show() method
        params = dict(itemname=self.itemname, **self.params)

        q.gui.dialog.message("Osis Connecttion %(itemname)s "
            "(%(server)s:%(port)d%(path)s)" % params
        )

    # Optional implementation of retrieve() method, to be used by find()
    def retrieve(self):
        from osis import init
        init(self.params['model_path'])
        from osis.model.serializers import ThriftSerializer
        from osis.client.xmlrpc import XMLRPCTransport
        from osis.client import OsisConnection
        transport = XMLRPCTransport('http://%s:%s/%s'%(self.params['server'], self.params['port'], self.params['path']), 'osis_service')
        connection = OsisConnection(transport, ThriftSerializer)

        return connection

OsisConnectionsConfig = ItemGroupClass(OsisConnectionConfig)