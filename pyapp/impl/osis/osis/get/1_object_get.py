
from pymodel.serializers import ThriftSerializer

def main(q, i, p, params, tags):
    category_name = params['category']
    domain_name = params['domain']
    type_name = params['rootobjecttype']
    # FIXME: use category
    key  = 'osis.%s.%s.%s'  % (domain_name, type_name, params['rootobjectguid'])
    root = p.api.db.get(key)
    # Temporary hack
    # TODO FIXME
    category = getattr(p.api, category_name)
    domain = getattr(category, domain_name)
    client = getattr(domain, type_name)
    type_class = client._ROOTOBJECTTYPE

    rootobject =  ThriftSerializer.deserialize(type_class, root)
    params['rootobject'] = rootobject
    return rootobject
