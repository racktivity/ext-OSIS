
namespace = "cloud.vdc"

## @doc  attributes of a VDC object, acts like a view, info required to be able to draw a vdc
class vdc(RootObject):

    ## @doc  guid of the customer, owning the VDC
    ## @bizz ref = vdccustomer
    ## @db   indexed
    ## @type guid
    customerguid

    ## @doc  list of vdcitems in the VDC, e.g. switch, virtual machines, ...
    ## @type array(cloudservice)
    cloudservices
    
    ## @doc  status of the VDC, listed in the vdcstatustype, can be determined by asking status for all connected cloudservices
    ## @db   notnull indexed
    ## @type vdcstatustype
    status
 
class cloudservice(DRPObject):

    ## @doc  x-position of the item in the graphical view of the VDC
    ## @type int
    positionx
    
    ## @doc  y-position of the item in the graphical view of the VDC
    ## @type int
    positiony
    
    ## @doc  link to machine in this vdcitem (can be machine or application or lan but not both)
    ## @bizz ref = core.machine/machine
    ## @db   notnull indexed
    ## @type guid
    machine    
    
    ## @doc  link to machine in this vdcitem (can be machine or application or lan but not both)
    ## @bizz ref = core.application/machine
    ## @db   notnull indexed
    ## @type guid
    application    

    ## @doc  link to lan in this vdcitem (can be machine or application or lan but not both)
    ## @bizz ref = core.lan/lan
    ## @db   notnull indexed
    ## @type guid
    lan    
    
    ## @doc  connections to other vdcitems
    ## @bizz ref = vdcitem
    ## @db   notnull indexed
    ## @type array(guid)
    connections
    
    ## @doc  status of the cloudservice (corresponds with status of corresponding machine, lan or application object in drp)
    ## @db   notnull indexed
    ## @type cloudservicestatustype
    status
    

class vdcstatustype(QType):

   ##+ name = 'modeled'
   ##+ name = 'deploying'
   ##+ name = 'deployed'
   ##+ name = 'error'
   ##+ name = 'delete'
   ##+ name = 'changed'
   ##+ name = 'processing'
   ##+ name = 'deleted'
   ##+ name = 'unconfigured'
   ##+ name = 'configured'


class cloudservicestatustype(QType):

   ##+ name = 'modeled'
   ##+ name = 'deploying'
   ##+ name = 'deployed'
   ##+ name = 'error'

    
