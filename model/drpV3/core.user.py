
namespace = "core.user"

## @doc a user is someone who can access the datacenter infrastructure, security is given on this level
class user(RootObject):

    ## @doc  first name of the customer account
    ## @type type_name
    firstname
    
    ## @doc  last name of the customer account
    ## @type type_name
    lastname
    
    
    ## @doc  optional description of user
    ## @type string(250)
    description
    
    ## @doc  login
    ## @db   notnull
    ## @type type_login
    login
    
    ## @doc  password 
    ## @type type_password
    ## @db   notnull
    password
        
    ## @doc  address of the contact
    ## @type string(50)
    address
    
    ## @doc  city where the contact resides
    ## @type string(50)
    city
    
    ## @doc  country where the contact is located
    ## @type string(50)
    country
    
    ## @doc  status of the customer
    ## @db   notnull indexed
    ## @type statustype
    status=CONFIGURED
    
    ## @doc  guid of customer this user belongs to (optional)
    ## @bizz ref = customer
    ## @db   indexed
    ## @type guid
    parentcustomerguid
     
    ## @doc  certificate of the customer account for secure acces into datacenter
    ## @type string
    certificate
    
    ## @doc  checksum of the certificate for verifying the validity of the certificate
    ## @type string(50)
    certificatechecksum
    
    ## @doc  private key
    ## @type string
    privatekey
    
    ## @doc  option to give the user administrator rights
    ##       An user with administrator rights can access the spaces of sub-customers
    ## @type boolean
    isadmin=False
    
    ## @doc  e-mail address of the user (can be comma separated)
    ## @type type_email
    email

    ## @doc  mobile phone
    ## @type string(50)
    phonemobile
    
    ## @doc  landline phone
    ## @type string(50)
    phonelandline
    
        
    
## @doc a group of users
class group(RootObject):

    ## @doc  name of user
    ## @type string(50)
    name

    ## @doc  optional description of user
    ## @type string(250)
    description
    
    ## @doc  users who belong to group
    ## @bizz ref = user
    ## @db   indexed
    ## @type array(guid)
    members
    
class statustype(QType):
    ##+ name = "CONFIGURED"
    ##+ name = "CREATED"
