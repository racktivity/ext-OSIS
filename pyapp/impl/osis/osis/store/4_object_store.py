__author__ = 'incubaid'
from pymodel.serializers import ThriftSerializer
import time

def main(q, i, p, params, tags):
    root = params['rootobject']
    if not root.creationdate:
        root.creationdate = str(int(time.time()))
        
def match(q, i, p, params, tags):
    return params['domain'] != 'core'
