from modules import StorageModule
from logging import getLogger
import os
from uuid import uuid1


class SimpleStorage(StorageModule):
    """
    Simple Storage Module

    """
    def __init__(self, storage_dir='/tmp/storage'):
        """
        SimpleStorage initialization

        :param string storage_dir: directory where files will be stored (must exist)
        """
        super(SimpleStorage, self).__init__()
        self.storage_dir = storage_dir

    # Public Interface
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
        return '%s.dat' % uuid1().hex

    def assign(self, context, module_data, stream):
        '''
        Assigns data to the item represented by the 'module_data' reserved
        with the 'new_data' method.

        :param dict context: the storage context (defined above)
        :param str module_data: - opaque module data
        :param stream stream: - input data stream
        :returns: None

        '''
        file_path = os.path.join(self.storage_dir, module_data)

        try:
            with open(file_path, 'w') as ofile:
                data = stream.read(64000)
                while data:
                    ofile.write(data)
                    data = stream.read(64000)
        except Exception, e:
            getLogger(__name__).exception('Exception storing file data:')
            try:
                os.remove(file_path)
            except:
                getLogger(__name__).error('Could not clean up orphan file: %s' % repr(file_path))
            raise e

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
        file_path = os.path.join(self.storage_dir, module_data)
        return os.path.exists(file_path)

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
        file_path = os.path.join(self.storage_dir, module_data)
        return open(file_path, 'r')

    def delete(self, context, module_data):
        '''
        Destroys file content stored in the module.
        Called by the platform when it wishes to delete any data pointed to
        by 'module_data'.

        :param dict context: the storage context
        :param str module_data: - opaque module data
        :returns: None
        '''
        file_path = os.path.join(self.storage_dir, module_data)

        if os.path.exists(file_path):
            os.remove(file_path)

    def get_size(self, context, module_data):
        '''
        Called to get the size of data pointed to by 'module_data'

        :param dict context: the storage context
        :param str module_data: - opaque module data
        :returns: size of object if present
        :rtype: int

        '''
        file_path = os.path.join(self.storage_dir, module_data)
        return os.path.getsize(file_path)

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
        capacity = {}

        try:
            s = os.statvfs(self.storage_dir)
        except:
            # Directory doesn't exist
            getLogger(__name__).error("Mount point : '%s' doesn't exist!", self.storage_dir)
            capacity['total'] = -1
            capacity['free'] =  -1
            capacity['used'] = -1
        else:
            capacity = {}
            capacity['total'] = (s.f_frsize * s.f_blocks)
            capacity['free'] =  (s.f_bavail * s.f_frsize)
            capacity['used'] = capacity['total'] - capacity['free']

        stats = {}
        stats['capacity'] = capacity

        return stats

