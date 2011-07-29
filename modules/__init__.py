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

        :param kwargs: list of arguments needed for the module to initialize
        '''
        pass

    def new_data(self, context):
        '''
        Called by the platform when a new file data object needs to be reserved.

        A new ticket should be created and returned by this call that can be
        used by passing it to 'assign' along with a stream containing the data
        to be stored in the module.

        :param dict context: the storage context (defined above)
        :returns: module_data - opaque module data
        :rtype: str

        '''
        raise NotImplemented()

    def assign(self, context, module_data, stream):
        '''
        Assigns data to the item represented by the 'module_data' reserved
        with the 'new_data' method.

        :param dict context: the storage context (defined above)
        :param str module_data: - opaque module data
        :param stream stream: - input data stream
        :returns: None

        '''
        raise NotImplemented()

    def available(self, context, module_data):
        '''
        Checks if this storage object is present in the module.

        If the storage subsystem supports asynchronously transferring data
        the response is required to be True.

        :param dict context: the storage context (defined above)
        :param str module_data: - opaque module data
        :returns: True if present else False
        :rtype: boolean

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

    def get_size(self, context, module_data):
        '''
        Called to get the size of data pointed to by 'module_data'

        :param dict context: the storage context
        :param str module_data: - opaque module data
        :returns: size of object if present
        :rtype: int

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
