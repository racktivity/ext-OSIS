
namespace = "core.customer"

## @doc a customer is someone who consumes the service of the datacenter in a generic sense
class customer(RootObject):

    ## @doc  address of the customer
    ## @type string(50)
    address
    
    ## c@doc city where the customer resides
    ## @type string(50)
    city
    
    ## @doc country where the customer is located
    ## @type string(50)
    country
    
    ## @doc  status of the customer
    ## @db   notnull indexed
    ## @type statustype
    status=CONFIGURED
    
    ## @doc  guid of reseller
    ## @sdk  RW--
    ## @bizz ref = customer
    ## @db   indexed
    ## @type guid
    parentcustomerguid
    
    ## @doc  list of users from the customer (GUIDS)
    ## @bizz ref = core.user/user
    ## @type array(guid)    
    users

    ## @doc  list of capacity units consumed by customer
    ## @type array(capacityunit)
    capacityunitsconsumed
    
    ## @doc  max amount of capacity units which can be used by customer
    ## @type array(capacityunit)
    capacityunitslimits    
      
    
class statustype(QType):
    ##+ name = "CONFIGURED"
    ##+ name = "CREATED"
    

class capacityunit(DRPObject):
    
    ## @doc  amount of capacity units
    ## @type int
    amount
    
    ## @doc  type of capacity unit
    ## @db   notnull indexed
    ## @type capacityunittype
    type    
    
class capacityunittype(QType):
    
    ##+ name = "SUA"         # storage unit Archive
    ##+ name = "SUP"         # storage unit Primary
    
    ##+ name = "LV"          # Linux vmachines
    ##+ name = "WV"          # Windows vmachines
    
    ##+ name = "NUIPPORTS"   # network unit public ip address
    ##+ name = "NUM"         # network unit bandwidth in Mbit/s
    ##+ name = "NBU"         # network bandwidth units in GB/month
    
    ##+ name = "MU"          # memory unit (MB)
    ##+ name = "CU"          # CPU unit (mhz) 
        
