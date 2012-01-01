"""
Mezeo Cloud Storage Platform - Abstract Vendor Storage Module Interface

Storage modules are required to be deterministic in their output.

Each method is passed a 'storage context' which is a dictionary of method callbacks:

  {
    'func': { 'getModule': <method pointer> }
  }

Methods currently provided are:
 getModule: Allows a vendor module to request an instance of a module by name

"""


class StorageModule(object):
    '''
    Mezeo Storage Module Abstract Interface

    '''

    def __init__(self, **kwargs):
        '''
        Initializes the vendor storage module.
        Arguments for this method are defined by the module implementation.

        :param kwargs: dictionary of arguments needed for the module to initialize
        '''
        pass

    def available(self, context, module_data):
        '''
        Called by the platform to validate the existence of data stored in
        the module.

        The method MUST return 'True' when the module_data is available.

        :param dict context: the storage context (defined above)
        :param str module_data: - opaque module data
        :returns: bool - True if 'available' else False

        '''
        raise NotImplemented()

    def capabilities(self, context):
        '''
        Called by the platform to retrieve the module's capabilities.

        :param dict context: the storage context (defined above)
        :param str module_data: - opaque module data
        :returns: dict - dictionary of module capabilities

        '''
        raise NotImplemented()

    def put(self, context, stream):
        '''
        Called by the platform to request a stream of data to be stored in
        the module.

        The method MUST return an opaque `module_data` which will be passed to
        the other methods in the `module_data` parameter.
        This allows the Vendor Storage Module to provide context information
        for an object. Typical use of this value by a Vendor Storage Module
        is to store an Object ID or path information usually encoded in a
        JSON structure. The value returned from this method must be converted
        to a string.

        :param dict context: the storage context (defined above)
        :param str module_data: - opaque module data
        :param stream stream: - input data stream
        :returns: module_data - opaque module data

        '''
        raise NotImplemented()

    def get_read_stream(self, context, module_data):
        '''
        Called by the platform to request a stream containing the data
        stored in the module.  This stream will only be used to retrieve
        data and does not need to implement the 'write' method.

        The object returned needs to have a 'read' and a 'close' method.

        :param dict context: the storage context (defined above)
        :param str module_data: - opaque module data
        :returns: stream

        '''
        raise NotImplemented()

    def delete(self, context, module_data):
        '''
        Destroys file content stored in the module.
        Called by the platform when it wishes to delete any data pointed to
        by 'module_data'.

        :param dict context: the storage context
        :param str module_data: - opaque module data
        :returns: None
        '''
        raise NotImplemented()

    def statistics(self, context):
        '''
        Returns statistics from the storage module

        Format is as follows:

        {
          "capacity": {
              "total": <number of bytes total>
              "free": <number of bytes free>
              "used": <number of bytes used>
          }
        }

        :param dict context: the storage context
        :returns: dictionary of statistics data
        :rtype: dict

        '''
        raise NotImplemented()
