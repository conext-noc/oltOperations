conditionSpidOnt = "CTRL_C to break"
condition = "-----------------------------------------------------------------------------"
spidHeader = "SPID,ID,ATT,PORT_TYPE,F/S,/P,VPI,VCI,FLOW_TYPE,FLOW_PARA,RX,TX,STATE,"
conditionSPID = """Next valid free service virtual port ID: """
spidCheck = {
    "index": "Index               : ",
    "id": "VLAN ID             : ",
    "attr": "VLAN attr           : ",
    "endAttr": "Port type",
    "plan": "Outbound table name : ",
    "adminStatus": "Admin status        : ",
    "status": "State               : ",
    "endStatus": "Label               :",
}

planX2Maps = {
    "7": "OZ_FAMILY",
    "8": "FTTH_INTERNET_10Mbps",
    "9": "FTTH_INTERNET_15",
    "15": "FTTH_INTERNET_30Mbps",
    "16": "FTTH_INTERNET_5Mbps",
    "18": "FTTH_UNLIMITED",
    "19": "FTTH_VOIP",
    "30": "FTTH_INTERNET_MAX",
    "32": "OZ_MAGICAL",
    "33": "OZ_NEXT",
    "34": "OZ_LIFT",
    "36": "OZ_UP",
    "44": "OZ_EMPRENDE",
    "45": "OZ_INICIATE",
    "46": "OZ_CONECTA",
    "47": "OZ_SKY",
    "48": "OZ_MAX",
    "49": "OZ_PLUS",
    "50": "DEDICADO 10 Mbps",
}
planX15NMaps = {
    "210": "OZ_0_2",
    "211": "OZ_PLUS_2",
    "212": "OZ_MAX_2",
    "213": "OZ_NEXT_2",
    "214": "OZ_MAGICAL_2",
    "215": "OZ_SKY_2",
    "310": "OZ_0_IP",
    "311": "OZ_PLUS_IP",
    "312": "OZ_MAX_IP",
    "313": "OZ_NEXT_IP",
    "314": "OZ_MAGICAL_IP",
    "315": "OZ_SKY_IP",
}
planX15Maps = {
    "6": "OZ_LIFT",
    "7": "OZ_FAMILY",
    "9": "FTTH_VOIP",
    "15": "UNLIMITED",
    "16": "FTTH_INTERNET_10Mbps",
    "20": "FTTH_INTERNET_5Mbps",
    "23": "FTTH_INTERNET_15",
    "25": "FTTH_INTERNET_30Mbps",
    "39": "OZ_MAGICAL",
    "40": "OZ_NEXT",
    "41": "OZ EMPRENDE",
    "42": "OZ_EMPRENDE",
    "43": "OZ_INICIATE",
    "44": "OZ_CONECTA",
    "45": "OZ_SKY",
    "46": "OZ_MAX",
    "47": "OZ_PLUS",
    "48": "DEDICADO 10 Mbps",
    "49": "OZ_UP",
}

PLANS = {
    "1": {
        "OZ_0_1": {
            "line_profile": 3,
            "srv_profile": 110,
            "vlan": 1100,
            "provider": "INTER",
            "plan": 110,
            "gem_port": 10
        },
        "OZ_PLUS_1": {
            "line_profile": 17,
            "srv_profile": 111,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 111,
            "gem_port": 11
        },
        "OZ_MAX_1": {
            "line_profile": 27,
            "srv_profile": 112,
            "vlan": 1102,
            "provider": "INTER",
            "plan": 112,
            "gem_port": 12
        },
        "OZ_NEXT_1": {
            "line_profile": 37,
            "srv_profile": 113,
            "vlan": 1103,
            "provider": "INTER",
            "plan": 113,
            "gem_port": 13
        },
        "OZ_MAGICAL_1": {
            "line_profile": 47,
            "srv_profile": 114,
            "vlan": 1104,
            "provider": "INTER",
            "plan": 114,
            "gem_port": 14
        },
        "OZ_SKY_1": {
            "line_profile": 57,
            "srv_profile": 115,
            "vlan": 1105,
            "provider": "INTER",
            "plan": 115,
            "gem_port": 15
        },
        "OZ_0_2": {
            "line_profile": 3,
            "srv_profile": 210,
            "vlan": 2100,
            "provider": "VNET",
            "plan": 210,
            "gem_port": 1
        },
        "OZ_PLUS_2": {
            "line_profile": 17,
            "srv_profile": 211,
            "vlan": 2101,
            "provider": "VNET",
            "plan": 211,
            "gem_port": 21
        },
        "OZ_MAX_2": {
            "line_profile": 27,
            "srv_profile": 212,
            "vlan": 2102,
            "provider": "VNET",
            "plan": 212,
            "gem_port": 22
        },
        "OZ_NEXT_2": {
            "line_profile": 37,
            "srv_profile": 213,
            "vlan": 2103,
            "provider": "VNET",
            "plan": 213,
            "gem_port": 23
        },
        "OZ_MAGICAL_2": {
            "line_profile": 47,
            "srv_profile": 214,
            "vlan": 2104,
            "provider": "VNET",
            "plan": 214,
            "gem_port": 24
        },
        "OZ_SKY_2": {
            "line_profile": 57,
            "srv_profile": 215,
            "vlan": 2105,
            "provider": "VNET",
            "plan": 215,
            "gem_port": 25
        },
        "OZ_PLUS_IP": {
            "line_profile": 18,
            "srv_profile": 311,
            "vlan": 102,
            "provider": "PUBLICAS",
            "plan": 311,
            "gem_port": 14
        },
        "OZ_MAX_IP": {
            "line_profile": 28,
            "srv_profile": 312,
            "vlan": 102,
            "provider": "PUBLICAS",
            "plan": 312,
            "gem_port": 14
        },
        "OZ_NEXT_IP": {
            "line_profile": 38,
            "srv_profile": 313,
            "vlan": 102,
            "provider": "PUBLICAS",
            "plan": 313,
            "gem_port": 14
        },
        "OZ_MAGICAL_IP": {
            "line_profile": 48,
            "srv_profile": 314,
            "vlan": 102,
            "provider": "PUBLICAS",
            "plan": 314,
            "gem_port": 14
        },
        "OZ_SKY_IP": {
            "line_profile": 58,
            "srv_profile": 315,
            "vlan": 102,
            "provider": "PUBLICAS",
            "plan": 315,
            "gem_port": 14
        },
    },
    "2": {
        "OZ_PLUS_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 47,
            "gem_port": 14
        },
        "OZ_MAX_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 46,
            "gem_port": 14
        },
        "OZ_NEXT_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 40,
            "gem_port": 14
        },
        "OZ_MAGICAL_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 39,
            "gem_port": 14
        },
        "OZ_SKY_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 45,
            "gem_port": 14
        },
        "OZ_START_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 23,
            "gem_port": 14
        },
        "OZ_FAMILY_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 25,
            "gem_port": 14
        },
        "OZ_EMPRENDE_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 42,
            "gem_port": 14
        },
        "OZ_CONECTA_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 44,
            "gem_port": 14
        },
        "OZ_INICIATE_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 43,
            "gem_port": 14
        },
        "OZ_LIFT_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 6,
            "gem_port": 14
        },
        "OZ_UP_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 49,
            "gem_port": 14
        },
        "OZ_PLUS_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 47,
            "gem_port": 14
        },
        "OZ_MAX_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 46,
            "gem_port": 14
        },
        "OZ_NEXT_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 40,
            "gem_port": 14
        },
        "OZ_MAGICAL_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 39,
            "gem_port": 14
        },
        "OZ_SKY_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 45,
            "gem_port": 14
        },
        "OZ_START_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 23,
            "gem_port": 14
        },
        "OZ_FAMILY_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 25,
            "gem_port": 14
        },
        "OZ_EMPRENDE_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 42,
            "gem_port": 14
        },
        "OZ_CONECTA_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 44,
            "gem_port": 14
        },
        "OZ_INICIATE_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 43,
            "gem_port": 14
        },
        "OZ_LIFT_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 6,
            "gem_port": 14
        },
        "OZ_UP_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 49,
            "gem_port": 14
        },
        "OZ_PLUS_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 47,
            "gem_port": 14
        },
        "OZ_MAX_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 46,
            "gem_port": 14
        },
        "OZ_NEXT_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 40,
            "gem_port": 14
        },
        "OZ_MAGICAL_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 39,
            "gem_port": 14
        },
        "OZ_SKY_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 45,
            "gem_port": 14
        },
        "OZ_START_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 23,
            "gem_port": 14
        },
        "OZ_FAMILY_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 25,
            "gem_port": 14
        },
        "OZ_EMPRENDE_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 42,
            "gem_port": 14
        },
        "OZ_CONECTA_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 44,
            "gem_port": 14
        },
        "OZ_INICIATE_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 43,
            "gem_port": 14
        },
        "OZ_LIFT_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 6,
            "gem_port": 14
        },
        "OZ_UP_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 49,
            "gem_port": 14
        },
    },
    "3": {
        "OZ_PLUS_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 49,
            "gem_port": 14
        },
        "OZ_MAX_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 48,
            "gem_port": 14
        },
        "OZ_NEXT_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 33,
            "gem_port": 14
        },
        "OZ_MAGICAL_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 32,
            "gem_port": 14
        },
        "OZ_SKY_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 47,
            "gem_port": 14
        },
        "OZ_START_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 9,
            "gem_port": 14
        },
        "OZ_FAMILY_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 15,
            "gem_port": 14
        },
        "OZ_EMPRENDE_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 44,
            "gem_port": 14
        },
        "OZ_CONECTA_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 46,
            "gem_port": 14
        },
        "OZ_INICIATE_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 45,
            "gem_port": 14
        },
        "OZ_LIFT_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 34,
            "gem_port": 14
        },
        "OZ_UP_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 36,
            "gem_port": 14
        },
        "OZ_PLUS_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 49,
            "gem_port": 14
        },
        "OZ_MAX_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 48,
            "gem_port": 14
        },
        "OZ_NEXT_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 33,
            "gem_port": 14
        },
        "OZ_MAGICAL_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 32,
            "gem_port": 14
        },
        "OZ_SKY_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 47,
            "gem_port": 14
        },
        "OZ_START_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 9,
            "gem_port": 14
        },
        "OZ_FAMILY_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 15,
            "gem_port": 14
        },
        "OZ_EMPRENDE_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 44,
            "gem_port": 14
        },
        "OZ_CONECTA_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 46,
            "gem_port": 14
        },
        "OZ_INICIATE_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 45,
            "gem_port": 14
        },
        "OZ_LIFT_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 34,
            "gem_port": 14
        },
        "OZ_UP_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 36,
            "gem_port": 14
        },
        "OZ_PLUS_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 49,
            "gem_port": 14
        },
        "OZ_MAX_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 48,
            "gem_port": 14
        },
        "OZ_NEXT_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 33,
            "gem_port": 14
        },
        "OZ_MAGICAL_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 32,
            "gem_port": 14
        },
        "OZ_SKY_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 47,
            "gem_port": 14
        },
        "OZ_START_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 9,
            "gem_port": 14
        },
        "OZ_FAMILY_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 15,
            "gem_port": 14
        },
        "OZ_EMPRENDE_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 44,
            "gem_port": 14
        },
        "OZ_CONECTA_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 46,
            "gem_port": 14
        },
        "OZ_INICIATE_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 45,
            "gem_port": 14
        },
        "OZ_LIFT_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 34,
            "gem_port": 14
        },
        "OZ_UP_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 36,
            "gem_port": 14
        },
    }
}