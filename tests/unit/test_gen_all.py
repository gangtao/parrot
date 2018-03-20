import unittest
import sys
import os
import json

sys.path.append('../../src')

from model.converter import ModelConverter
from model.gen import Generator


class TestGenAll(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.file1 = "output.json"
        self.count = 1000
        try:
            os.remove(self.file1)
        except:
            pass

    def tearDown(self):
        pass

    def test_gen(self):
        converter = ModelConverter()
        model1 = converter.convert("Splunk_TA_cisco-asa")
        generator1 = Generator(model1)
        result1 = generator1.generate(["samplelog_vpn.cisco.asa", "abnormalities.cisco.asa",
                                       "samplelog_tcp_connection.cisco.asa", "samplelog_access.cisco.asa"], self.count)

        model2 = converter.convert("Splunk_TA_web")
        generator2 = Generator(model2)
        result2 = generator2.generate(["sample.websense"], self.count)

        model3 = converter.convert("Splunk_TA_windows")
        generator3 = Generator(model3)
        result3 = generator3.generate(["sample.websense"], self.count)

        with open(self.file1, "w") as output:
            output.write(json.dumps(result1+result2+result3))


if __name__ == '__main__':
    unittest.main()
