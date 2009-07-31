from pymonkey import q

class HelloWorld:

    @q.manage.applicationserver.expose
    def hello(self, names):
        s = ''
        for name in names:
            s += "Hello %s! \n" %name
        return s

    @q.manage.applicationserver.expose
    def printnumbers(self, count):
        s = ''
        count1=int(count)
        for name in range(count1):
            s += "%d" %(name)
        return s

    @q.manage.applicationserver.expose
    def multiplynumbers(self, num1, num2):
        s = ''
        res=num1*num2
        s += "%d" %(res)
        return s
