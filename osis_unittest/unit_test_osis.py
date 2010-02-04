#from pymonkey.InitBase import *
import osis
from pymonkey import q
from pymonkey import i
import unittest
import os
import sys
import time
from osis import init
init(q.system.fs.joinPaths(q.dirs.baseDir, 'libexec','osis'))
from osis.model.serializers import ThriftSerializer
from osis.client.xmlrpc import XMLRPCTransport
from osis.client import OsisConnection
from osis.store.OsisDB import OsisDB
from osis.model.serializers import YamlSerializer
from osis import *
import time

class OsisTest(unittest.TestCase):
    def setUp(self):
        """called before each test."""
        """All preconditions for the test should be checked here"""
        """Create a new database"""
        self.assertEquals(self.isPackageInstalled('osis'),True,'Osis is not installed. Please install and try again')
        self.assertEquals(self.isPackageInstalled('postgresql'),True,'Postgres is not installed. Please install and try again')
        self.assertEquals(self.isPackageInstalled('jdbserver'),True,"jdbserver is  not installed.Please install Jdbserver and try again")
        self.assertEquals(self.isPackageInstalled('jdbclient'),True,"jdbclient is not installed. Please install jdbclient")
        self.assertEquals(self.isPackageInstalled('osis_service'),True,"osis_service is not installed. Please install osis_service")

        sleeptime=3
        q.manage.postgresql8.start()
        if q.jdb.server.__isRunning__()==False:
            q.manage.zookeeper.start()
            time.sleep(2)
            q.jdb.server.getConfigurationFromMasterJDBServer("127.0.0.1")
            q.jdb.server.start()
            
            sleeptime=60

        q.manage.applicationserver.stop()
        self.create_model_file('/opt/qbase3/libexec/osis','test_model.py')

        self.create_osis_db()
        q.manage.applicationserver.start()

        #        self.conn = osisdb.getConnection('main')done server
        osisdb=OsisDB()
        osisdb.addConnection('main', '127.0.0.1', 'osis', 'qbase', 'pass123',
                        "127.0.0.1",2181,"127.0.0.1","osis","qbase","rooter")


        time.sleep(sleeptime)
        self.conn = osisdb.getConnection('main')
        
        self.conn.createObjectTypeByName('testcompany')

        #done client
        osis.init('/opt/qbase3/libexec/osis')

        #client
        self.transport = XMLRPCTransport('http://localhost:8888', 'osis_service')
        #connection = OsisConnection(self.transport, ThriftSerializer)
        #self.companydata=self.get_model_object(connection)
        self.createViewTasklet()

        
    def tearDown(self):
        """called after each test."""
        """Remove the site from apache"""
        q.manage.applicationserver.stop()
        self.remove_views()
        #self.remove_test_file('/opt/qbase3/libexec/osis')
        
    def get_model_object(self,connection,name):
        #q.manage.applicationserver.stop()

        company1 = connection.testcompany.new()
#        employee1 = company1.employees.new(first_name='Zenith', last_name='FSTL')
#        employee1.email_addresses.append('test1@freesystems.biz')
#        employee1.email_addresses.append('test2@freesystems.biz')

        company1 = connection.testcompany.new()
        company1.name=name
        company1.url='http://freesystems.biz'
        
        
        company1.companyId="243875892375893"
        company1.companyIncomeincrore=7.4564564564
        company1.companytype="SMALL"

        employee1 = company1.employees.new()
        employee1.first_name='Free'
        employee1.last_name='Systems'
        employee1.email_addresses.append('one@freesystems.biz')
        employee1.email_addresses.append('two@freesystems.biz')

        employee_address=employee1.address.new()
        employee_address.street='street1'
        employee_address.number = 125
        employee_address.postal_code = 600000
        employee_address.city = 'Bangalore'
        employee1.address=employee_address
        company1.employees.append(employee1)


        return company1
        #self.companydata=company1



    def create_osis_db(self):
        """Create a data base 'osis' and add users to it"""
        manage=q.manage.postgresql8
        # Add user name and password and save
        manage.startChanges()
        manage.cmdb.rootLogin = 'qbase'
        manage.cmdb.rootPasswd = 'rooter'
        manage.cmdb.save()
        manage.applyConfig()
        # Create a new database 'osis'
        if manage.cmdb.databases.has_key('osis')==False:
            manage.startChanges()
            manage.cmdb.addDatabase('osis')
            manage.cmdb.save()
            manage.applyConfig()

    def check_equal(self,companydata,saved_object):
        """check two objects"""
        self.companydata=companydata; #temparary self. otherwise make it local object
        self.assertEqual(saved_object.name,self.companydata.name)
        self.assertEqual(saved_object.url,self.companydata.url)
        
        self.assertEqual(saved_object.companyId,self.companydata.companyId)
        self.assertEqual(saved_object.companyIncomeincrore,self.companydata.companyIncomeincrore)
        self.assertEqual(saved_object.companytype,self.companydata.companytype)

        self.assertEqual(saved_object.employees[0].first_name,self.companydata.employees[0].first_name)
        self.assertEqual(saved_object.employees[0].last_name,self.companydata.employees[0].last_name)
        self.assertEqual(saved_object.employees[0].email_addresses[0],self.companydata.employees[0].email_addresses[0])
        self.assertEqual(saved_object.employees[0].email_addresses[1],self.companydata.employees[0].email_addresses[1])
        saved_address = saved_object.employees[0].address
        self.assertEqual(saved_address.street,self.companydata.employees[0].address.street)
        self.assertEqual(saved_address.number,self.companydata.employees[0].address.number)
        self.assertEqual(saved_address.postal_code,self.companydata.employees[0].address.postal_code)


    def test_save_retrive_object(self):
        """Save retrive Test """
        #q.manage.applicationserver.start()
        #try:
        #    self.create_osis_db()
        #except:
        #    self.assertEqual(True,False)

        connection = OsisConnection(self.transport, ThriftSerializer)
        companydata=self.get_model_object(connection,"freeSystem")
        connection.testcompany.save(companydata)
        saved_object=connection.testcompany.get(companydata.guid)
        self.check_equal(companydata,saved_object)

        yamalconnection=OsisConnection(self.transport, YamlSerializer)
        yamlcompanydata=self.get_model_object(yamalconnection,"bvirtual")
        yamlcompanydata.name="ZenithInfotech"
        connection.testcompany.save(yamlcompanydata)
        yamlsaved_object=connection.testcompany.get(yamlcompanydata.guid)
        self.check_equal(yamlcompanydata,yamlsaved_object)

        ##checking only two field as reference and test with different version
        saved_object.name="zenith"
        saved_object.url="http://aserver.com"
        connection.testcompany.save(saved_object)

        updatedObject=connection.testcompany.get(companydata.guid)

        assert updatedObject.name!=companydata.name,"Not getting updated data"

        #latestobject=connection.testcompany.get(saved_object.guid,saved_object.version)
        #assert latestobject==saved_object,"We have to get"

        oldorginalObject=connection.testcompany.get(companydata.guid,companydata.version)
        assert oldorginalObject==companydata, "Have to get Oldversion data"


    def test_query(self):
        querystring="create table test (Field char(100))"
        querystring2="insert into test (Field) values('test')"
        client = OsisConnection(self.transport, ThriftSerializer)
        try :
            value=client.testcompany.query(querystring)

            try:
                client.testcompany.query(querystring2)
            except:
                ##Message: Known bug so that put into try catch
                pass

            value=client.testcompany.query("select * from test")
        finally:
            client.testcompany.query("drop table test")

        assert value !="", "Not getting any data"



    def test_delete(self):
        """ deletion of object  """

        connection = OsisConnection(self.transport, ThriftSerializer)
        aserverdata=self.get_model_object(connection,"aserver")
        connection.testcompany.save(aserverdata)

        #sundata=self.get_model_object(connection,"sun")
        #connection.testcompany.save(sundata)

        #testata=self.get_model_object(connection,"test")
        #connection.testcompany.save(testata)

        aserverdata2=connection.testcompany.get(aserverdata.guid)
        aserverdata2.name="aserverdata2"
        connection.testcompany.save(aserverdata2)

        aserverdata3=connection.testcompany.get(aserverdata2.guid)
        aserverdata3.name="aserverdata3"
        connection.testcompany.save(aserverdata3);


        connection.testcompany.delete(aserverdata3.guid,aserverdata3.version)
        tempObject=None
        try:
            tempObject=connection.testcompany.get(aserverdata3.guid,aserverdata3.version)
        except:
            pass

        assert tempObject ==None,"Object not deleting"


        tempObject=connection.testcompany.get(aserverdata2.guid)
        assert tempObject==aserverdata2,"have to get next latest version"


        connection.testcompany.delete(aserverdata3.guid)
        tempObject2=None
        tempObject=None
        try:
            tempObject=connection.testcompany.get(aserverdata2.guid,aserverdata2.version)
        except:
            pass
        try:
            tempObject2=connection.testcompany.get(aserverdata.guid,aserverdata.version)
        except:
            pass
        assert (tempObject ==None and tempObject2 ==None), "Should not get any version"

    def create_view(self,objecttype,viewname):
        #Create a view with name test_osis_view for object type testcompany
        #and add two columns creation date and name
        ro_view = self.conn.viewCreate(objecttype,viewname)
        ro_view.setCol('creationdate',q.enumerators.OsisType.DATETIME,False)
        ro_view.setCol('name',q.enumerators.OsisType.STRING,False)
        self.conn.viewAdd(ro_view)


    def create_view2(self,objecttype,viewname):
        ro_view = self.conn.viewCreate(objecttype,viewname)
        ro_view.setCol('companyIncomeincrore',model.Float,False)
        ro_view.setCol('companyId',q.enumerators.OsisType.UUID,False)
        self.conn.viewAdd(ro_view)

    def create_veiew3(self,objecttype,viewname):
        ro_view = self.conn.viewCreate(objecttype,viewname)
        ro_view.setCol('emailaddress',q.enumerators.OsisType.STRING,False)
        self.conn.viewAdd(ro_view)

    def remove_views(self):
        if self.conn.viewExists("testcompany", 'test_osis_views'):
            self.conn.viewDestroy('testcompany','test_osis_views')
        #if self.conn.viewExists("testcompany", 'test_osis_views2'):
        #    self.conn.viewDestroy('testcompany','test_osis_views2')
        if self.conn.viewExists("testcompany", 'test_osis_views3'):
            self.conn.viewDestroy('testcompany','test_osis_views3')

    def test_osis_views_found(self):
        """osis_views: Search for a string in an osis view and check the result"""
        connection = OsisConnection(self.transport, ThriftSerializer)
        filteredlist=[]
        self.create_view('testcompany','test_osis_views')
        #self.create_view2('testcompany','test_osis_views2')
        self.create_veiew3('testcompany','test_osis_views3')

        filterObj = self.conn.getFilterObject()
        filterObj.add('test_osis_views', 'name', 'FreeSystems')
        company1 =self.get_model_object(connection,"freeSystem")
        company1.name='FreeSystems'
        connection.testcompany.save(company1)

        company2=self.get_model_object(connection,"zenith")
        connection.testcompany.save(company2)

        filteredlist=self.conn.objectsFind('testcompany', filterObj)
        print filteredlist
        saved_object=connection.testcompany.get(filteredlist[0])
        #print filteredlist
        self.remove_views()
        self.assertEqual(len(filteredlist),1,'Expected one object with the given name')
        self.assertEqual(saved_object.name,'FreeSystems','Expected name is FreeSystems')




    def remove_osis_db(self):
        manage.startChanges()
        manage.cmdb.removeDatabase('osis')
        manage.cmdb.save()
        manage.applyConfig()

    def isPackageInstalled(self,packagename):
        installedpackages=q.qpackages.listInstalledQPackages()
        found=0;
        for i in installedpackages.keys():
           list1=installedpackages[i]
           listsize=len(list1)
           for j in range(listsize):
               package_version=list1[j]
               if(package_version[0]==packagename):
                  return True
        return False
    
    def create_file(self,path,filename,string):
        #Platform specific code
        #os.makedirs(path) 
        #OS specific code
        filepath=path+'/'+filename
        write_to_file=open(filepath,'w')
        write_to_file.write(string) 
        write_to_file.close

    def create_model_file(self,path,filename):
        string="""
from osis import model
from pymonkey.baseclasses.BaseEnumeration import BaseEnumeration

class companyType(BaseEnumeration):
	@classmethod
	def _initItems(cls):
            cls.registerItem('SMALL')
            cls.registerItem('MEDIUM')
            cls.registerItem('LARGE')
            cls.finishItemRegistration()

class testAddress(model.Model):
      street = model.String(thrift_id=1)
      number = model.Integer(thrift_id=2)
      postal_code = model.Integer(thrift_id=3)
      city = model.String(thrift_id=4)

class testEmployee(model.Model):
      first_name = model.String(thrift_id=1)
      last_name = model.String(thrift_id=2)
      email_addresses = model.List(model.String(), thrift_id=3)
      address = model.Object(testAddress, thrift_id=4)

class testcompany(model.RootObjectModel):
      name = model.String(thrift_id=1)
      url = model.String(thrift_id=2)
      employees = model.List(model.Object(testEmployee), thrift_id=3)
      companyId= model.GUID(thrift_id=4)
      companyIncomeincrore= model.Float(thrift_id=5)
      companytype= model.Enumeration(companyType,thrift_id=6)
      secotr= model.Boolean(thrift_id=7)

      """
        self.create_file(path,filename,string)


    def createViewTasklet(self):
        stringdata="""
__author__ = 'aserver'
__tags__ = 'osis', 'store'
#__priority__ = 4

def main(q, i, params, tags):
    from osis.model.serializers import ThriftSerializer
    from osis.store.OsisDB import OsisDB
    from osis import ROOTOBJECT_TYPES
    import datetime

    osis = OsisDB().getConnection('main')
    rootobject = params['rootobject']
    rootobjecttype = params['rootobjecttype']
    if osis.viewExists(rootobjecttype, 'test_osis_views'):
         osis.viewSave(rootobjecttype, 'test_osis_views', rootobject.guid,
                      rootobject.version, {'creationdate':datetime.datetime.now(),'name':rootobject.name})

#    if osis.viewExists(rootobjecttype,"test_osis_views2"):
#        osis.viewSave(rootobjecttype,"test_osis_views2",rootobject.guid,
#                     rootobject.version,{'companyIncomeincrore':rootobject.companyIncomeincrore,'companyId':rootobject.companyId})

    if osis.viewExists(rootobjecttype,"test_osis_views3"):
        for emp in rootobject.employees:
            for empemailid in emp.email_addresses:
                osis.viewSave(rootobjecttype,"test_osis_views3",rootobject.guid,
                     rootobject.version,{'emailaddress':empemailid})

        """
        folder="/opt/qbase3/apps/applicationserver/services/osis_service/tasklets/generic"
        self.create_file(folder,"saveview.py",stringdata)

"""
    def remove_test_file(self,path):
        #OS specific code
        os.remove(path+'/test111.py')
        os.remove(path+'/test111.pyc')
"""
if __name__ == "__main__":
     osisTestSuite = unittest.TestSuite()
     osisTestSuite.addTest(unittest.makeSuite(OsisTest))
     runner = unittest.TextTestRunner(verbosity=2)
     res=runner.run(osisTestSuite)
     #print res.errors
     #print res.failures
     #print res.testsRun

