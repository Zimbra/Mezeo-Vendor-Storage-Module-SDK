Mezeo Vendor Storage Module Developer Information
=================================================

Vendor Storage Modules provide a means to extend the Mezeo system to
provide connectivity with unique types of storage. All Vendor Storage
Modules are written in Python (targeting Python 2.6) and must extend
Mezeo's `StorageModule` base class. Once implemented, the module needs only
to be added to the system's Python Path to be made available.

Vendor Storage Modules may also be used to extend existing Storage Modules
with additional capabilities like encryption or deduplication. By
implementing the same Storage Module interface, data streams may be
intercepted and pre/post-processed.

Support Materials
-----------------

A setuptools build file (`setup.py` and associated `setup.cfg`) is included
with this package which provides an example of building a Vendor Storage
Module. For deployment, Mezeo uses setuptools' egg files containing only
compiled code. Obviously, this requires a recent version of setuptools to
be installed. A suitable egg file may be generated executing the following:

    $> python setup.py bdist_egg

for more information on setuptools please see:
[http://pypi.python.org/pypi/setuptools/](http://pypi.python.org/pypi/setuptools/)

Any egg files produced for deployment should contain **only** the Vendor
Storage Module and related resources. Please *do not* include the included
`modules` module nor the sample `simple` module. The `setup.py` file
included has been pre-configured to exclude these modules.

Example tests covering the *Simple Storage Example* (described below) are
also included. Typically Mezeo executes these tests using `nose`. If `nose`
has been installed, you can run the tests with the following command:

    $> python setup.py nosetests

or by running `nose` directly when located in the root directory of the project:

    $> nosetests

Note that if `coverage` has not also been installed, you may see warnings
related to this in the test output.

For more information on `coverage` please see:
[http://pypi.python.org/pypi/coverage/](http://pypi.python.org/pypi/coverage/)

Simple Storage Example
----------------------

Included with this document is a sample Vendor Storage Module called
*simple*. It may be used as a reference when implementing a module.

There are several things to note:

1.   Each Vendor Storage Module should be implemented in its own Python
     module. Related python modules may be included into a single module.

2.   Each module needs to import the `StorageModule` base class (described below),
     this module is imported as:
     
        from modules import StorageModule
        
3.   Any other modules required by the Vendor Storage Module should also be
     imported.

4.   Once a Vendor Storage Module has been loaded in the system, an instance
     of the module is instantiated once per server process (of which there
     may be many). These processes tend to have a rather long lifespan. Care
     should be taken in the Vendor Storage Module implementation to be
     respectful of system resources as they are unlikely to be freed (ever).

The StorageModule base class
----------------------------

Each Vendor Storage Module is required to extend the `modules.StorageModule`
base class. The `StorageModule` class defines seven methods that must be
implemented for the module to work with the system. Several methods defined
by this interface accept a `context` parameter. This value is used to
provide a set of function pointers for utility functions that may be used
by the Vendor Storage Module to interact with other aspects of the Mezeo
System. A Vendor Storage Module is not required to use this value. The set
of functions provided through this parameter is documented in the head
documentation of the `StorageModule` class.

Module Initialization: 
----------------------
    __init__(self, **kwargs)

A Vendor Storage Module may take any number of parameters on
initialization. These parameters may be used by the module implementation
to initialize the instance of the module with instance specific information
such as IP address for the storage, storage path, etc. These arguments are
specified by an administrator when the Vendor Storage Module is configured
in the system.

Creation of module opaque data: 
-------------------------------
    new_data(self, context)

The system will call this method of the Vendor Storage Module before any
data is *assigned* to the module instance. This is an opportunity for the
Vendor Storage Module to provide context information for an object. Typical
use of this value by a Vendor Storage Module is to store an Object ID or
path information usually encoded in a JSON structure. The value returned
from this method must be converted to a string. This value is passed to
other methods in the `module_data` parameter.

Associating Data with an Object: 
--------------------------------
    assign(self, context, module_data, stream)

The assign method is used to associate a data stream with a previously
allocated `module_data` value. The Vendor Storage Module is free to do
whatever it likes with the data stream.

Determining if Data already exists: 
-----------------------------------
    available(self, context, module_data)

The Mezeo System provides a way to optimize handling of data that may be
replicated by some other sub-system. To determine if the data associated
with the specified `module_data` exists at a location, this method is
called. If the method returns `True` then the Mezeo System will not attempt
to replicate the object data to the location where the *available* call was
made. If the Vendor Storage Module returns `False`, the module can expect
to have its `assign` method immediately called.

Retrieving Data from an Object: 
-------------------------------
    get_read_stream(self, context, module_data)

The `get_read_stream` method provides a means by which the Mezeo System may
read the contents of a stored object. The stream returned by this method
must implement `read`, `close` and `seek` methods.

Destroying Object Data: 
-----------------------
    delete(self, context, module_data)

The `delete` method is called by the Mezeo System when an object is to be
destroyed and no longer accessed. If successful, the `module_data` provided
to this method will never again be used.

Determining the size of an Object: 
----------------------------------
    get_size(self, context, module_data)

This method is used by the Mezeo System to ensure that ranged requests are
valid before attempting to call the `get_read_stream` method of the
module. This method is also employed by the system when performing a
*server-side copy*.

Storage Information: 
--------------------
    statistics(self, context)

The `statistics` method is used by the Mezeo System to provide system
administrators with information about the storage associated with the
instance of the Vendor Storage Module. The Vendor Storage Module is free to
return any JSON formatted value as the response to this method call. For
conformance with other Vendor Storage Modules, a *capacity* value is
defined (and documented in the StorageModule class) that is leveraged by
various system UIs. Additional values may be added to the return value if
they are significant to the Vendor Storage Module.
 
Installation and Configuration of the Storage Module:
-----------------------------------------------------

In this example, a new storage module named "newstore" will be created.

Create a source directory ($SRC) for development of the new module, and copy
the setup.py and setup.cfg files supplied by the SDK to $SRC. Also create
a README file with any useful information concerning the new module. 

Create the python package for the new module by creating a new directory in
$SRC called "newstore", and place the python source code for the module in
this directory, along with an "__init__.py" file (which may be empty).
In the $SRC directory, run:

	python2.6 setup.py bdist_egg
	
The new egg file containing "newstore" will be found in $SRC/dist - copy this
file to each of the nodes in the MezeoCloud cluster. The egg file may be placed
in any convenient location on the node. Add the full path name of the egg file
(path and file name) to the 'python-path' argument in the WSGI-Daemon line in
each of the configuration files in /opt/mezeo/conf/apache.d, and then restart
apache on each of the nodes.

The MezeoCloud Provisioning Guide contains examples of adding, updating and 
deleting storage module ("vendor module") information to the system. A curl
example for adding "newstore":

curl -u administrator -v -X PUT --data-binary \
'{"module": "newstore.newstore.NewStorage", \
  "description": "New Storage Module", \
  "args": ["arg1", "arg2", "arg3"] }' \
  https://cloud.example.com/cdmi/system_configuration/vendor_modules/newstore
  
Note: the "args" list contains the values of the arguments used to initialize
the new storage module - see 'Module Initialization' above.
  
This curl command should return a '204 No Content' response.

After this step is completed, new users may be provisioned with "policy" set to
"newstore". Data for these users will then be stored in and accessed from
"newstore".
