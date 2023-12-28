import json
import os
import re
import sys
import unittest
from helpers.handlers.printer import inp
from helpers.utils.decoder import check_iter, decoder

current_directory = os.getcwd()
sys.path.append(current_directory)

from helpers.utils.ssh import ssh
from helpers.constants.definitions import olt_devices

OLT = "1"
devices = [
    {"frame": 0, "slot": 1, "port": 1, "onu_id": 35},
    {"frame": 0, "slot": 1, "port": 1, "onu_id": 39},
    {"frame": 0, "slot": 1, "port": 1, "onu_id": 26},
    {"frame": 0, "slot": 1, "port": 3, "onu_id": 6},
    {"frame": 0, "slot": 1, "port": 0, "onu_id": 28},
    {"frame": 0, "slot": 4, "port": 5, "onu_id": 60},
    {"frame": 0, "slot": 1, "port": 5, "onu_id": 60},
]


class TestRegexExtraction(unittest.TestCase):
    def test_get_ont_version(self):
        (comm, command, quit_ssh) = ssh(olt_devices[OLT], False)
        for device in devices:
            command(f"interface gpon {device['frame']}/{device['slot']}")
            command(f"display ont version {device['port']} {device['onu_id']}")
            output = decoder(comm)
            regex = check_iter(
                output,
                "--------------------------------------------------------------------------",
            )
            if len(regex) > 0:
                [(_, start), (end, _)] = regex
                equipment_id = (
                    re.sub(
                        " +",
                        " ",
                        re.search(r"Equipment-ID\s+:\s+[^\n]+", output[start:end]).group(),
                    )
                    .replace(" \r", "")
                    .replace("Equipment-ID : ", "")
                )

                print(equipment_id)
            else:
                continue
        quit_ssh()


if __name__ == "__main__":
    unittest.main()
