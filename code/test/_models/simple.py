from osis import model

class Simple(model.RootObjectModel):
    i = model.Integer(thrift_id=1)

    @classmethod
    def generate_test_object(cls):
        obj = cls()
        obj.i = 123
        return obj
