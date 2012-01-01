#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest2 as unittest
import os
import shutil

from tests import (
    StorageModuleTestBase
)


class TestSimpleStorage(unittest.TestCase, StorageModuleTestBase):
    """
    Tests the SimpleStorage module

    """
    def setUp(self):
        workdir = '/tmp/simple'
        extra_context = {}

        from simple.simple import SimpleStorage
        connector = SimpleStorage(workdir)

        StorageModuleTestBase.setUp(self, connector, extra_context)

        if not os.path.exists(workdir):
            os.mkdir(workdir)

        # save our workdir for tearDown time
        self.workdir = workdir

    def tearDown(self):
        StorageModuleTestBase.tearDown(self)

        # clean up after ourselves
        shutil.rmtree(self.workdir)

    def compareWrittenData(self, module_data, data):
        """
        Warning: This method depends on the data to be compared fitting into memory!
        """
        file_path = os.path.join(self.workdir, module_data.strip('/'))

        written_data = open(file_path, 'r').read()

        if written_data != data:
            return False
        else:
            return True

    def wasDeleted(self, module_data):
        return not os.path.exists(os.path.join(self.workdir, module_data.strip('/')))
