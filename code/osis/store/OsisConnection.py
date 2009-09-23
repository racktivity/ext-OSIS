# <License type="Aserver BSD" version="2.0">
# 
# Copyright (c) 2005-2009, Aserver NV.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or
# without modification, are permitted provided that the following
# conditions are met:
# 
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
# 
# * Neither the name Aserver nor the names of other contributors
#   may be used to endorse or promote products derived from this
#   software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY ASERVER "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL ASERVER BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# </License>


import re
import datetime, time

from pymonkey import q
from pymonkey.baseclasses.ManagementApplication import ManagementApplication
from pymonkey.db.DBConnection import DBConnection
from OsisView import OsisView, OsisColumn, OsisType
from OsisFilterObject import OsisFilterObject

from osis.model.serializers import ThriftSerializer
from osis.model.serializers.osisyaml import YamlSerializer
import sys
sys.path.append('/opt/qbase3/apps/kademlia_dht')
import dht_client
from ttypes import *





class _OsisPGTypeConverter(object):
    def __init__(self):
        self._pgType2pyType = {}
        self._pgType2pyType["integer"] = "int"
        self._pgType2pyType["character varying"] = "str"
        self._pgType2pyType["uuid"] = "uuid"
        self._pgType2pyType["timestamp without time zone"] = "datetime"
        self._pgType2pyType["boolean"] = "bool"
        self._pgType2pyType["ARRAY"] = "hex"

    def convertType(self, pgType):
        return self._pgType2pyType[pgType]

osisPGTypeConverter = _OsisPGTypeConverter()

class OsisConnection(object):
    def __init__(self):
        self._dbConn = None
        self._login = None       
        self._ip_for_kad = None
        self._port_for_kad = None
    
    def connect(self, ip, db, login, passwd,isView,port_to_connect=5000,port_to_start=8000):
        """
        Connect to the postgresql server
        
        @param ip : ip of the db server
        @param db : database to connect to
        @param login : login to connect
        @param passwd : password to connect
        """
        self._ip_for_kad=ip
        self._port_for_kad=int(port_to_connect)
        self._login = login
        self._login = login
        if isView :
            self._dbConn = DBConnection('127.0.0.1', 'osis', 'qbase', 'pass123' )
        

    def objectExists(self, objType, guid):
        """
        Checks if an instance of objType with the supplied guid exists
        
        @param objType : type of object to check
        @param guid : unique identifier 
        """
        
        return self.viewObjectExists(objType, 'main', guid)
    
    def viewObjectExists(self, objType, viewName, guid):
        """
        Checks if an instance of objType with the supplied guid exists
        
        @param objType : type of object to check
        @param viewName : view whixh contains the object
        @param guid : unique identifier 
        """
        q.logger.log("select * from only %s.main where guid='%s'"%(objType, guid) ,5)
        result = self._dbConn.sqlexecute("select * from only %s.%s where guid='%s'"%(objType, viewName, guid)).dictresult()
        if result:
            return result[0] > 0
        return False
    
    
    def objectGet(self, objType,guid, version=None):
        """
        Get an instance of objType with the supplied guid
        
        @param objType : type of object to check
        @param guid : unique identifier 
        @param version : unique identifier indicating the version of the object. (Optional)
                         If specified, only the mentioned version will be retrieved, 
                         If ommited, only the active version is retrieved !
        """
        q.logger.log("Getting Object guid= %s "%guid,3)
        if not version:
            guid_arg=guid
            versionValue=dht_client.receive_data( self._ip_for_kad , self._port_for_kad , guid_arg)
            keyValue=guid+str(versionValue.value)
            keyValue=keyValue
        else:
            keyValue=guid+version
            keyValue=keyValue

        result=dht_client.receive_data( self._ip_for_kad , self._port_for_kad , keyValue)

        result=str(result.value)
        if result=="-1":
            return ""
        return result.decode('hex');

    
    
    def objectDelete(self, objType, guid,guidversion):
        """
        Delete an instance of objType with the supplied guid
        
        @param objType : type of object to check
        @param guid : unique identifier 
        """   
       
        return dht_client.remove( self._ip_for_kad , self._port_for_kad , guid)

        if(self.objectExists(objType, guid)):
            self._dbConn.sqlexecute("delete from only %s.main where guid='%s'"%(objType,guid))   
            return True
        else:
            q.eventhandler.raiseCriticalError('%s with guid %s not found.'%(objType, guid))
        
    def objectSave(self,data):
        """
        Update or create the supplied object
        
        @param objType : type of object to check
        @param guid : unique identifier 
        """        
        obj =  self._createObject(data)
        return obj

    
 
    def createObjectType(self, objType):
        """
        Creates the model structure on the database 
        
        @param objType : the object type to create
        """
        objTypeName = objType.__class__.__name__
        self.createObjectTypeByName(objTypeName)
     
    def createObjectTypeByName(self, objTypeName):
        """
        Creates the model structure on the database 
        
        @param objTypeName : the name of the type to create
        """  
        if not self.schemeExists(objTypeName):
            q.logger.log("Creating object schema in database" ,3)
            self._dbConn.sqlexecute('CREATE SCHEMA %s'%objTypeName)
            q.logger.log("Creating object main table in database" ,3)
            self._dbConn.sqlexecute('CREATE TABLE %s.main ( guid uuid NOT NULL, "version" uuid, creationdate timestamp without time zone, data text, CONSTRAINT pk_guid PRIMARY KEY (guid)) WITH (OIDS=FALSE);'%objTypeName)
            q.logger.log("Creating object main archive table in database" ,3)
            self._dbConn.sqlexecute('CREATE TABLE %(scheme)s.main_archive () INHERITS (%(scheme)s.main) WITH (OIDS=FALSE);'%{'scheme':objTypeName})
            q.logger.log("Creating delete rule in database" ,3)
            self._dbConn.sqlexecute('CREATE OR REPLACE RULE %(scheme)s_delete AS ON DELETE TO %(scheme)s.main DO  INSERT INTO %(scheme)s.main_archive (guid, version, creationdate, data) VALUES (old.guid, old.version, old.creationdate, old.data)'%{'scheme':objTypeName})
            q.logger.log("Creating update rule in database" ,3)
            self._dbConn.sqlexecute('CREATE OR REPLACE RULE %(scheme)s_update AS ON UPDATE TO %(scheme)s.main DO  INSERT INTO %(scheme)s.main_archive (guid, version, creationdate, data) VALUES (old.guid, old.version, old.creationdate, old.data)'%{'scheme':objTypeName})
        else:
            q.logger.log("ObjectType %s already exists"%objTypeName ,3)        

    def schemeExists(self, name):
        """
        Checks if the schema with the supplied name exists
        
        @param name : name of the schema to check
        """
        sql =  "select distinct schemaname as name from pg_tables where schemaname = '%s'"%name 
        q.logger.log(sql ,5)
        result = self._dbConn.sqlexecute(sql).dictresult()
        if result:
            return True
        else:
            return False 

    def viewExists(self, objType, viewname):
        """
        Checks if the requested view exists in the supplied schema
        
        @param objType : the object type to check
        @param viewname : name of the view to check
        """        
        sql =  "select distinct schemaname, tablename from pg_tables where schemaname = '%s' and tablename = '%s'"%(objType, viewname)
        q.logger.log(sql ,5)
        result = self._dbConn.sqlexecute(sql).dictresult()
        if result:
            return True
        else:
            return False 
        
        
    def _createObject(self, data):
        """
        Store the supplied data in the database
        @param data : object to store
        """         
        data.creationdate = time.strftime('%Y-%m-%d %H:%M', time.localtime())

        listKeyValue=[]
        obj = data.serialize(ThriftSerializer)
        obj = obj.encode('hex')
        keyValue=data.guid+data.version
        listKeyValue.append(KeyValuePair( keyValue,obj))

        listKeyValue.append(KeyValuePair(data.guid, data.version))
        dht_client.putBulkData(self._ip_for_kad , self._port_for_kad,listKeyValue)
 
    def _updateObject(self, data):
        """
        #Update the supplied data in the database
        
        @param data : object to update
        """         
        
        data.creationdate = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        #obj = data.serialize(ThriftSerializer)
        obj = data.serialize(YamlSerializer)
        obj = obj.encode('hex')
        q.logger.log("update only %s.main set guid = '%s', version = '%s', creationdate = '%s', data = '{%s}') where guid = '%s'"%(data.__class__.__name__, data.guid, data.version, data.creationdate, obj, data.guid) ,5)
        self._dbConn.sqlexecute("update only %s.main set guid = '%s', version = '%s', creationdate = '%s', data = '{%s}' where guid = '%s'"%(data.__class__.__name__, data.guid, data.version, data.creationdate, obj, data.guid))
        return data

    def objectsSearch(self, objType, query_string):
        """
        returns a list of searched string
        
        @param objType : type of object to search
        @param query_string : Query string
        @param return the string contain the result
        """
        results = []
        tempdata=dht_client.parse_query( self._ip_for_kad , self._port_for_kad , query_string)
        q.logger.log("Serching result =%s"%tempdata,3)
        splitter=re.compile(r'[$]')
        lines=splitter.split(tempdata)
        q.logger.log("Splited searched result  %s"%lines,3)
       
       #return lines
        for items in lines:
            if items != "" :
                results.append(items)
        return results

    def objectsFind(self, objType, filterobject, viewToReturn):
        """
        returns a list of matching guids according to the supplied fitlerobject filters
        
        @param objType : type of object to search
        @param filterobject : a list of filters indicating the view and field-value to use to filter
        @param viewToReturn : the view to use to return the list of found objects
        """
        results = []

        if viewToReturn:
            sql = "select guid from %s.%s"%(objType, viewToReturn)
        else:
            sql = "select guid from only %s.%s"%(objType, 'main')

        rawdata = self._dbConn.sqlexecute(sql).dictresult()
        for row in rawdata:
            results.append(row['guid'])

        for item in filterobject.filters:
            view = item.keys()[0]
            field = item.values()[0].keys()[0]
            fieldvalue = item.values()[0].values()[0]
            q.logger.log("Process Filter : (%s.%s = %s)"%(view, field, fieldvalue) ,3)
            results = self._getFilterResults(objType, view, field , fieldvalue , results)

        if viewToReturn:
            q.logger.log("Building view %s"%viewToReturn ,3)
            results = self._getViewResults(objType, viewToReturn, results)

        return results

    
    def getFilterObject(self):
        """
        returns an object to hold the filter criteria
        """        
        return OsisFilterObject()

    def viewCreate(self, objType, viewName):
        """
        Creates and returns a new view object

        @param objType : the object type on which to add the view
        @param viewName : the name of the view
        """        
        
        if not self.viewExists(objType, viewName):
            return OsisView(objType, viewName)
        else:
            q.eventhandler.raiseCriticalError('[%s] already has a view [%s].'%(objType, viewName))
        
    def viewAdd(self, view):
        """
        Adds the new view to the database
        
        @param view : Osisview object to create on the database
        """              
        self._dbConn.sqlexecute(view.buildSql())
        
    
    def viewDestroy(self, objType, viewName):
        """
        Removes a view from the database
        @param objType : the type of object to destroy
        @param viewName : Osisview object to destroy
        """         
        if not self.viewExists(objType, viewName):
            q.eventhandler.raiseCriticalError('%s.%s not found.'%(objType, viewName))
            return
        
        self._dbConn.sqlexecute('DROP TABLE %s.%s CASCADE'%(objType, viewName))
        return True
    
    def viewDelete(self, objType, viewName, viewguid, versionguid=None):
        """
        Removes the row with the supplied viewguid from the view
        
        @param objType : the object Type name
        @param viewName : the view from which to remove a row
        @param viewguid : unique identifier for the object
        @param versionguid : unique identifier indicating the version of the object. (Optional)
                             If specified, only the mentioned version will be removed, 
                             If ommited, all versions will be removed !
        """      
        
        if not versionguid:
            self._dbConn.sqlexecute("delete from %s.%s where guid='%s'"%(objType, viewName, viewguid))   
        else:
            self._dbConn.sqlexecute("delete from %s.%s where guid='%s' and version = '%s'"%(objType, viewName, viewguid, versionguid))   
            
        return True
            
    
    def viewSave(self, objType, viewName, guid, version, fields):
        """
        Add a new row to the view
        
        @param objType : the object Type name
        @param viewName : the view from which to remove a row
        @param guid : unique identifier for the object
        @param versionguid : unique identifier indicating the version of the object
        @param fields : dict containing the field:values
        """         
        
        fieldnames = "guid, version, viewguid"
        values = "'%s', '%s', '%s'"%(guid, version, q.base.idgenerator.generateGUID())
        
        for itemKey in fields.iterkeys():
            fieldnames = "%s, %s"%(fieldnames, itemKey)
            if fields[itemKey]:
                values = "%s, '%s'"%(values, fields[itemKey])
            else:
                values = "%s, %s"%(values, self._generateSQLString(fields[itemKey]))
            
        sql = "insert into %s.%s (%s) VALUES (%s)"%(objType, viewName, fieldnames, values)
        
        print sql
        self._dbConn.sqlexecute(sql)
        
    def _generateSQLString(self, value):
        if q.basetype.integer.check(value):
            return value
        if q.basetype.float.check(value):
            return value       
        
        return "'%s'"%value
    def _generateSQLCondition(self, objType, view, field, value):
        ret = ""
        if q.basetype.integer.check(value):
            ret = "%s.%s.%s = %s"%(objType,view,field,value)
        else:
            if q.basetype.float.check(value):
                ret = "%s.%s.%s = %s"%(objType,view,field,value)
            else:
                ret = "%s.%s.%s like '%%%s%%'"%(objType,view,field,value)
        return ret
    
    def _getViewResults(self, objType, view, results):
        
        #build view definition
        colList= """
        select column_name, data_type
           from information_schema.columns
           where table_name = '%s' and table_schema = '%s'
        """%(view, objType)
        
        coldef = list()
        columns = self._dbConn.sqlexecute(colList).getresult()
        for col in columns:
            coldef.append((col[0], osisPGTypeConverter.convertType(col[1])))
            
            
        #no results to retrieve, just return the view definition
        if not results:
            return tuple(coldef), tuple()
        
        #retrieve view data
        
        viewname = "%s.%s"%(objType, view)
        mainname = "%s.main"%objType
        mainguid = "%s.guid"%mainname
        viewguid = "%s.guid"%viewname
        mainversion = "%s.version"%mainname
        viewversion = "%s.version"%viewname
        
        guids = ','.join("'%s'"%r for r in results)
        sql = """
        select %(viewname)s.* from %(viewname)s 
            inner join only %(mainname)s on %(mainguid)s = %(viewguid)s and %(mainversion)s = %(viewversion)s 
        where %(viewguid)s in (%(guids)s)"""%{
                'mainname':mainname, 
                'mainguid':mainguid,         
                'viewname':viewname,                
                'viewguid':viewguid, 
                'mainversion':mainversion,
                'viewversion':viewversion,
                'guids':guids}
    
        sql = """select %(viewname)s.* from %(viewname)s where %(viewguid)s in (%(guids)s) """%{'viewname':viewname, 'viewguid':viewguid, 'guids':guids}
        
        rawdata = self._dbConn.sqlexecute(sql).getresult()
        
        return tuple(coldef), tuple(rawdata)
        
        
    def _getFilterResults(self, objType, view, filterField, filterValue, results):
        #no results left to filter on
        if not results:
            return []
        
        #no view specified to filter on, so just return the results
        if not view:
            return results
        
        guidList = []
        
        guids = ','.join("'%s'"%r for r in results)
        viewname = "%s.%s"%(objType, view)
        mainname = "%s.main"%objType
        mainguid = "%s.guid"%mainname
        viewguid = "%s.guid"%viewname
        mainversion = "%s.version"%mainname
        viewversion = "%s.version"%viewname
        
        sql = """
        select %(viewguid)s from %(viewname)s 
            inner join only %(mainname)s on %(mainguid)s = %(viewguid)s and %(mainversion)s = %(viewversion)s 
        where %(filterCondition)s and 
              %(viewguid)s in (%(guids)s)"""%{
                'mainname':mainname, 
                'viewname':viewname,                
                'mainguid':mainguid,                
                'viewguid':viewguid, 
                'mainversion':mainversion,
                'viewversion':viewversion,
                'filterCondition':self._generateSQLCondition(objType,view,filterField, filterValue),
                'guids':guids}

        sql = """select distinct %(viewguid)s from %(viewname)s where %(filterCondition)s and %(viewguid)s in (%(guids)s)"""%{'viewguid':viewguid,'filterCondition':self._generateSQLCondition(objType,view,filterField, filterValue),'viewname':viewname, 'viewguid':viewguid, 'guids':guids}

        rawdata = self._dbConn.sqlexecute(sql).dictresult()
        for row in rawdata:
            guidList.append(row['guid'])   

        return guidList
                
            
            
            
        
