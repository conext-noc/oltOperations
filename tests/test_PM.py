import json
import os
import re
import sys
import unittest

current_directory = os.getcwd()
sys.path.append(current_directory)

from helpers.handlers.printer import inp
from helpers.utils.decoder import check_iter, decoder
from scripts.plan_migration import migration
from helpers.utils.ssh import ssh
from helpers.constants.definitions import olt_devices
OLT="1"

class TestRegexExtraction(unittest.TestCase):
    def test_get_ont_version(self):
        (comm, command, quit_ssh) = ssh(olt_devices[OLT], False)
        migration(comm, command, quit_ssh, "1", action="all")


if __name__ == "__main__":
    unittest.main()
