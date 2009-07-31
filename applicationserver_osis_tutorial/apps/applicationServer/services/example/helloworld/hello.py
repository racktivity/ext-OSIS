from pymonkey import q

class HelloWorld:

    @q.manage.applicationserver.expose
    def hello(self, names):
        s = ''
        for name in names:
            s += "Hello %s!\n" %name
        return s
