import json
import os
import re
import sys
import unittest
from dotenv import load_dotenv
from pysnmp.hlapi import (
    CommunityData,
    ContextData,
    ObjectType,
    ObjectIdentity,
    UdpTransportTarget,
    bulkCmd,
    SnmpEngine,
)

load_dotenv()

current_directory = os.getcwd()
sys.path.append(current_directory)

from helpers.handlers.request import db_request
from helpers.constants.definitions import olt_devices, snmp_oid, endpoints, payload


class SNMPBulk:
    def __init__(self, target, *oids):
        self.community = CommunityData(os.environ["SNMP_COMMUNITY"])
        self.target = UdpTransportTarget((target, 161))
        self.context = ContextData()
        self.non_repeaters = 10
        self.max_repetitions = 10
        self.oids = [ObjectType(ObjectIdentity(oid)) for oid in oids]

    def execute(self):
        error_indication, error_status, error_index, data = next(
            bulkCmd(
                SnmpEngine(),
                self.community,
                self.target,
                self.context,
                self.non_repeaters,
                self.max_repetitions,
                *self.oids,
            )
        )
        return error_indication, error_status, error_index, data


class TestSnmpBulkCompiler(unittest.TestCase):
    def test_snmp_bulk(self):
        port = db_request(endpoints["get_ports"], {})["data"][0] or {}
        payload["lookup_type"] = "VP"
        payload["lookup_value"] = {
            "fsp": port["fspo"].split("-")[0],
            "olt": port["fspo"].split("-")[1],
        }
        clients_req = db_request(endpoints["get_clients"], payload)["data"]
        for client in clients_req:
            ont_id = "" if client[ "onu_id"] == 0 else f".{int(client['onu_id'])-1}"
            snmp = SNMPBulk(
                olt_devices[str(1)],
                f'{snmp_oid["descr"]}.{port["oid"]}.{ont_id}',
                f'{snmp_oid["serial"]}.{port["oid"]}.{ont_id}',
                f'{snmp_oid["power"]}.{port["oid"]}.{ont_id}',
                f'{snmp_oid["ldc"]}.{port["oid"]}.{ont_id}',
                f'{ snmp_oid["lddt"]}.{port["oid"]}.{ont_id}',
            )
            error_indication, error_status, error_index, data = snmp.execute()
            for clt in data:
                print(clt)
        pass


if __name__ == "__main__":
    unittest.main()
