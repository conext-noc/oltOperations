import os
import sys
from time import sleep
import unittest

from helpers.handlers.spid import calculate_spid

current_directory = os.getcwd()
sys.path.append(current_directory)

from helpers.constants.definitions import olt_devices, endpoints
from helpers.utils.ssh import ssh
from helpers.handlers.request import db_request

OLT = "1"
DEBUG = True
PAYLOAD = {
    "lookup_type": "VP",
    "lookup_value": {
        "fsp": "",
        "olt": OLT,
    },
}


def print_client(client):
    print(
        f"""
NOMBRE          :       {client['name_1']} {client['name_2']}
CONTRATO        :       {client["contract"]}
FSPI            :       {client["fspi"]}
PLAN            :       {client["plan_name_id"]}
INDEX DE PLAN   :       {client["plan_idx"]}
SRV PROFILE     :       {client["srv_profile"]}
LINE PROFILE    :       {client["line_profile"]}
GEM PORT        :       {client["gem_port"]}
VLAN            :       {client["vlan"]}
SPID            :       {client["spid"]}
"""
    )


class TestDataPlanMigration(unittest.TestCase):
    def test_get_client(self):
        # (comm, command, quit_ssh) = ssh(olt_devices[OLT], DEBUG)
        ports = db_request(endpoints["get_ports"], {})["data"]
        data_plans = db_request(endpoints["get_plans"], {})["data"]

        OLD_PLAN = "OZ_0_2"
        NEW_PLAN = "OZ_MAX_2"

        for port_data in ports:
            if OLT == str(port_data["olt"]) and port_data["is_open"]:
                PAYLOAD["lookup_value"][
                    "fsp"
                ] = f'{port_data["frame"]}/{port_data["slot"]}/{port_data["port"]}'
                clients_req = db_request(endpoints["get_clients"], PAYLOAD)["data"]
                for client_req in clients_req:
                    if OLD_PLAN == client_req["plan_name_id"]:
                        data_plan_req = [
                            data_plan
                            for data_plan in data_plans
                            if client_req["plan_name_id"] == data_plan["plan_name"]
                        ][0]
                        spid_data = calculate_spid(client_req)
                        spid = (
                            spid_data["I"]
                            if "IP" in client_req["plan_name_id"]
                            else spid_data["P"]
                        )
                        client = client_req.copy()
                        client.update(data_plan_req)
                        client["spid"] = spid
                        print_client(client)

                        new_plan = [
                            data_plan
                            for data_plan in data_plans
                            if NEW_PLAN == data_plan["plan_name"]
                        ][0]

                        sleep(3)
                        print(f'undo service-port {client["spid"]}')
                        sleep(3)
                        print(f'interface gpon {client["frame"]}/{client["slot"]}')
                        sleep(3)
                        print(
                            f"ont modify {client['port']} {client['onu_id']} ont-lineprofile-id {new_plan['line_profile']}"
                        )
                        sleep(3)
                        print(
                            f"ont modify {client['port']} {client['onu_id']} ont-srvprofile-id {new_plan['srv_profile']}"
                        )
                        sleep(3)

                        print(
                            f'El SPID que se le agregara al cliente es : {client["spid"]}',
                            "ok",
                        )

                        print(f"interface gpon {client['frame']}/{client['slot']}")
                        sleep(3)

                        # check model type then add vlan if needed
                        add_vlan = input("Se agregara vlan al puerto? [Y | N] : ")

                        print(
                            f" ont port native-vlan {client['port']} {client['onu_id']} eth 1 vlan {client['vlan']} "
                        ) if add_vlan == "Y" else None

                        IPADD = (
                            input("Ingrese la IPv4 Publica del cliente : ")
                            if "_IP" in new_plan["plan_name"]
                            else None
                        )

                        sleep(3)

                        internet_index = 2 if client["device"] != "BDCM" else 1

                        print(
                            f"ont ipconfig {client['port']} {client['onu_id']} ip-index 2 dhcp vlan {new_plan['vlan']}"
                        ) if "_IP" not in new_plan["plan_name"] and client[
                            "device"
                        ] != "BDCM" else print(
                            f"ont ipconfig {client['port']} {client['onu_id']} ip-index 2 static ip-address {IPADD} mask 255.255.255.128 gateway 181.232.181.129 pri-dns 9.9.9.9 slave-dns 149.112.112.112 vlan 102"
                        ) if "_IP" in new_plan[
                            "plan_name"
                        ] and client[
                            "device"
                        ] != "BDCM" else print(
                            f"ont ipconfig {client['port']} {client['onu_id']} ip-index 1 dhcp vlan {new_plan['vlan']} priority 0"
                        )
                        sleep(3)

                        if client["device"] == "BDCM":
                            print(
                                f"ont ipconfig {client['port']} {client['onu_id']} ip-index 2 dhcp vlan {new_plan['vlan']} priority 5"
                            )

                        print(
                            f"ont internet-config {client['port']} {client['onu_id']} ip-index {internet_index}"
                        )

                        print(
                            f"ont policy-route-config {client['port']} {client['onu_id']} profile-id 2"
                        )

                        print("quit")
                        sleep(3)
                        print(
                            f"""service-port {client['spid']} vlan {new_plan['vlan']} gpon {client['frame']}/{client['slot']}/{client['port']} ont {client['onu_id']} gemport {new_plan['gem_port']} multi-service user-vlan {new_plan['vlan']} tag-transform transparent inbound traffic-table index {new_plan["plan_idx"]} outbound traffic-table index {new_plan["plan_idx"]}"""
                        )

                        sleep(3)
                        print(f"interface gpon {client['frame']}/{client['slot']}")
                        sleep(3)
                        print(
                            f"ont wan-config {client['port']} {client['onu_id']} ip-index 2 profile-id 0"
                        ) if client["device"] != "BDCM" else print(
                            f"ont wan-config {client['port']} {client['onu_id']} ip-index 1 profile-id 0"
                        )
                        sleep(3)
                        if client["device"] == "BDCM":
                            print(
                                f"ont wan-config {client['port']} {client['onu_id']} ip-index 2 profile-id 0"
                            )
                            print(
                                f"ont fec {client['port']} {client['onu_id']} use-profile-config"
                            )
                            sleep(3)
                        print("quit")
                        sleep(3)


if __name__ == "__main__":
    unittest.main()
