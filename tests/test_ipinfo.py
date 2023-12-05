import os
import sys
import unittest

current_directory = os.getcwd()
sys.path.append(current_directory)


class TestIpExtraction(unittest.TestCase):
    def test_wan_values(self):

        # self.assertEqual(olt_rx_ont_value, "-22.22")
        pass


if __name__ == "__main__":
    unittest.main()
