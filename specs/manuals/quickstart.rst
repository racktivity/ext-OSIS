===============
OSIS Quickstart
===============

System overview
===============
OSIS consists of 3 core components:

* Model definitions
* A server
* A client

The server can be split up in 3 components:

* An actual server listening on some TCP port
* Tasklets handling all required actions
* A persistant storage system

Next to this, there needs to be some transport layer so a client can connect to
a server.

Implementation
==============
The current OSIS implementation uses Thrift as serialization system, XMLRPC as
client-server transport and PostgreSQL as persistant storage layer.

Basic usage
===========
Model definition
----------------
When using OSIS, one starts by defining models, which represent the objects to
be stored. In this walkthrough we'll create a system to store information about
companies and their employees.

The model definition::

  from osis import model

  class Address(model.Model):
      street = model.String(thrift_id=1)
      number = model.Integer(thrift_id=2)
      postal_code = model.Integer(thrift_id=3)
      city = model.String(thrift_id=4)

  class Employee(model.Model):
      first_name = model.String(thrift_id=1)
      last_name = model.String(thrift_id=2)
      email_addresses = model.List(model.String(), thrift_id=3)
      address = model.Object(Address, thrift_id=4)

  class Company(model.RootObjectModel):
      name = model.String(thrift_id=1)
      url = model.String(thrift_id=2)
      employees = model.List(model.Object(Employee), thrift_id=3)


Model deployment
----------------
The model code goes into $QBASE/libexec/osis/company.py (note the filename is
not important, as long as it ends with .py).

The file should be deployed on both the client and the server. TODO Mention
model versioning

Server setup
------------
The current OSIS server runs inside the PyMonkey Applicationserver. After
installing the package, a new service should be registered in the server. Refer
to the Applicationserver documentation to figure out how to achieve this. The
server classspec is 'OsisServer.OsisServer', in this walktrough the service name
will be 'osis'.

Setting up a database
---------------------
TODO Check whether this is still correct

::

  * Install postgresql QPackage

  q.manage.postgresql8.cmdb.rootLogin = username
  q.manage.postgresql8.cmdb.rootPasswd = password

  q.manage.postgresql8.cmdb.save()
  q.manage.postgresql8.applyConfig()

  ##if postgresql fails to start using the q.manage commands use
  q.cmdtools.postgresql8.pg_ctl.start(username)

  q.manage.postgresql8.cmdb.addDatabase('osis', username)
  q.manage.postgresql8.cmdb.save()
  q.manage.postgresql8.applyConfig()

  from osis.store.OsisDB import OsisDB
  osisdb = OsisDB()
  osisdb.addConnection('main', '127.0.0.1', 'osis', username, password)

Setting up basic tasklets
-------------------------
Save tasklet
************
::

  from osis.store.OsisDB import OsisDB

  __author__='qlayer'
  __tags__='osis', 'store'
  __priority__= 2

  def main(q, i , params, tags):
      q.logger.log('Storing %s'%(repr(params)), 5)

      osis = OsisDB().getConnection('main')
      osis.objectSave(params['rootobject'])


Get tasklet
***********
::

  from osis.store.OsisDB import OsisDB
  __author__='qlayer'
  __tags__ = 'osis', 'get'

  def main(q, i, params, tags):
      q.logger.log('Getting %s'%(repr(params)), 5)

      osis = OsisDB().getConnection('main')
      rootobject = osis.objectGet(params['rootobjecttype'], \
                     params['rootobjectguid'])
      params['rootobject'] = rootobject

Registering the model on the server
-----------------------------------
::

  from osis.store.OsisDB import OsisDB
  osisdb = OsisDB()
  con = osisdb.getConnection('main')
  con.createObjectTypeByName('company')


Using the client
----------------
Three steps are necessary to connect to an OSIS server:

* Initialize the OSIS system
* Create a transport
* Create a client

Here's a session::

  import osis
  from osis.client import OsisConnection
  from osis.client.xmlrpc import XMLRPCTransport

  osis.init('/opt/qbase2/libexec/osis')
  transport = XMLRPCTransport('http://localhost:8000', 'osis')
  client = OsisConnection(transport)

  company = client.company.new(name='Aserver', url='http://www.aserver.com')

  employee1 = company.employees.new(first_name='John', last_name='Doe')
  employee1.email_addresses.append('john.doe@aserver.com')
  employee1.email_addresses.append('john@aserver.com')

  # TODO This doesn't work yet
  # employee1.address.street = 'Foostreet'
  # employee1.address.number = 21
  # employee1.address.postal_code = 1234
  # employee1.address.city = 'Bar'

  client.company.save(company)

Views
=====
TODO Define

Registering a view
------------------
Views are mainly registered in the install tasklet of the Qpackage deploying the
view tasklets.

Here's how to::

  from osis.store.OsisDB import OsisDB
  osisdb = OsisDB()
  conn = osisdb.getConnection('main')
  view = conn.viewCreate('company', 'name')
  view.setCol('name', q.enumerators.OsisType.STRING, False)
  view.setCol('url', q.enumerators.OsisType.STRING, False)
  conn.viewAdd(view)

Updating a view
---------------
View data should be updated by a tasklet executed when a rootobject is saved.

Here's an example::

  from osis.store.OsisDB import OsisDB

  __author__ = 'qlayer'
  __tags__ = 'osis', 'store'
  __priority__ = 1

  myRootObjectType = 'Company'

  def match(q,i,params, tags):
      return params['rootobjecttype'] == myRootObjectType

  def main(q, i, params, tags):
      osis = OsisDB().getConnection('main')
      rootObject = params['rootobject']
      osis.viewSave(myRootObjectType, 'name', rootObject.guid,
                        rootObject.version,
                        {
                                'name':rootObject.name,
                                'url':rootObject.url
                        }
                    )

Querying a view
---------------
Querying a view is easy::

  filter_ = client.company.getFilterObject()

  filter_.add('name', 'name', 'serv') # viename, fieldname, value

  # Get a list of matching GUIDs
  client.company.find(filter_)
  # Returns a list containing the GUID of the 'Aserver' company

  # Get view information
  client.company.find(filter_, 'name')
  results = client.company.find(filter_, 'name')
  for result in results:
      print '%s:' % result.name, result.url

Note: the result of a find call with view argument (the second example) returns
a generator, so don't reuse it or wrap it in a list (TODO maybe change this),
and the objects in the iterable are not root objects, but only contain
attributes for all fields defined in the view definition (ie, result.employees
would not exist).
