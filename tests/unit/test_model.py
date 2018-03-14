import unittest

import sys
import json
import time

sys.path.append('../../src')

from model.converter import ModelConverter

class TestModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mode_conversion(self):
        converter = ModelConverter()
        print(converter.convert("Splunk_TA_cisco-asa"))


if __name__ == '__main__':
    unittest.main()
