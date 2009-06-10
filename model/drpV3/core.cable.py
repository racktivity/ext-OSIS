
namespace = "core.cable"


## @doc  physical cable connecting two device ports
class cable(RootObject):

    ## @doc  guid of the source port to which a cable is connected (where possible source = device, target = port aggregator e.g. switch or UPS)
    ## @db   indexed
    ## @bizz ref = core.device/port
    ## @type guid
    sourceportguid

    ## @doc  target port to which cable is connected (where possible source = device, target = port aggregator e.g. switch or UPS)
    ## @db   indexed
    ## @bizz ref = core.device/port
    ## @type guid
    targetportguid

    ## @doc  cable type
    ## @db   notnull indexed
    ## @type cabletype
    type
 
 
## @doc  type of physical cable
class cabletype(QType):
    ##+ name="USBCABLE", description="USB cable"
    ##+ name="FIREWIRECABLE", description="Firewire cable"
    ##+ name="NETCABLE", description="Network cable"
    ##+ name="IBCABLE", description="Infiniband Cable"
    ##+ name="SATACABLE", description="SATA cable"
    ##+ name="POWERCABLE", description="Power cable"
