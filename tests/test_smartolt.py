import json
import os
import sys
from time import sleep
import requests
import unittest

from helpers.finder.optical import optical_values
from helpers.handlers.add_onu import add_client
from helpers.handlers.spid import calculate_spid
from helpers.handlers.wan_handler import wan_data

current_directory = os.getcwd()
sys.path.append(current_directory)

from helpers.constants.definitions import olt_devices, endpoints
from helpers.utils.ssh import ssh
from helpers.handlers.request import db_request

OLT = "1"
DEBUG = True
ONU_2_INSTALL = "485754430B0A32A9"
PLAN_2_INSTALL = "OZ_MAX_A"


class TestSmartOLTIntegration(unittest.TestCase):
    def test_install_client(self):
        (comm, command, quit_ssh) = ssh(olt_devices[OLT], DEBUG)
        url = "https://conext.smartolt.com/api/onu/unconfigured_onus"
        response = requests.request(
            "GET", url, headers={"X-Token": os.environ["SMART_OLT_API_KEY"]}, data={}
        ).json()

        client = {}

        unconf_onus = []
        if response["status"]:
            for onu in response["response"]:
                unconf_onus.append(
                    {
                        "olt": onu["olt_id"],
                        "slot": onu["board"],
                        "port": onu["port"],
                        "fsp": f"0/{onu['board']}/{onu['port']}",
                        "sn": f"48575443{onu['sn'][4:]}",
                        "device": onu["onu_type_name"],
                    }
                )

            for onu in unconf_onus:
                # print(onu)
                if ONU_2_INSTALL == onu["sn"]:
                    client = onu

            client["frame"] = int(client["fsp"].split("/")[0])
            client["slot"] = int(client["fsp"].split("/")[1])
            client["port"] = int(client["fsp"].split("/")[2])

            client["plan_name"] = PLAN_2_INSTALL

            db_plans = db_request(endpoints["get_plans"], {})["data"]
            plan_lists = [item["plan_name"] for item in db_plans]

            if client["plan_name"] not in plan_lists:
                print("El plan ingresado no existe...", "fail")
                return

            plan = next(
                (item for item in db_plans if item["plan_name"] == client["plan_name"]),
                None,
            )

            client["line_profile"] = plan["line_profile"]
            client["srv_profile"] = plan["srv_profile"]
            client["wan"] = [plan]

            client["name_1"] = "TEST"
            client["name_2"] = "SMARTOLT"
            client["contract"] = "7600000001"

            (client["onu_id"], client["fail"]) = add_client(comm, command, client)

            (client["temp"], client["pwr"], client["pwr_rx"]) = optical_values(
                comm, command, client, True
            )
            url = f"https://conext.smartolt.com/api/onu/get_onu_details/HWTC{client['sn'][8:]}"
            ip_and_mask = requests.request(
                "GET",
                url,
                headers={"X-Token": os.environ["SMART_OLT_API_KEY"]},
                data={},
            ).json()
            if ip_and_mask["status"]:
                client["ip"] = ip_and_mask["onu_details"]["ip_address"]

            url = f"https://conext.smartolt.com/api/onu/update_location_details/HWTC{client['sn'][8:]}"
            update_location_response = requests.request(
                "POST",
                url,
                headers={"X-Token": os.environ["SMART_OLT_API_KEY"]},
                data=
{
    "zone": "Zone 1",
    "address_or_comment": "Avenida 5 de julio",
    "contract":"+58 414-1234567",
    "latitude": "10.653860",
    "longitude": "-71.645966",
},
            ).json()
        
            print(json.dumps(client))


if __name__ == "__main__":
    unittest.main()
