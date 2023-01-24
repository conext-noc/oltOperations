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
            "srv_profile": 210,
            "vlan": 3100,
            "provider": "INTER",
            "name": "OZ_0",
            "plan": 210,
            "gem_port": 20
        },
        "OZ_PLUS_1": {
            "line_profile": 17,
            "srv_profile": 211,
            "vlan": 3101,
            "name": "OZ_PLUS",
            "provider": "INTER",
            "plan": 211,
            "gem_port": 21
        },
        "OZ_MAX_1": {
            "line_profile": 27,
            "srv_profile": 212,
            "vlan": 3102,
            "name": "OZ_MAX",
            "provider": "INTER",
            "plan": 212,
            "gem_port": 22
        },
        "OZ_NEXT_1": {
            "line_profile": 37,
            "srv_profile": 213,
            "vlan": 3103,
            "name": "OZ_NEXT",
            "provider": "INTER",
            "plan": 213,
            "gem_port": 23
        },
        "OZ_MAGICAL_1": {
            "line_profile": 47,
            "srv_profile": 214,
            "vlan": 3104,
            "name": "OZ_MAGICAL",
            "provider": "INTER",
            "plan": 214,
            "gem_port": 24
        },
        "OZ_SKY_1": {
            "line_profile": 57,
            "srv_profile": 215,
            "vlan": 3105,
            "name": "OZ_SKY",
            "provider": "INTER",
            "plan": 215,
            "gem_port": 25
        },
        "OZ_0_2": {
            "line_profile": 3,
            "srv_profile": 210,
            "vlan": 2100,
            "provider": "VNET",
            "name": "OZ_0",
            "plan": 210,
            "gem_port": 20
        },
        "OZ_PLUS_2": {
            "line_profile": 17,
            "srv_profile": 211,
            "vlan": 2101,
            "name": "OZ_PLUS",
            "provider": "VNET",
            "plan": 211,
            "gem_port": 21
        },
        "OZ_MAX_2": {
            "line_profile": 27,
            "srv_profile": 212,
            "vlan": 2102,
            "name": "OZ_MAX",
            "provider": "VNET",
            "plan": 212,
            "gem_port": 22
        },
        "OZ_NEXT_2": {
            "line_profile": 37,
            "srv_profile": 213,
            "vlan": 2103,
            "name": "OZ_NEXT",
            "provider": "VNET",
            "plan": 213,
            "gem_port": 23
        },
        "OZ_MAGICAL_2": {
            "line_profile": 47,
            "srv_profile": 214,
            "vlan": 2104,
            "name": "OZ_MAGICAL",
            "provider": "VNET",
            "plan": 214,
            "gem_port": 24
        },
        "OZ_SKY_2": {
            "line_profile": 57,
            "srv_profile": 215,
            "vlan": 2105,
            "name": "OZ_SKY",
            "provider": "VNET",
            "plan": 215,
            "gem_port": 25
        },
        "OZ_PLUS_IP": {
            "line_profile": 18,
            "srv_profile": 311,
            "vlan": 102,
            "provider": "PUBLICAS",
            "name": "OZ_PLUS",
            "plan": 311,
            "gem_port": 14
        },
        "OZ_MAX_IP": {
            "line_profile": 28,
            "srv_profile": 312,
            "vlan": 102,
            "provider": "PUBLICAS",
            "name": "OZ_MAX",
            "plan": 312,
            "gem_port": 14
        },
        "OZ_NEXT_IP": {
            "line_profile": 38,
            "srv_profile": 313,
            "vlan": 102,
            "provider": "PUBLICAS",
            "name": "OZ_NEXT",
            "plan": 313,
            "gem_port": 14
        },
        "OZ_MAGICAL_IP": {
            "line_profile": 48,
            "srv_profile": 314,
            "vlan": 102,
            "provider": "PUBLICAS",
            "name": "OZ_MAGICAL",
            "plan": 314,
            "gem_port": 14
        },
        "OZ_SKY_IP": {
            "line_profile": 58,
            "srv_profile": 315,
            "vlan": 102,
            "provider": "PUBLICAS",
            "name": "OZ_SKY",
            "plan": 315,
            "gem_port": 14
        },
    },
    "2": {
        "OZ_PLUS_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "name": "OZ_PLUS",
            "provider": "INTER",
            "plan": 47,
            "gem_port": 14
        },
        "OZ_MAX_1": {
            "line_profile": 2,
            "srv_pro,file": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_MAX",
            "plan": 46,
            "gem_port": 14
        },
        "OZ_NEXT_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_NEXT",
            "plan": 40,
            "gem_port": 14
        },
        "OZ_MAGICAL_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_MAGICAL",
            "plan": 39,
            "gem_port": 14
        },
        "OZ_SKY_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_SKY",
            "plan": 45,
            "gem_port": 14
        },
        "OZ_START_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_START",
            "plan": 23,
            "gem_port": 14
        },
        "OZ_FAMILY_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_FAMILY",
            "plan": 25,
            "gem_port": 14
        },
        "OZ_EMPRENDE_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_EMPRENDE",
            "plan": 42,
            "gem_port": 14
        },
        "OZ_CONECTA_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_CONECTA",
            "plan": 44,
            "gem_port": 14
        },
        "OZ_INICIATE_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_INICIATE",
            "plan": 43,
            "gem_port": 14
        },
        "OZ_LIFT_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_LIFT",
            "plan": 6,
            "gem_port": 14
        },
        "OZ_UP_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_UP",
            "plan": 49,
            "gem_port": 14
        },
        "OZ_PLUS_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_PLUS",
            "plan": 47,
            "gem_port": 14
        },
        "OZ_MAX_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_MAX",
            "plan": 46,
            "gem_port": 14
        },
        "OZ_NEXT_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_NEXT",
            "plan": 40,
            "gem_port": 14
        },
        "OZ_MAGICAL_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_MAGICAL",
            "plan": 39,
            "gem_port": 14
        },
        "OZ_SKY_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_SKY",
            "plan": 45,
            "gem_port": 14
        },
        "OZ_START_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_START",
            "plan": 23,
            "gem_port": 14
        },
        "OZ_FAMILY_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_FAMILY",
            "plan": 25,
            "gem_port": 14
        },
        "OZ_EMPRENDE_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_EMPRENDE",
            "plan": 42,
            "gem_port": 14
        },
        "OZ_CONECTA_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_CONECTA",
            "plan": 44,
            "gem_port": 14
        },
        "OZ_INICIATE_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_INICIATE",
            "plan": 43,
            "gem_port": 14
        },
        "OZ_LIFT_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_LIFT",
            "plan": 6,
            "gem_port": 14
        },
        "OZ_UP_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_UP",
            "plan": 49,
            "gem_port": 14
        },
        "OZ_PLUS_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_PLUS",
            "plan": 47,
            "gem_port": 14
        },
        "OZ_MAX_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_MAX",
            "plan": 46,
            "gem_port": 14
        },
        "OZ_NEXT_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_NEXT",
            "plan": 40,
            "gem_port": 14
        },
        "OZ_MAGICAL_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_MAGICAL",
            "plan": 39,
            "gem_port": 14
        },
        "OZ_SKY_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_SKY",
            "plan": 45,
            "gem_port": 14
        },
        "OZ_START_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_START",
            "plan": 23,
            "gem_port": 14
        },
        "OZ_FAMILY_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_FAMILY",
            "plan": 25,
            "gem_port": 14
        },
        "OZ_EMPRENDE_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_EMPRENDE",
            "plan": 42,
            "gem_port": 14
        },
        "OZ_CONECTA_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_CONECTA",
            "plan": 44,
            "gem_port": 14
        },
        "OZ_INICIATE_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_INICIATE",
            "plan": 43,
            "gem_port": 14
        },
        "OZ_LIFT_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_LIFT",
            "plan": 6,
            "gem_port": 14
        },
        "OZ_UP_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_UP",
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
            "name": "OZ_PLUS",
            "plan": 49,
            "gem_port": 14
        },
        "OZ_MAX_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_MAX",
            "plan": 48,
            "gem_port": 14
        },
        "OZ_NEXT_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_NEXT",
            "plan": 33,
            "gem_port": 14
        },
        "OZ_MAGICAL_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_MAGICAL",
            "plan": 32,
            "gem_port": 14
        },
        "OZ_SKY_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_SKY",
            "plan": 47,
            "gem_port": 14
        },
        "OZ_START_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_START",
            "plan": 9,
            "gem_port": 14
        },
        "OZ_FAMILY_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_FAMILY",
            "plan": 15,
            "gem_port": 14
        },
        "OZ_EMPRENDE_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_EMPRENDE",
            "plan": 44,
            "gem_port": 14
        },
        "OZ_CONECTA_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_CONECTA",
            "plan": 46,
            "gem_port": 14
        },
        "OZ_INICIATE_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_INICIATE",
            "plan": 45,
            "gem_port": 14
        },
        "OZ_LIFT_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_LIFT",
            "plan": 34,
            "gem_port": 14
        },
        "OZ_UP_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_UP",
            "plan": 36,
            "gem_port": 14
        },
        "OZ_PLUS_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_PLUS",
            "plan": 49,
            "gem_port": 14
        },
        "OZ_MAX_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_MAX",
            "plan": 48,
            "gem_port": 14
        },
        "OZ_NEXT_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_NEXT",
            "plan": 33,
            "gem_port": 14
        },
        "OZ_MAGICAL_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_MAGICAL",
            "plan": 32,
            "gem_port": 14
        },
        "OZ_SKY_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_SKY",
            "plan": 47,
            "gem_port": 14
        },
        "OZ_START_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_START",
            "plan": 9,
            "gem_port": 14
        },
        "OZ_FAMILY_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_FAMILY",
            "plan": 15,
            "gem_port": 14
        },
        "OZ_EMPRENDE_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_EMPRENDE",
            "plan": 44,
            "gem_port": 14
        },
        "OZ_CONECTA_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_CONECTA",
            "plan": 46,
            "gem_port": 14
        },
        "OZ_INICIATE_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_INICIATE",
            "plan": 45,
            "gem_port": 14
        },
        "OZ_LIFT_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_LIFT",
            "plan": 34,
            "gem_port": 14
        },
        "OZ_UP_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_UP",
            "plan": 36,
            "gem_port": 14
        },
        "OZ_PLUS_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_PLUS",
            "plan": 49,
            "gem_port": 14
        },
        "OZ_MAX_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_MAX",
            "plan": 48,
            "gem_port": 14
        },
        "OZ_NEXT_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_NEXT",
            "plan": 33,
            "gem_port": 14
        },
        "OZ_MAGICAL_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_MAGICAL",
            "plan": 32,
            "gem_port": 14
        },
        "OZ_SKY_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_SKY",
            "plan": 47,
            "gem_port": 14
        },
        "OZ_START_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_START",
            "plan": 9,
            "gem_port": 14
        },
        "OZ_FAMILY_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_FAMILY",
            "plan": 15,
            "gem_port": 14
        },
        "OZ_EMPRENDE_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_EMPRENDE",
            "plan": 44,
            "gem_port": 14
        },
        "OZ_CONECTA_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_CONECTA",
            "plan": 46,
            "gem_port": 14
        },
        "OZ_INICIATE_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_INICIATE",
            "plan": 45,
            "gem_port": 14
        },
        "OZ_LIFT_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_LIFT",
            "plan": 34,
            "gem_port": 14
        },
        "OZ_UP_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_UP",
            "plan": 36,
            "gem_port": 14
        },
    }
}
