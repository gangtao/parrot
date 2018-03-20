import unittest
import sys
import os

sys.path.append('../../src')

from model.converter import ModelConverter
from model.gen import BatchFileGenerator, CSVFileGenerator, JSONFileGenerator


class TestGen(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.file1 = "test1.txt"
        self.file2 = "test2.txt"
        self.file3 = "test3.txt"
        self.file4 = "test4.txt"

        try:
            os.remove(self.file1)
            os.remove(self.file2)
            os.remove(self.file3)
            os.remove(self.file4)
        except:
            pass

    def tearDown(self):
        pass

    def test_batchfilegen1(self):
        converter = ModelConverter()
        model = converter.convert("Splunk_TA_cisco-asa")
        generator = CSVFileGenerator(model, self.file1)
        generator.generate(["samplelog_vpn.cisco.asa"], 10)

    @unittest.skip("testing skipping")
    def test_batchfilegen2(self):
        converter = ModelConverter()
        model = converter.convert("Splunk_TA_cisco-asa")
        generator = CSVFileGenerator(model, self.file2)
        generator.generate(["samplelog_vpn.cisco.asa", "abnormalities.cisco.asa",
                            "samplelog_tcp_connection.cisco.asa", "samplelog_access.cisco.asa"], 30)

    @unittest.skip("testing skipping")
    def test_batchfilegen3(self):
        converter = ModelConverter()
        model = converter.convert("Splunk_TA_web")
        generator = CSVFileGenerator(model, self.file3)
        generator.generate(["sample.websense"], 30)

    @unittest.skip("testing skipping")
    def test_batchfilegen4(self):
        converter = ModelConverter()
        model = converter.convert("Splunk_TA_windows")
        generator = CSVFileGenerator(model, self.file4)
        generator.generate(
            ["Security.4624.windows", "Security.4634.windows", "Security.528.windows"], 30)


if __name__ == '__main__':
    unittest.main()
