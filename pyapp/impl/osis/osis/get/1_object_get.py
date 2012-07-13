from pymodel.serializers import ThriftSerializer

def main(q, i, p, params, tags):
    categoryName = params['category']
    domainName = params['domain']
    typeName = params['rootobjecttype']

    osis = p.application.getOsisConnection(p.api.appname)
    root = osis.objectGet(domainName, typeName, params['rootobjectguid'])

    category = getattr(p.api, categoryName)
    domain = getattr(category, domainName)
    client = getattr(domain, typeName)

    typeClass = client._ROOTOBJECTTYPE

    rootobject =  ThriftSerializer.deserialize(typeClass, root)
    params['rootobject'] = rootobject
    return rootobject
