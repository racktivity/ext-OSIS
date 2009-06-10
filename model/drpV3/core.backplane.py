
namespace = "core.backplane"

## #is physical interconnects between devices
class backplane(RootObject):
    
    ## @doc  name for backplane
    ## @db   notnull indexed
    ## @type string
    name  

    ## @doc  additional remarks / description
    ## @type type_description
    description  
   
    ## @doc  type of backplane, storage, vlan host, management, and/or public
    ## @db   notnull indexed
    ## @type backplanetype
    type
    
    ## @doc  flag indicating if backplane is ment to be connected to the outside world
    ## @type boolean
    publicflag = False
    
    ## @doc  flag indicating if the backplane is hosting management Q-LAN's
    ## @type boolean
    managementflag = False
    
    ## @doc  flag indicating if the backplane is used for storage purposes
    ##       Usually used on InfiniBand or Fibre Channel backplanes
    ## @type boolean
    storageflag = False
    
    ## @doc  guid of the datacenter to which the domain belongs
    ## @bizz ref = core.datacenter/datacenter
    ## @db   indexed
    ## @type guid
    datacenterguid
    
    ## @doc  array of cables being connected to this backplane (can be used to figure out connections between devices)
    ## @bizz ref = core.cable/cable
    ## @db   indexed
    ## @type array(guid)
    cableconnections
    
          
class backplanetype(QType):

    ##+ name = "INFINIBAND"
    ##+ name = "ETHERNET"
