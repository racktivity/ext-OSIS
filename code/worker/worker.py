#!/opt/qbase3/bin/python

import os
import traceback 

from workerlib import WorkerBase
from workerlib.consumer import QueueMessageConsumer
from workerlib.dispatcher import MessageDispatcher
from workerlib.publisher import QueuePublisher

from service import OsisService

from pymonkey.InitBase import q

class OsisDispatcher(MessageDispatcher):
    
    def __init__(self, api):
        self.api = api
        
    def dispatch(self, message):
            
        #print '---> %s' % message.getMessageString()            
        try:
            method = getattr(self, message.methodname, None)
            
            if not method:
                resultvalue = 'Method %s does not exist' % message.methodname
                resultcode  = 1
            else:
                resultvalue = method(message)
                resultcode  = 0
        except Exception, ex:
            q.logger.log('Error in dispatching: %s' % ex.message,1)
            resultcode  = 1 
            resultvalue = 'Failed to execute method %s: %s' % (message.methodname, traceback.format_exc())

        # Copy message properties        
        #resultmessage = copy.deepcopy(message)
        # @todo: Hack: double de-/serialization and RPC only
        resultmessage = q.messagehandler.getRPCMessageObject(message.getMessageString())
        # Update result
        resultmessage.params = {'resultcode': resultcode, 'resultvalue': resultvalue}
        
        #print '<--- %s' % resultmessage.getMessageString()
        
        return resultmessage
    
    def get(self, message):
        return self.api.get(message.domain, message.category, message.params['rootobjectguid'])
        
    def query(self, message):
        return self.api.runQuery(message.domain, query)

    def delete(self, message):      
        return self.api.delete(message.domain, message.category, message.params['rootobjectguid'])

    def save(self, message):
        return self.api.save(message.domain, message.category, message.params['rootobjectguid'], message.params['rootobject'])

    def find(self, message):
        return self.api.find(message.domain, message.category, message.params['filter'], view=message.params['view'])
    
    def findAsView(self, message):
        return self.api.findAsView(message.domain, message.category, message.params['filter'], view=message.params['view'])

if __name__ == '__main__':
    
    q.application.appname = 'osis_worker'
    q.application.start()
    
    exchange        = 'pylabs.rpc'
    exchange_type   = 'topic'
    binding_key     = 'pylabs.rpc.osis.#'
    queue_name      = 'pylabs.osis'
    
    durable         = False
    auto_delete     = True
    no_ack          = False
    
    
    # Define consumer
    consumer = QueueMessageConsumer(exchange, exchange_type, binding_key, durable, auto_delete, queue_name, no_ack)
    
    # Define dispatcher
    tasklet_path = os.path.join(os.path.dirname(__file__), 'tasklets')
    api = OsisService(tasklet_path)
    dispatcher = OsisDispatcher(api)
    
    # Define publisher
    publisher = QueuePublisher(exchange)
    
    # Start the worker
    worker = WorkerBase(consumer, dispatcher, publisher)
    worker.work()
    
    q.application.stop()