from pymonkey import q

class HelloWorld:

    @q.manage.applicationserver.expose_authenticated
    def hello(self, names):
        s = ''
        for name in names:
            s += "Hello %s!\n" %name
        return s
    def checkAuthentication(self, username, password):
        return username == 'terry' and password == 'jones'

