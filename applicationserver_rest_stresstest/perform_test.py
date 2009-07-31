from pymonkey import q,i
import httplib,urllib
import os,re,time,sys
from urllib2 import HTTPError,URLError
import shutil

class rest_stress_test:
    def help(self):
        q.gui.dialog.message('\nThe functions runtest_get or runtest_post can be called with the following arguments')
        q.gui.dialog.message('First argument is server ipaddress as string,Second argument is port number,Third is')
        q.gui.dialog.message('number of requests eg., runtest_get(\'127.0.0.1\',\'8889\',1000)')
        q.gui.dialog.message('The above command will send 1000 get requests to server at 127.0.0.1 at 8889 port')
        q.gui.dialog.message('Please use the setup function if the application server is running on local host so that')
        q.gui.dialog.message('required service is configured for stress test. If server is at remote host, ensure that')
        q.gui.dialog.message('service name test_service1 is available with service class example.stresstest_service.HelloWorld is available')


    def __get_data(self,address,prefix,suffix):
	'''Open a HTTP connection and get data'''
     	conn = httplib.HTTPConnection(address)
    	quoted_suffix=urllib.quote(suffix,'/')
    	conn.request("GET", prefix+quoted_suffix)
    	r1=conn.getresponse()
    	data=r1.read()
	self.errorCode = r1.status
    	if (repr(r1.status)=='200'):
	      	self.responses_count=self.responses_count+1
    		self.responses.append(data+'\n')
    	conn.close()
	return data

    def __post_data(self,address,prefix,suffix):
	'''Open a HTTP connection and get data'''
     	conn = httplib.HTTPConnection(address)
    	quoted_suffix=urllib.quote(suffix,'/')
    	conn.request("POST", prefix+quoted_suffix)
    	r1=conn.getresponse()
    	data=r1.read()
    	if (repr(r1.status)=='200'):
	      	self.responses_count=self.responses_count+1
    		self.responses.append(data+'\n')
    	conn.close()

    def runtest_get(self,ipaddress,portno,no_of_requests):
        '''Run the stress test for REST
	@param ipaddress: IP Address of the Application Server having REST interface
	@type ipaddress: string
	@param portno: Port No of the REST service
	@type portno: string
	@param no_of_requests: Number of GET requests to be sent to the Server
	@type no_of_request: integer
	'''
        self.ipaddress=ipaddress
        self.portno=portno 
        self.count=no_of_requests
        self.responses=[]
        self.responses_count=0
    	self.sys_time=time.ctime()
    	self.start_time=time.time()
        count=0
        q.gui.dialog.message('\n')
	for i in range(self.count):
            self.__get_data(self.ipaddress+':'+self.portno,'/test_service1/hello?names=','["Application Server","Stress Test"]')
            count=count+1
            if(count%10==0):
                q.gui.dialog.message('Sending request no:%d-%d' %(count-9,count))
        self.sys_time_end=time.ctime()
        self.end_time=time.time()
        self.__print_results()

    def runtest_post(self,ipaddress,portno,no_of_requests):
        '''Run the stress test for REST
	@param ipaddress: IP Address of the Application Server having REST interface
	@type ipaddress: string
	@param portno: Port No of the REST service
	@type portno: string
	@param no_of_requests: Number of POST requests to be sent to the Server
	@type no_of_request: integer
	'''
        self.ipaddress=ipaddress
        self.portno=portno 
        self.count=no_of_requests
        self.responses=[]
        self.responses_count=0
    	self.sys_time=time.ctime()
    	self.start_time=time.time()
        count=0
        q.gui.dialog.message('\n')
	for i in range(self.count):
            self.__post_data(self.ipaddress+':'+self.portno,'/test_service1/hello?names=','["Application Server","Stress Test"]')
            count=count+1
            if(count%10==0):
                q.gui.dialog.message('Sending request no:%d-%d' %(count-9,count))
        self.sys_time_end=time.ctime()
        self.end_time=time.time()
        self.__print_results()


    def __print_results(self): 
        '''Print the results after test is run'''
        elapsed_time=self.end_time-self.start_time
        requests_per_sec=self.count/elapsed_time
        success_per_sec=self.responses_count/elapsed_time
        average_time_per_request=0.0
        if(success_per_sec!=0):
            average_time_per_request=1000/success_per_sec
        summary=[]
        summary.append('\n#################################################################\n')
        summary.append('Start time is: '+repr(self.sys_time)+'\n')
        summary.append('Server ip address:'+self.ipaddress+' PortNo:'+self.portno+'\n')
        summary.append('Elapsed time in sec is: '+repr(elapsed_time)+'\n')
        summary.append('Number of get requests:'+repr(self.count)+'\n')
        summary.append('Number of success responses:'+repr(self.responses_count)+'\n')
        summary.append('Average requests per second: '+repr(requests_per_sec)+'\n')
        summary.append('Average responses per second: '+repr(success_per_sec)+'\n')
        summary.append('Average time in millisec per request: '+repr(average_time_per_request)+'\n')
        summary.append('End time is: '+repr(self.sys_time_end)+'\n')
        summary.append('#################################################################\n\n')

        for items in summary:
             print items

    def setup(self):
	'''Setup the required service in application server'''
        filepath=os.path.dirname(__file__) 
        newstr=filepath.split('/')
        newlen=len(newstr)-4
        newlist=newstr[:newlen]
        path_to_copy=''
        for i1 in newlist:
          path_to_copy=path_to_copy+i1+'/'
        path_to_copy=path_to_copy+'apps/applicationServer/services/example/stresstest_service.py'
        source_path=filepath+'/stresstest_service.py'
        shutil.copy(source_path,path_to_copy)
        print '\nPlease provide the service name as "test_service1" and service class as "example.stresstest_service.HelloWorld"' 
        i.servers.applicationserver.services.add()
	q.manage.applicationserver.start()

    def print_errorCodes(self, errorCode, mesg):
	httpErrorCode = mesg.split(',')
	print 'The Application Server returned:'
	print 'HTTP Error: ', errorCode
	for items in httpErrorCode:
		print items
	print '--------------------------------\n'
	
    def runtest_get_errorCodes(self,ipaddress,portno):
        '''Run the test to get Error Codes for REST
	@param ipaddress: IP Address of the Application Server having REST interface
	@type ipaddress: string
	@param portno: Port No of the REST service
	@type portno: string
	'''
        self.ipaddress=ipaddress
        self.portno=portno 
        self.responses=[]
        self.responses_count=0
    	self.sys_time=time.ctime()
    	self.start_time=time.time()
        count=0
        q.gui.dialog.message('\n')

	print 'Sending GET request with wrong module arguments'
        httpErrorCode = self.__get_data(self.ipaddress+':'+self.portno,'/test_service1/hello?names_error=','["Application Server","Stress Test"]')
	self.print_errorCodes(self.errorCode, httpErrorCode)

	print 'Sending GET request with wrong module name'
        httpErrorCode = self.__get_data(self.ipaddress+':'+self.portno,'/test_service1/hello_error?names=','["Application Server","Stress Test"]')
	self.print_errorCodes(self.errorCode, httpErrorCode)

	print 'Sending GET request with wrong service name'
        httpErrorCode = self.__get_data(self.ipaddress+':'+self.portno,'/test_service1_error/hello?names=','["Application Server","Stress Test"]')
	self.print_errorCodes(self.errorCode, httpErrorCode)

        self.sys_time_end=time.ctime()
        self.end_time=time.time()
