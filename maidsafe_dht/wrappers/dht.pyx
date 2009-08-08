cdef extern from "stdlib.h":
    ctypedef unsigned long size_t
    void free(void *ptr)
    void *malloc(size_t size)
    void *realloc(void *ptr, size_t size)
    size_t strlen(char *s)
    char *strcpy(char *dest, char *src)


cdef extern from "c_interface_dht1.h":
    void START(char *ip,int port,int pport_to_start)
    void STOP()
    char * DHT_GET( char *key,int flag )
    void DHT_PUT( char *key , char *value)
    void DHT_START_AS_SERVER(int port)

def start(char *ip, int port,int pport_to_start=8000):
    START(ip,port,pport_to_start)

def stop():
    STOP()

def get(char *key,int flag=0):
   return DHT_GET(key,flag)

def put(char *key, char *value):
    DHT_PUT(key,value)

def start_as_server(int port):
    DHT_START_AS_SERVER(port)

	

