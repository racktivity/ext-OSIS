# Author: Sneha Shinjani [Free System Technology Labs]
# Last Updated: 30 - 06 - 2009
# Tutorial on Application Server & Osis

from pymonkey import q
from pymonkey import i
import re
import sys
import xmlrpclib
import osis
from osis.client import OsisConnection
from osis.client.xmlrpc import XMLRPCTransport
from osis.store.OsisDB import OsisDB
from osis.model.serializers import ThriftSerializer
import urllib2
#from pymonkey.baseclasses.CMDBServerObject import CMDBServerObject


class applicationserver:
    def sequence (self):
        '''This function provides you with correct sequence of execution of q.tutorial.applicationserver commands. You can view the correct sequence\
        as well as execute according to the sequence by selecting choices from menu. '''
        choices = ['Configure','Start','CreateService','TestServiceRest','TestServiceXML','CreateServiceAuthenticated','TestServiceAuthenticated']
        choice = q.gui.dialog.askChoiceMultiple('Application Server Sequence is as follows. Which do u want to execute?',choices)
        if choice == ['Configure']:
            q.tutorial.applicationserver.config()
        elif choice == ['Start']:
            q.tutorial.applicationserver.start()
        elif choice == ['CreateService']:
            q.tutorial.applicationserver.createService()
        elif choice == ['TestServiceRest']:
            q.tutorial.applicationserver.testServiceRest()
        elif choice == ['TestServiceXML']:
            q.tutorial.applicationserver.testServiceXmlrpc()
        elif choice == ['CreateServiceAuthenticated']:
            q.tutorial.applicationserver.createServiceAuthenticated()
        elif choice == ['TestServiceAuthenticated']:
            q.tutorial.applicationserver.testServiceAuthenticateRest()
    def config(self):
        '''After Installation Application Server needs to be configured, to assign various ports, etc. This commands helps you to configure Application\
         Server as well as verification of its configuration\nPrerequisites: Installation Procedure Complete'''
        print '\n\033[1;34mConfiguring Application Server:\n\n\033[1;32m[ ]i.servers.applicationserver.review()\n'
        i.servers.applicationserver.review()
        print '\n\033[1;34mTo check the Application service configuration use:\n\033[1;32m[ ]i.servers.applicationserver.getConfig()\n'
        print i.servers.applicationserver.getConfig()
        print '\n\033[1;34m rest_ip: 127.0.0.1\n rest_port: 8889\n xmlrpc_ip: 0.0.0.0\n xmlrpc_port: 8088\nMake a note of these ports\n'
        
    def start(self):
        '''This Command helps you to start Application Server and check its status.\nPrerequisites: Configure Application server '''
        print '\n\033[1;34mStarting Application Server:\n\n\033[1;32m[ ]q.manage.applicationserver.start()\n' 
        q.manage.applicationserver.start()
        print '\n\033[1;34m Check Status of Application Server:\n\n\033[1;32m[ ]q.manage.applicationserver.isRunning()\n'
        print q.manage.applicationserver.isRunning()
    
    def createService(self):
        '''This command helps you to create and register your own service in application server. User can create any functionality within the\
        application server and use it through REST/XML-RPC/EMAIL Interface.\n Prerequisites: Configure & Start Application Server '''
        print '\n\033[1;34mWrite a python script with at least one Class and one/more modules implementing the desired functionality.'
        print '\n\033[1;34mTake Example case of a service which accepts names & displays Hello <name>.\nCreate a python script:hello.py \n'
        print '\n\033[1;34mMake a folder helloworld @ /opt/qbase3/apps/applicationServer/services/example/ & save hello.py @helloworld\nFile hello.py:\
        \n\033[1;33m'
        try:
	    q.system.process.execute('cat /opt/qbase3/apps/applicationServer/services/example/helloworld/hello.py')
	except Exception,e:
	    print 'Unable to open file hello.py'
	print '\n\033[1;34mNOTE: Every module/method which needs to be exposed to the network, should use the decorator'
        print '\033[1;34m@q.manage.applicationserver.expose\n'
        print '\033[1;34mAdding Service to Application Server\n\n\033[1;32m[ ]i.servers.applicationserver.services.add()\n'
        print '\033[1;34mPlease enter a name for the Application server service: my_service\nService class: example.helloworld.hello.HelloWorld\n'
        i.servers.applicationserver.services.add()
        print '\n\033[1;34mService Class format is path.filename.classname, where path is w.r.t. /opt/qbase3/apps/applicationServer/services/ \n'
        print '\n\033[1;34mView the created service:\n\033[1;32m[ ]i.servers.applicationserver.services.list() \n'
        print i.servers.applicationserver.services.list()
   
    def testServiceRest(self):
        '''Services created in Application Server can be tested/used through REST/XML-RPC/EMAIL Interface. This commands calls a service using REST\
        interface'''
        print '\n\033[1;34mTesting the Created Service in Application Service with Rest Interface  \n'
        print '\n\033[1;32mfh=urllib2.urlopen(\'http://localhost:8889/my_service/hello?names=["John%20Doe","Michael%20Montee"]\')\nstrData = fh.read()\n'
	print '\033[1;32mfh.close()\n'
        import urllib2
	from urllib2 import urlopen
	try:
            fh = urllib2.urlopen('http://localhost:8889/my_service/hello?names=["John%20Doe","Michael%20Montee"]')
	    strData = fh.read()
	    fh.close()
	    print strData
        except Exception,e:
            print 'Unable to open URL'
        print '\n\n\033[1;34mIn this URL, distinguish the following parameters:\n127.0.0.1 / local host: address of the PyMonkey Application Server\n \
        8889: the defined port of the REST interface\nmy_service: name of the service\nhello: name of the method in the Python Class file\n \
        names: name of the argument, used in the method\n\n You will be asked to download the result (json file) of the called method\n'

    def testServiceXmlrpc(self):
        '''Services created in Application Server can be tested/used through REST/XML-RPC/EMAIL Interface. This commands calls a service using XML_RPC\
        interface'''
        print '\n\033[1;34mTesting the Created Service in Application Service with XML-RPC Interface  \n'
        print '\n\033[1;34m!firefox http://127.0.0.1:8888/my_service/hello?names=["John Doe","Michael Montee"] &\n'
        import urllib2
	from urllib2 import urlopen
	try:
            fh = urllib2.urlopen('http://localhost:8888/my_service/hello?names=["John%20Doe","Michael%20Montee"]')
	    strData = fh.read()
	    fh.close()
	    print strData
        except Exception,e:
            print 'Unable to open URL'
        print '\n\n\033[1;34mIn this URL, distinguish the following parameters:\n127.0.0.1 / local host: address of the PyMonkey Application Server\n \
        8088: the defined port of the XML-RPC interface\nmy_service: name of the service\nhello: name of the method in the Python Class file\n \
        names: name of the argument, used in the method\n\n You will be asked to download the result (json file) of the called method\n'

    def createServiceAuthenticated(self):
        '''This function helps you to create a authenticated service, i.e. add authentication to your service. Authentication enables the service to\
        be available only to a specified group of user, who can provide correct username & password '''
        print '\n\033[1;34mWrite a python script with at least one Class and one/more modules implementing the desired functionality.'
        print '\n\033[1;34mTake Example case of a service which accepts names & displays Hello <name>.\nCreate a python script:hello_authenticate.py \n'
        print '\n\033[1;34mSave hello_authenticate.py @ /opt/qbase3/apps/applicationServer/services/example/helloworld\nFile hello_authenticate.py:\n'
        try:
            q.system.process.execute('cat /opt/qbase3/apps/applicationServer/services/example/helloworld/hello_authenticate.py')
        except Exception,e:
	    print 'Unable to open file hello_authenticate.py'
        print '\n\033[1;34mNOTE: Every module/method which needs to be exposed to the network, should use the decorator \
               @q.manage.applicationserver.expose_authenticated, The function checkAuthentication checks authentication when module is called\n'
        print '\033[1;34mAdding Service to Application Server\n\n\033[1;32m[ ]i.servers.applicationserver.services.add()\n'
        print '\033[1;34mPlease enter a name for the Application server service:\033[1;33mmy_service_authent\n'
        print '\033[1;34mService class :\033[1;33mexample.helloworld.hello_authenticate.HelloWorld\n\033[1;34m'
        i.servers.applicationserver.services.add()
        print '\n\033[1;34mService Class format is path.filename.classname, where path is w.r.t. /opt/qbase3/apps/applicationServer/services/ \n'
        print '\n\033[1;34mView the created service:\n\033[1;32m[ ]i.servers.applicationserver.services.list() \n'
        print i.servers.applicationserver.services.list()

    def testServiceAuthenticateRest(self):
        '''This functions enables you to call/test authenticated services in application server. A call to an authenticated service, essentially\
        requires usename and password & gives correct result only if username & password provided are correct'''
        print '\n\033[1;34mTesting the Authenticated Service in Application Service with Rest Interface  \n'
        print '\n\033[1;32mURL http://terry:jones@127.0.0.1:8889/my_service_authent/hello?names=[\'John Doe\',\'Michael Montee\'] \n\033[1;33m'
        try:
            import urllib2
            auth_handler = urllib2.HTTPBasicAuthHandler()
            auth_handler.add_password("Realm here", "localhost", "terry", "jones")
            opener = urllib2.build_opener(auth_handler)
            handle = opener.open('http://localhost:8889/my_service/hello?names=["John%20Doe","Michael%20Montee"]')
            strData = handle.read()
            print strData
        except Exception,e:
            print 'Unable to open URL'
        print '\n\n\033[1;34mIn this URL, distinguish the following parameters:\nterry:jones - username:password\n127.0.0.1/local host: address of'
        print '\033[1;34mthe PyMonkey Application Server\n8889: the defined port of the REST interface\nmy_service: name of the service\n'
        print '\033[1;34mhello: name of the method in the Python Class file\nnames: name of the argument, used in the method\n\n\
        You will be asked to download the result (json file) of the called method\n'

class osisTutorial:
    def sequence (self):
        '''This function provides you with correct sequence of execution of q.tutorial.applicationserver commands. You can view the correct sequence\
        as well as execute according to the sequence by selecting choices from menu. '''
        choices = ['DefineModel','DeployModel','StoreData','RetreiveData','View']
        choice = q.gui.dialog.askChoiceMultiple('OSIS Execution Sequence is as follows. Which do u want to execute?',choices)
        if choice == ['DefineModel']:
            q.tutorial.osis.defineModel()
        elif choice == ['DeployModel']:
            q.tutorial.osis.deployModel()
        elif choice == ['StoreData']:
            q.tutorial.osis.store()
        elif choice == ['RetreiveData']:
            q.tutorial.osis.retreive()
        elif choice == ['View']:
            q.tutorial.osis.view()
                
    def defineModel(self):
        '''When using OSIS, one starts by defining models, which represent the objects to be stored in the Database. This funtion helps you to define\
        a example model, to be used for OSIS Tutorial walkthrough. '''
        print '\n\033[1;34m When using OSIS, one starts by defining models, which represent the objects to be stored in the Database.\n'
        print '\033[1;34mConsider Model example: Database of Companies & their Employees\nCreate a python script: company.py @ /opt/qbase3/libexec/osis\
        \n\033[1;33m'
        try:
            q.system.process.execute('cat /opt/qbase3/libexec/osis/company.py')
        except Exception,e:
            print 'Unable to open file company.py'
        print '\n\033[1;34mDatastructures defined to store data Adress, Employee data & Company data,\
        Root Object being Company which in turn embeds Employee &'
        print '\033[1;34mAddress. thrift_id indicates parameter sequence \n'

    def deployModel(self):
        '''The defined model must be deployed on both the server and the client(s). Model types must be registered with the OSIS server. This function\
        helps you to deploy/register the model in osis as well as in database. It is a prereqisite for using any store/retreive/view functions.  '''
        print '\033[1;34mOSIS Server Setup: Current OSIS server runs inside the PyMonkey Application Server as a Service.\n'
        print '\033[1;34mDatabase Setup: Osis server stores data in postgresql\nSo lets start with setting up postgresql8\n'  
        print '\n\033[1;32m[ ]q.manage.postgresql8.cmdb.rootLogin = \'qbase\' \n[ ]q.manage.postgresql8.cmdb.rootPasswd = \'qbase\'\n'
        print '\033[1;32m[ ]q.manage.postgresql8.cmdb.save()\n[ ]q.manage.postgresql8.applyConfig() \n'
        try:
            q.manage.postgresql8.cmdb.rootLogin = 'qbase'
            q.manage.postgresql8.cmdb.rootPasswd = 'qbase'
        except Exception,e:
	    print '\033[1;33mPostgresql requires group and user accounts.\nLinux users may try:'
	    print '#groupadd qbase\n#useradd qbase'
        #q.manage.postgresql8.cmdb.save()
        q.manage.postgresql8.applyConfig()
        ##if postgresql fails to start using the q.manage commands use
        #q.cmdtools.postgresql8.pg_ctl.start(username)
        print '\n\033[1;34mAdd Database:\n\033[1;32m[ ]q.manage.postgresql8.cmdb.addDatabase(\'osis\')\n'
        q.manage.postgresql8.cmdb.addDatabase('osis')
        #q.manage.postgresql8.cmdb.save()
        q.manage.postgresql8.applyConfig()
        print '\n\033[1;34mView the created Database:\n\033[1;32m[ ]q.manage.postgresql8.cmdb.printDatabases()\n'
        q.manage.postgresql8.cmdb.printDatabases()
        osisdb = OsisDB()
        print '\n\033[1;34mAdd Connection for the database:\n\033[1;32m[ ]osisdb.addConnection(\'main\', \'127.0.0.1\', \'osis\', \'qbase\', \'qbase\')'
        try: 
            osisdb.addConnection('main', '127.0.0.1', 'osis', 'qbase', 'qbase')
            #Register Model on server
            print '\n\033[1;34mGet a connection for the database:\n\033[1;32m[ ]con = osisdb.getConnection(\'main\')\n'
            con = osisdb.getConnection('main')
            print '\n\033[1;34mCreate an object in the database:\n\033[1;32m[ ]con.createObjectTypeByName(\'company\') \n'
            print con.createObjectTypeByName('company')
            con.createObjectTypeByName('company')
            print '\n\033[1;34mInitialise OSIS System: \n\033[1;32m[ ]osis.init(\'/opt/qbase3/libexec/osis\') \n'
            print osis.init('/opt/qbase3/libexec/osis')
        except Exception,e:
	    print 'Connection to OSIS Database Failed. Check if Model file is present'

    def store(self):
        '''This function is used to store data in the database. First a transport is obtained to establish a client connection, and then data is fed\
        & saved in database'''
        print '\n\033[1;34mStores an object in the Database. \n\033[1;33m'
        try:
            transport = XMLRPCTransport('http://localhost:8888', 'osis_service')
            client = OsisConnection(transport,ThriftSerializer)
            company = client.company.new(name='freesystems', url='http://www.freesystems.com')
            employee1 = company.employees.new(first_name='John', last_name='Doe')
            employee1.email_addresses.append('john.doe@aserver.com')
            employee1.email_addresses.append('john@aserver.com')
            client.company.save(company)
        except Exception,e:
            print 'XML-RPC Port could be different\nCheck tasklet folder for save,get,saveview,getview tasklets'
        print company.guid
        comp = client.company.get(company.guid)
        print comp.name
        print comp.url

    def retreive(self):
        '''This function is used to retreive data from the database. First a transport is obtained to establish a client connection, and then data is \
        obtained from the database'''
        print '\n\033[1;34m Retreive the stored object from the Database.\n'
        try:
            transport = XMLRPCTransport('http://localhost:8888', 'osis_service')
            client = OsisConnection(transport,ThriftSerializer)
            filter_ = client.company.getFilterObject()
            filter_.add('name', 'name', 'free') # viewname, fieldname, value
            # Get a list of matching GUIDs
            client.company.find(filter_)
            # Returns a list containing the GUID of the 'Aserver' company
            # Get view information
        except Exception,e:
	    print 'XML-RPC Port could be different\nCheck tasklet folder for save,get,saveview,getview tasklets'
        client.company.find(filter_, 'name')
        results = client.company.find(filter_, 'name')
        for result in results._list[1]:
            for view_row in result:
                print view_row 
	        

    def view(self):
        '''Views allow OSIS users/developers/administrators to define their desired specific ways to query the stored objects.\
        Every view needs to be updated on every store action. '''
        print '\n\033[1;34mRegistering a View \n\033[1;32m[ ]osisdb = OsisDB()\n[ ]conn = osisdb.getConnection(\'main\')\n'
        print '\033[1;32m[ ]view = conn.viewCreate(\'company\', \'name\')\n[ ]view.setCol(\'name\', q.enumerators.OsisType.STRING, False)\n'
        print '[ ]view.setCol(\'url\', q.enumerators.OsisType.STRING, False)\n[ ]conn.viewAdd(view)'
        osisdb = OsisDB()
        try:
            conn = osisdb.getConnection('main')
            view = conn.viewCreate('company', 'name')
            view.setCol('name', q.enumerators.OsisType.STRING, False)
            view.setCol('url', q.enumerators.OsisType.STRING, False)
            conn.viewAdd(view)
        except Exception,e:
            print '\033[1;32mView Already Exists'                
