import unittest
import sys

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

    def test_mode_conversion1(self):
        converter = ModelConverter()
        print(converter.convert("Splunk_TA_cisco-asa"))

    def test_mode_conversion2(self):
        converter = ModelConverter()
        print(converter.convert("Splunk_TA_web"))

    def test_mode_conversion3(self):
        converter = ModelConverter()
        print(converter.convert("Splunk_TA_windows"))


if __name__ == '__main__':
    unittest.main()
