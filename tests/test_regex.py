import os
import re
import sys
import unittest

from helpers.handlers.fail import fail_checker

current_directory = os.getcwd()
sys.path.append(current_directory)

from helpers.constants.regex_conditions import (
    condition_onu_pwr_rx,
    condition_onu_temp,
    condition_onu_pwr,
)
from helpers.constants.regext_test_cases import install_new_values, version_values
from helpers.utils.decoder import check, check_iter

newCondFSP = "F/S/P               : "


class TestRegexExtraction(unittest.TestCase):
    def test_version_values(self):
        ONT_VERSION = None
        ONT_EQUIPMENT_ID = None
        output = version_values
        FAIL = fail_checker(output)
        if FAIL is None:
            version_match = re.search(r"Main Software Version\s+:\s+(\S+)", output)
            if version_match:
                ONT_VERSION = version_match.group().replace(" \r", "").replace("Main Software Version    : ", "")
            id_match = re.search(r"Equipment-ID\s+:\s+([^\n]+)", output)
            if id_match:
                ONT_EQUIPMENT_ID = id_match.group(1).replace(" \r", "").replace("Equipment-ID : ", "")

        self.assertIsInstance(ONT_VERSION, str)
        self.assertIsInstance(ONT_EQUIPMENT_ID, str)
        
        self.assertRegex(output, r"Main Software Version\s+:\s+(\S+)")
        self.assertRegex(output, r"Equipment-ID\s+:\s+[^\n]+")

        self.assertEqual(ONT_VERSION, "V5R020C00S080")
        self.assertEqual(ONT_EQUIPMENT_ID, "EG8145X6")

        print("version : ", ONT_VERSION)
        print("equipment id : ", ONT_EQUIPMENT_ID)
    # def test_optical_values(self):
    #     newCond = "----------------------------------------------------------------------------"
    #     regex = check_iter(install_new_values, newCond)
    #     for ont in range(len(regex) - 1):
    #         (_, s) = regex[ont]
    #         (e, _) = regex[ont + 1]
    #         result = install_new_values[s:e]

    #         data = check(result, newCondFSP).span()
    #         print(data)


if __name__ == "__main__":
    unittest.main()
