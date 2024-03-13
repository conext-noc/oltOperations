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
from helpers.constants.regext_test_cases import install_new_values
from helpers.utils.decoder import check, check_iter
newCondFSP = "F/S/P               : "

class TestRegexExtraction(unittest.TestCase):
    def test_optical_values(self):
        newCond = "----------------------------------------------------------------------------"
        regex = check_iter(install_new_values, newCond)
        for ont in range(len(regex) - 1):
            (_, s) = regex[ont]
            (e, _) = regex[ont + 1]
            result = install_new_values[s:e]
            
            data = check(result, newCondFSP).span()
            print(data)

if __name__ == "__main__":
    unittest.main()
