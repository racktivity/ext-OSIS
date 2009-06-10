
# Namespace
namespace = "core.rack"


## @doc rack in the datacenter
class rack(RootObject):

    ## @doc datacenter to which the rack belongs
    ## @bizz ref = core.datacenter/datacenter
    ## @db   indexed
    ## @type guid
    datacenterguid

    ## @doc optional customer to which the rack belongs    
    ## @bizz ref = core.customer/customer
    ## @db   indexed
    ## @type guid
    customerguid

    ## @doc  floor location of the rack in the datacenter
    ## @type string(100)
    floor

    ## @doc  corridor location of the rack on the floor
    ## @type string(100)
    corridor

    ## @doc  position of the rack in the corridor or datacenter
    ## @type string(100)
    position

    ## @doc  rack height in u
    ## @type int
    height = 42

    ## @doc  racktype, listed in the enumerator racktype    
    ## @db   notnull indexed
    ## @type racktype
    type
    


class racktype(QType):
    ##+ name = "CLOSED"
    ##+ name = "CLOSEDCOOLED"
    ##+ name = "OPEN"

