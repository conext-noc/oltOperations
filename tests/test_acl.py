import os
import sys
import unittest
import ipaddress
from dotenv import load_dotenv
from helpers.handlers.file_formatter import data_to_dict

load_dotenv()

current_directory = os.getcwd()
sys.path.append(current_directory)

from helpers.handlers.printer import inp
from helpers.constants.definitions import rtr_devices, olt_devices
from helpers.utils.ssh import ssh
from helpers.utils.decoder import decoder, check_iter, check


class DevicesACL(unittest.TestCase):
    ipv4_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    sample_db_api_response = {
        "message": "Success!",
        "error": False,
        "data": [
            {
                "rule_id": 1,
                "name": "ops-env-rule",
                "rtr_acl_name": "SSH_ACCESS",
                "olt_acl_name": "3000",
                "rtr_rule_id": 8,
                "olt_rule_id": 8,
                "ip_addr": "52.36.152.69",
            },
            {
                "rule_id": 2,
                "name": "sch-env-rule",
                "rtr_acl_name": "SSH_ACCESS",
                "olt_acl_name": "3000",
                "rtr_rule_id": 12,
                "olt_rule_id": 12,
                "ip_addr": "54.213.11.170",  # 54.213.11.171
            },
            {
                "rule_id": 3,
                "name": "mon-env-rule",
                "rtr_acl_name": "SSH_ACCESS",
                "olt_acl_name": "3000",
                "rtr_rule_id": 9,
                "olt_rule_id": 9,
                "ip_addr": "34.221.165.245",
            },
            {
                "rule_id": 4,
                "name": "mod-env-rule",
                "rtr_acl_name": "SSH_ACCESS",
                "olt_acl_name": "3000",
                "rtr_rule_id": 7,
                "olt_rule_id": 7,
                "ip_addr": "35.91.9.72",
            },
            {
                "rule_id": 5,
                "name": "ins-ms-rule",
                "rtr_acl_name": "SSH_ACCESS",
                "olt_acl_name": "3000",
                "rtr_rule_id": 11,
                "olt_rule_id": 11,
                "ip_addr": "35.93.66.254",
            },
        ],
    }

    def test_olt_acls(self):
        device = inp("Select OLT [1 | 2 | 3] : ")
        if device not in olt_devices:
            self.fail("device not supported")

        (comm, command, quit_ssh) = ssh(olt_devices[device], debugging=True)

        command("acl 3000")
        command("display this")
        value = decoder(comm)
        re_acl = check_iter(value, "#")
        acl_start_id_name = 10
        acl_start = re_acl[-3][1] + acl_start_id_name
        acl_end = re_acl[-2][0]

        live_olt_rules = [
            {"olt_rule_id": rule["olt_rule_id"], "ip_addr": rule["ip_addr"]}
            for rule in data_to_dict(
                "unused_1,olt_rule_id,unused_2,unused_3,unused_4,ip_addr,unused_5",
                value[acl_start:acl_end],
            )
            if rule["unused_2"] != "deny"
        ]

        def is_valid_ip(ip_address):
            try:
                ipaddress.ip_address(ip_address)
                return True
            except ValueError:
                return False

        self.assertTrue(any(is_valid_ip(rule["ip_addr"]) for rule in live_olt_rules))
        quit_ssh()
        return

    def test_rtr_acls(self):
        device = inp("Select Router [E1 | E2 | A1 | A2] : ")
        if device not in rtr_devices:
            self.fail("device not supported")

        (comm, command, quit_ssh) = ssh(rtr_devices[device], debugging=True)

        command("acl name SSH_ACCESS")
        command("display this")
        value = decoder(comm)
        
        re_acl = check_iter(value, "#")
        acl_start = check(value, "rule 1 permit").span()[0] - 1
        acl_end = re_acl[-1][0]
        live_rtr_rules = [
            {"rtr_rule_id": rule["rtr_rule_id"], "ip_addr": rule["ip_addr"]}
            for rule in data_to_dict(
                "NA,unused_1,rtr_rule_id,unused_2,unused_3,unused_4,ip_addr,unused_5",
                value[acl_start:acl_end],
            )
            if rule["unused_2"] != "deny"
        ]
        
        def is_valid_ip(ip_address):
            try:
                ipaddress.ip_address(ip_address)
                return True
            except ValueError:
                return False

        self.assertTrue(any(is_valid_ip(rule["ip_addr"]) for rule in live_rtr_rules))
        quit_ssh()
        return

    def test_rtr_acl_check(self):
        device = inp("Select Router [E1 | E2 | A1 | A2] : ")
        if device not in rtr_devices:
            self.fail("device not supported")

        (comm, command, quit_ssh) = ssh(rtr_devices[device], debugging=True)

        command("acl name SSH_ACCESS")
        command("display this")
        value = decoder(comm)
        
        re_acl = check_iter(value, "#")
        acl_start = check(value, "rule 1 permit").span()[0] - 1
        acl_end = re_acl[-1][0]
        
        live_rtr_rules = [
            {"rtr_rule_id": rule["rtr_rule_id"], "ip_addr": rule["ip_addr"]}
            for rule in data_to_dict(
                "NA,unused_1,rtr_rule_id,unused_2,unused_3,unused_4,ip_addr,unused_5",
                value[acl_start:acl_end],
            )
            if rule["unused_2"] != "deny"
        ]

        acl_db_rules_rtr = [
            rule["rtr_rule_id"] for rule in self.sample_db_api_response["data"]
        ]
        acl_rtr_rules = [rule["rtr_rule_id"] for rule in live_rtr_rules]

        for live_rtr_rule in acl_rtr_rules:
            for db_rtr_rule in acl_db_rules_rtr:
                if int(live_rtr_rule) == int(db_rtr_rule):
                    live_rule = [
                        rule
                        for rule in live_rtr_rules
                        if int(rule["rtr_rule_id"]) == int(db_rtr_rule)
                    ][0]
                    db_rule = [
                        rule
                        for rule in self.sample_db_api_response["data"]
                        if int(rule["rtr_rule_id"]) == int(db_rtr_rule)
                    ][0]
                    
                    rule_condition = live_rule["ip_addr"] == db_rule["ip_addr"]
                    
                    self.assertTrue(rule_condition) if rule_condition else self.assertFalse(rule_condition, "MISMATCH ON IP FOUND")
        quit_ssh()
        return

    def test_olt_acl_check(self):
        device = inp("Select OLT [1 | 2 | 3] : ")
        if device not in olt_devices:
            self.fail("device not supported")

        (comm, command, quit_ssh) = ssh(olt_devices[device], debugging=True)

        command("acl 3000")
        command("display this")
        value = decoder(comm)
        re_acl = check_iter(value, "#")
        acl_start_id_name = 10
        acl_start = re_acl[-3][1] + acl_start_id_name
        acl_end = re_acl[-2][0]

        live_olt_rules = [
            {"olt_rule_id": rule["olt_rule_id"], "ip_addr": rule["ip_addr"]}
            for rule in data_to_dict(
                "unused_1,olt_rule_id,unused_2,unused_3,unused_4,ip_addr,unused_5",
                value[acl_start:acl_end],
            )
        ]

        acl_db_rules_olt = [
            rule["olt_rule_id"] for rule in self.sample_db_api_response["data"]
        ]
        acl_olt_rules = [rule["olt_rule_id"] for rule in live_olt_rules]

        for live_olt_rule in acl_olt_rules:
            for db_olt_rule in acl_db_rules_olt:
                if int(live_olt_rule) == int(db_olt_rule):
                    live_rule = [
                        rule
                        for rule in live_olt_rules
                        if int(rule["olt_rule_id"]) == int(db_olt_rule)
                    ][0]
                    db_rule = [
                        rule
                        for rule in self.sample_db_api_response["data"]
                        if int(rule["olt_rule_id"]) == int(db_olt_rule)
                    ][0]
                    
                    rule_condition = live_rule["ip_addr"] == db_rule["ip_addr"]
                    
                    self.assertTrue(rule_condition) if rule_condition else self.assertFalse(rule_condition, "MISMATCH ON IP FOUND")
        quit_ssh()
        return


if __name__ == "__main__":
    unittest.main()
