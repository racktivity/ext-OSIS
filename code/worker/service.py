from osis.server import BaseServer

class OsisService(object):
    '''
    @todo: UPDATE DOCSTRINGS
    '''
    
    def __init__(self, tasket_path=None, serializer=None):
        '''Initialize the OSIS service

        @param taskletPath: Container path of OSIS tasklets
        @type taskletPath: string
        '''
        
        self.server = BaseServer(tasket_path)
        # thriftbase64 as default
        self.serializer = serializer or 'thriftbase64'
    
    def get(self, domain, rootobjecttype, rootobjectguid):
        '''Retrieve a root object with a given GUID from the OSIS server

        If no version is specified, the latest version is retrieved.

        @param guid: GUID of the root object to retrieve
        @type guid: string

        @return: Root object instance
        @rtype: L{osis.model.RootObjectModel}
        '''
        
        return self.server.get(domain, rootobjecttype, rootobjectguid, self.serializer)
        
        
    def query(self, domain, query):
        
        ''' 
        run query from OSIS server

        @param query: Query to execute on OSIS server
        @type query: string

        @return: result of the query else raise error
        @type: List of rows. Each row shall be represented as a dictionary.
        '''
        
        return self.server.runQuery(domain, query)
        

    def delete(self, domain, rootobjecttype, rootobjectguid):
        '''Delete a root object with a given GUID from the OSIS server

        If no version is specified, all the versions shall be deleted.

        @param guid: GUID of the root object to delete
        @type guid: string
        @param version: Version GUID of the object to delete
        @type version: string

        @return: True or False, according as the deletion succeeds or fails
        '''
        
        return self.server.delete(domain, rootobjecttype, rootobjectguid)

    def save(self, domain, rootobjecttype, rootobjectguid, rootobject):
        '''Save a root object to the server

        @param object_: Object to store
        @type object_: L{osis.model.RootObjectModel}
        '''
        
        return self.server.put(domain, rootobjecttype, rootobject, self.serializer)

    def find(self, domain, rootobjecttype, filter, view=None):
        '''Perform a find/filter operation

        If no view name is specified, a list of GUIDs of the matching root
        objects is returned. Otherwise a L{ViewResultList} is returned.

        @param filter: Filter description
        @type filter: OsisFilterObject
        @param view: View to return
        @type view: string

        @return: List of GUIDs or view result
        @rtype: tuple<string> or L{ViewResultList}
        '''
        
        return self.server.find(domain, rootobjecttype, filter, view=None)
    
    def findAsView(self, domain, rootobjecttype, filter, view):
        """
        Perform a find/filter operation.
        @param filter: Filter description
        @type filter: OsisFilterObject
        @param view: name of the view to return
        @type view: string

        @return: list of dicts representing the view{col: value}
        """
        
        return self.server.findAsView(domain, rootobjecttype, filter, view=None)