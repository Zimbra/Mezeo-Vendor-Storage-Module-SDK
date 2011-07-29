# -*- coding: utf-8 -*-
import random
import string
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class StorageModuleTestBase(object):
    """
    Storage module test base

    All tests non-module specific tests reside here
    """
    def setUp(self, connector, extra_context):
        """
        Common setUp function

        Sets up the environment and adds any extra environment values into
        the test environment
        """
        self.connector = connector

        self.context = {

        }

        # Add our extra environment values
        self.context.update(extra_context)

    def tearDown(self):
        """
        Common tearDown function
        """
        pass

    def randomBuffer(self, length=1):
        """
        Return a random buffer of the specified length
        Only letters and numbers are used
        """
        return ''.join(random.choice(string.letters + string.digits) for i in xrange(length))

    def compareWrittenData(self, fileInfo, data):
        """
        This method is supposed to validate that the data written using the vendor
        module is correct.

        Since the process of doing this validation is module specific this must be implemented
        in the vendor specific test suite code.
        """
        raise NotImplemented("This method must be implemented in any subclasses")


    def testWrite(self):
        """
        validate 1 megabyte of data written is correct

        """
        datalen = 1024 * 1024
        data = self.randomBuffer(datalen)

        module_data = self.connector.new_data(self.context)

        self.connector.assign(self.context, module_data, StringIO(data))

        self.assertTrue(self.compareWrittenData(module_data, data),
                        "File data contents does NOT match the data buffer written")

    def testWriteThenRead(self):
        """
        validate 1 megabyte of data written is read back correctly

        """
        datalen = 1024 * 1024
        data = self.randomBuffer(datalen)

        module_data = self.connector.new_data(self.context)

        self.connector.assign(self.context, module_data, StringIO(data))

        self.assertTrue(self.compareWrittenData(module_data, data),
                        "Intial data written does NOT match the data buffer written")

        # Get the stream to read the data back
        gets = self.connector.get_read_stream(self.context, module_data)
        read_data = gets.read()
        self.assertTrue(data == read_data,
                        "Data doesn't match")

    def testAvailable(self):
        datalen = 1024 * 1024
        data = self.randomBuffer(datalen)

        module_data = self.connector.new_data(self.context)

        self.connector.assign(self.context, module_data, StringIO(data))
        self.assertTrue(self.connector.available(self.context, module_data),
                        "Module data was not available")

    def testNotAvailable(self):
        module_data = self.connector.new_data(self.context)

        self.assertTrue(not self.connector.available(self.context, module_data),
                        "Module data was available when it shouldn't be")
