import json
import os
import requests
from datetime import datetime
from helpers.constants.definitions import (
    AvailableOnu,
    OnuAlarmResponse,
    OnuDeactivatedResponse,
    OnuLookup,
    Client,
    InstallRequest,
    Zone,
    ODB
)
from typing import Dict, List, Union
from dotenv import load_dotenv

load_dotenv()


class SmartOLT():
    """This class handles all SmartOLT Connection handlers like, get_onus/update_onus"""

    def __init__(self) -> None:
        """Initializer class"""
        self.token = os.getenv("SMART_OLT_API_KEY")
        self.smart_olt_domain = os.getenv("SMART_OLT_DOMAIN")
        self.header = "X-Token"

    ############################### GET REQUESTS ###############################

    def get_available_onus(self) -> List[AvailableOnu]:
        """_summary_

        Returns:
            List[AvailableOnu]: _description_
        """
        onus = []
        url = f"{self.smart_olt_domain}/api/onu/unconfigured_onus"
        response = requests.request(
            "GET",
            url,
            headers={f"{self.header}": os.environ["SMART_OLT_API_KEY"]},
            data={},
        )
        if response.status_code != 200:
            return []

        for onu in response.json()["response"]:
            onus.append(
                AvailableOnu(
                    frame=0,
                    slot=int(onu["board"]),
                    port=int(onu["port"]),
                    olt=int(onu["olt_id"]),
                    fsp=f"0/{onu['board']}/{onu['port']}",
                    device=onu["onu_type_name"],
                    sn=onu["sn"],
                )
            )
        return onus

    def get_client(
        self,
        *,
        is_bulk: bool,
        lookup: OnuLookup,
    ) -> List[Client]:
        """_summary_

        Args:
            is_bulk (bool): _description_
            lookup (OnuLookup): _description_

        Returns:
            List[Client]: _description_
        """

        url = f"{self.smart_olt_domain}/api/onu/get_all_onus_details?olt_id={lookup.olt}&board={lookup.slot}&port={lookup.port}"
        response = requests.request(
            "GET",
            url,
            headers={f"{self.header}": os.environ["SMART_OLT_API_KEY"]},
            data={},
        )
        if response.status_code != 200:
            print("error in smartolt")  # log an error
            return []
        onus_list = []
        if is_bulk:
            onus_list = response.json()["onus"]
        if not is_bulk:
            onus_list = [
                onu
                for onu in response.json()["onus"]
                if onu["sn"][4:] == lookup.external_id[8:]
            ]
        response: List[Client] = []
        for onu in onus_list:
            response.append(
                Client(
                    name=str(onu["name"]),
                    frame=0,
                    slot=int(onu["board"]),
                    port=int(onu["port"]),
                    onu_id=int(onu["onu"]),
                    olt=int(onu["olt_id"]),
                    status=str(onu["status"]),
                    state=str(onu["administrative_status"]),
                    signal=str(onu["signal"]),
                    longitude=float(
                        onu["longitude"] if onu["longitude"] is not None else 0.0
                    ),
                    latitude=float(
                        onu["latitude"] if onu["latitude"] is not None else 0.0
                    ),
                    power=float(
                        onu["signal_1310"] if onu["signal_1310"] is not None else 0.0
                    ),
                    zone=str(onu["zone_name"]),
                    odb=str(onu["odb_name"]),
                    mode=str(onu["mode"]),
                    device=str(onu["onu_type_name"]),
                    sn=str(onu["sn"]),
                )
            )
        return response

    def get_alarms(self, *, olt: int) -> List[OnuAlarmResponse]:
        """Returns a list of all the current ONUs in LOS status

        Args:
            olt (int): OLT id

        Returns:
            List[SmartOLTOnuAlarmResponse]: list of all the current LOS ONUs
        """
        url = f"{self.smart_olt_domain}/api/onu/get_onus_statuses?olt_id={olt}"
        response = requests.request(
            "GET",
            url,
            headers={f"{self.header}": os.environ["SMART_OLT_API_KEY"]},
            data={},
        )
        url_zones = f"{self.smart_olt_domain}/api/system/get_zones"
        response_zones = requests.request(
            "GET",
            url_zones,
            headers={f"{self.header}": os.environ["SMART_OLT_API_KEY"]},
            data={},
        )
        zones = response_zones.json()["response"]
        los_onus = []
        time_now = datetime.now()
        for onu in response.json()["response"]:
            if onu["status"] == "LOS" and onu["last_status_change"]:
                last_status_change = datetime.strptime(
                    onu["last_status_change"], "%Y-%m-%d %H:%M:%S"
                )
                time_diff = time_now - last_status_change
                total_days = time_diff.days
                (
                    los_onus.append(
                        OnuAlarmResponse(
                            sn=["sn"],
                            frame=0,
                            slot=onu["board"],
                            port=onu["port"],
                            onu_id=onu["onu"],
                            olt=olt,
                            status="LOSi",
                            date=onu["last_status_change"],
                            zone=[
                                zone
                                for zone in zones
                                if int(zone["id"]) == int(onu["zone_id"])
                            ][0]["name"],
                        )
                    )
                    if total_days <= 3
                    else None
                )
        return los_onus

    def get_deactivated(self, *,olt: int) -> List[OnuDeactivatedResponse]:
        """Returns a list of all current ONUs in Deactivated administrative status

        Args:
            olt (int): OLT id

        Returns:
            List[OnuDeactivatedResponse]: list of all current Deactivated ONUs
        """
        url = f"{self.smart_olt_domain}/api/onu/get_onus_administrative_statuses?olt_id={olt}"
        response = requests.request(
            "GET",
            url,
            headers={f"{self.header}": os.environ["SMART_OLT_API_KEY"]},
            data={},
        )
        url_zones = f"{self.smart_olt_domain}/api/system/get_zones"
        response_zones = requests.request(
            "GET",
            url_zones,
            headers={f"{self.header}": os.environ["SMART_OLT_API_KEY"]},
            data={},
        )
        zones = response_zones.json()["response"]
        deact_onus = []
        for onu in response.json()["response"]:
            if onu["admin_status"] == "Disabled":
                deact_onus.append(
                    OnuDeactivatedResponse(
                        sn="48575443" + onu["sn"][4:],
                        frame=0,
                        slot=onu["board"],
                        port=onu["port"],
                        onu_id=onu["onu"],
                        olt=olt,
                        state="deactivated",
                        zone=[
                            zone
                            for zone in zones
                            if int(zone["id"]) == int(onu["zone_id"])
                        ][0]["name"],
                    )
                )
        return deact_onus

    def olt_ports(self, *,olt):
        url = f"{self.smart_olt_domain}/api/system/get_olt_pon_ports_details/{olt}"
        response = requests.request(
            "GET",
            url,
            headers={f"{self.header}": os.environ["SMART_OLT_API_KEY"]},
            data={},
        )
        print(json.dumps(response.json()))

    def get_zones(self) -> List[Zone]:
        zones = []
        url = f"{self.smart_olt_domain}/api/system/get_zones"
        response = requests.request(
            "GET",
            url,
            headers={f"{self.header}": os.environ["SMART_OLT_API_KEY"]},
            data={},
        )

        for zone in response.json()["response"]:
            zone["zone_id"] = int(zone["id"])
            del zone["id"]
            zones.append(Zone(**zone))
        return zones

    def get_odbs(self, *, zone_id: int) -> List[ODB]:
        odbs = []
        url = f"{self.smart_olt_domain}/api/system/get_odbs/{zone_id}"
        response = requests.request(
            "GET",
            url,
            headers={f"{self.header}": os.environ["SMART_OLT_API_KEY"]},
            data={},
        )
        for odb in response.json()["response"]:
            odb["odb_id"] = int(odb["id"])
            odb["ports"] = int(odb["nr_of_ports"])
            odb["zone_id"] = int(odb["zone_id"])
            odb["latitude"] = float(odb["latitude"])
            odb["longitude"] = float(odb["longitude"])
            del odb["id"]
            del odb["nr_of_ports"]
            odbs.append(ODB(**odb))
        return odbs
        #     zone["zone_id"] = zone["id"]
        #     del zone["id"]
        #     zones.append(Zone(**zone))
        # return zones

    ############################### POST REQUESTS ###############################

    def onu_add(self, *, onu_data: InstallRequest):
        """_summary_

        Args:
            onu_data (dict): _description_
        """
        url = f"{self.smart_olt_domain}/api/onu/authorize_onu"
        response = requests.request(
            "POST",
            url,
            headers={f"{self.header}": os.environ["SMART_OLT_API_KEY"]},
            data=json.dumps(onu_data.to_json()),
        )
        return response.json()


    def operate_onu(self, *, onu_sns: List[str], action: str):
        """Enables/Disable ONU's administrative status

        Args:
            onu_sns (List[str]): List of onu's SN
            action (str): type of batch action [enable|disable]

        Returns:
            _type_: _description_
        """
        url = f"{self.smart_olt_domain}/api/onu/bulk_{action}"
        response = requests.request(
            "POST",
            url,
            headers={f"{self.header}": os.environ["SMART_OLT_API_KEY"]},
            data={'onus_external_ids': ','.join(onu_sns)},
        )
        return response.json()

    def update_onu_sn(self, *, old_sn: str, new_sn: str):
        """ Changes the Current sn of the selected onu

        Args:
            old_sn (str): old onu's sn
            new_sn (str): new onu's sn
HWTC9E21307D
        Returns:
            _type_: _description_
        """
        url = f"{self.smart_olt_domain}/api/onu/update_sn/{old_sn}"
        response = requests.request(
            "POST",
            url,
            headers={"X-Token": os.environ["SMART_OLT_API_KEY"]},
            data={'new_sn': new_sn},
        )
        return response.json()

    def onu_tr069(self, *, onu_sn, operation):
        """_summary_
        https://{{subdomain}}.smartolt.com/api/onu/enable_tr069/{{onu_external_id}}
        https://{{subdomain}}.smartolt.com/api/onu/disable_tr069/{{onu_external_id}}
        """

    def onu_static_ip(self, *, onu_sn, ipv4, mask, gateway, dns1, dns2):
        """_summary_
        https://{{subdomain}}.smartolt.com/api/onu/set_onu_wan_mode_static_ip/{{onu_external_id}}
        payload={'ipv4_address': '10.100.0.11',
        'subnet_mask': '255.255.255.0',
        'gateway': '10.100.0.1',
        'dns1': '8.8.8.8',
        'dns2': '8.8.4.4'}"""

    def onu_remote_access(self, *, onu_sn, operation):
        """_summary_
        https://{{subdomain}}.smartolt.com/api/onu/enable_allow_remote_access_to_wan_ip/{{onu_external_id}}
        https://{{subdomain}}.smartolt.com/api/onu/disable_allow_remote_access_to_wan_ip/{{onu_external_id}}"""
        
    def onu_reboot(self, *, onu_sn):
        """_summary_
        https://{{subdomain}}.smartolt.com/api/onu/reboot/{{onu_external_id}}
        """
        
    def onu_resync(self, *, onu_sn):
        """_summary_
        https://{{subdomain}}.smartolt.com/api/onu/resync_config/{{onu_external_id}}
        """

    def onu_reset(self, *, onu_sn):
        """_summary_
        https://{{subdomain}}.smartolt.com/api/onu/restore_factory_defaults/{{onu_external_id}}
        """
        
    def onu_delete(self, *, onu_sn):
        """_summary_
        https://{{subdomain}}.smartolt.com/api/onu/delete/{{onu_external_id}}
        """
