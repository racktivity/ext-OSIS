__author__ = 'incubaid'
__tags__ ='osis', 'store'
__priority__= 3

def main(q, i, params, tags):
    from pymodel.serializers import ThriftSerializer
    root = params['rootobject']
    domain = params['domain']
    key  = 'osis.%s.%s.%s'  % (domain, root.PYMODEL_MODEL_INFO.name, root.guid)
    data = ThriftSerializer.serialize(root)
    arakoonClient = q.clients.arakoon.getClient('cluster1')
    arakoonClient.set(key, data)
