headers = {"Content-Type": "application/json"}
# domain = "http://127.0.0.1:8000"
domain = "http://db-api.conext.net.ve"
payload = {"lookup_type": None, "lookup_value": None}
payload_add = {"data": None}
endpoints = {
    "add_client":"/add-client",
    "get_client":"/get-client",
    "get_clients":"/get-clients",
    "update_client":"/update-client",
    "remove_client":"/remove-client",
    "get_plans":"/get-plans",
    "add_ports":"/add-ports",
    "get_ports":"/get-ports",
    "open_ports":"/open-ports",
    "disable_ports":"/disable-ports",
    "get_alarms":"/get-alarms",
    "add_alarms":"/add-alarms",
    "empty_alarms":"/empty-alarms",
    "ms_health_check":"/ms-health-check",
    "populate":"/populate",
    "get_creds":"/get-creds",
    "get_acls":"/get-acls",
    "create_acls":"/create-acls",
}
olt_devices = {"1": "181.232.180.7", "2": "181.232.180.5", "3": "181.232.180.6"}
rtr_devices = {
    "E1": "181.232.180.1",
    "E2": "181.232.180.2",
    "A1": "181.232.180.3",
    "A2": "181.232.180.4",
}
rtrs = ["A1", "A2", "E1", "E2"]
olts = ["1", "2", "3"]
client_place_holder = {
    "fail": None,
    "name_1": None,
    "name_2": None,
    "contract": None,
    "olt": None,
    "frame": None,
    "slot": None,
    "port": None,
    "onu_id": None,
    "fsp": None,
    "fspi": None,
    "sn": None,
    "last_down_cause": None,
    "state": None,
    "status": None,
    "type": None,
    "vendor": None,
    "ip_address": None,
    "plan_name": None,
    "spid": None,
    "vlan": None,
    "plan": None,
    "provider": None,
    "plan_name": None,
    "temp": None,
    "pwr": None,
    "line_profile": None,
    "srv_profile": None,
    "device": None,
    "wan": [{"vlan": None, "spid": None, "plan_name": None, "provider": None}],
}

client_payload = {
    "frame": None,
    "slot": None,
    "port": None,
    "onu_id": None,
    "olt": None,
    "fsp": None,
    "fspi": None,
    "name_1": None,
    "name_2": None,
    "contract": None,
    "status": None,
    "state": None,
    "sn": None,
    "device": None,
    "plan_name": None,
    "spid": None,
}


ont_type_start = "Equipment-ID             : "
ont_type_end = "Main Software Version"
ont_type_equipment_id = "Equipment-ID             : "

change_types = ["CT", "CP", "CO"]
