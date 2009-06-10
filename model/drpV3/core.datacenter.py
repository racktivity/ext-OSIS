

namespace = "core.datacenter"

## @doc  physical datacenter
class datacenter(RootObject):

    ## @doc  guid of the location of the datacenter
    ## @bizz ref = core.location/location
    ## @db   indexed
    ## @type guid
    locationguid

    ## @doc  guid of the customer owning the datacenter    
    ## @bizz ref = core.customer/customer
    ## @db   indexed
    ## @type guid
    customerguid
    
    ## @doc  datacenter name
    ## @db   notnull indexed
    ## @type string
    name  

    ## @doc  additional remarks on datacenter
    ## @type type_description
    description  
