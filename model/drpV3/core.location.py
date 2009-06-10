
namespace = "core.location"

## @doc class which provides the properties of a location of a data center
class location(RootObject):

    ## @doc  alias for a location
    ##       The alias can help you for faster management of the locations
    ## @type type_alias
    alias

    #TODO what does this, in the old sdk this is type boolean
    ## @type string(30)
    public

    ## @doc  address of the location of a data center
    ## @type string(50)
    address

    ## @doc  city where the data center is located
    ## @type string(50)
    city

    ## @doc  country where the data center is located
    ## @type string(50)
    country
    
    #@todo link to datacenter
