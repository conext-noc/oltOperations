clientData = {
    "fail": None,
    "name": None,
    "olt": None,
    "frame": None,
    "slot": None,
    "port": None,
    "onu_id": None,
    "sn": None,
    "last_down_cause": None,
    "state": None,
    "status": None,
    "type": None,
    "ip_address": None,
    "plan_name": None,
    "wan": [{"spid": None, "vlan": None, "plan": None, "provider": None, "plan_name": None, "state": None}],
    "temp": None,
    "pwr": None,
    "line_profile": None,
    "srv_profile": None,
    "device": None,
}

providerMap = {"1101": "INTER", "1102": "VNET",
               "1104": "IP PUBLICAS", "101": "VOIP"}

devices = {
    "OLT1": "181.232.180.7",
    "OLT2": "181.232.180.5",
    "OLT3": "181.232.180.6",
    "RTRE1": {"ip": "181.232.180.1", "ints": ["GigabitEthernet0/3/7(10G)"]},
    "RTRE2": {"ip": "181.232.180.2", "ints": ["GigabitEthernet0/3/7(10G)", "GigabitEthernet0/3/8(10G)"]},
    "RTRA1": {"ip": "181.232.180.3", "pool": "1", "section": {
        "1": {"start": 4, "end": 5},
        "2": {"start": 7, "end": 8},
    }},
    "RTRA2": {"ip": "181.232.180.4", "pool": "2", "section": {
        "1": {"start": 4, "end": 5},
        "2": {"start": 7, "end": 8},
    }},
}
