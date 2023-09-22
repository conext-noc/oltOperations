import os
import sys
import unittest

current_directory = os.getcwd()
sys.path.append(current_directory)

from helpers.constants.regex_conditions import (
    condition_onu_pwr_rx,
    condition_onu_temp,
    condition_onu_pwr,
)
from helpers.constants.regext_test_cases import optical_values
from helpers.utils.decoder import check

class TestRegexExtraction(unittest.TestCase):
    def test_optical_values(self):
        olt_rx_ont_match = check(optical_values, condition_onu_pwr_rx)
        rx_power_match = check(optical_values, condition_onu_pwr)
        temperature_match = check(optical_values, condition_onu_temp)

        self.assertIsNotNone(olt_rx_ont_match, "OLT Rx ONT optical power not found")
        self.assertIsNotNone(rx_power_match, "Rx optical power not found")
        self.assertIsNotNone(temperature_match, "Temperature not found")

        olt_rx_ont_value = olt_rx_ont_match.group(1)
        rx_power_value = rx_power_match.group(1)
        temperature_value = temperature_match.group(1)

        self.assertEqual(olt_rx_ont_value, "-22.22")
        self.assertEqual(rx_power_value, "-18.18")
        self.assertEqual(temperature_value, "58")


if __name__ == "__main__":
    unittest.main()
