import pymodel

class Simple(pymodel.RootObjectModel):
    i = pymodel.Integer(thrift_id=1)

    @classmethod
    def generate_test_object(cls):
        obj = cls()
        obj.i = 123
        return obj
