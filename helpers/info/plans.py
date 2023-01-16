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

oldPlans = {
    "2": {
        "OZ_PLUS": 47,
        "OZ_MAX": 46,
        "OZ_NEXT": 40,
        "OZ_MAGICAL": 39,
        "OZ_SKY": 45,
        "OZ_UP": 49,
        "OZ_LIFT": 6,
        "OZ_FAMILY": 25,
        "OZ_START": 23,
        "OZ_EMPRENDE": 41,
        "OZ_CONECTA": 43,
        "OZ_INICIATE": 44,
    },
    "3": {
        "OZ_PLUS": 49,
        "OZ_MAX": 48,
        "OZ_NEXT": 40,
        "OZ_MAGICAL": 32,
        "OZ_SKY": 47,
        "OZ_UP": 36,
        "OZ_LIFT": 34,
        "OZ_FAMILY": 15,
        "OZ_START": 9,
        "OZ_EMPRENDE": 44,
        "OZ_CONECTA": 46,
        "OZ_INICIATE": 45,
    }
}

PLANS = {
    "1": {
        "OZ_0_1": {
            "lineProfile": 3,
            "srvProfile": 110,
            "vlan": 1100,
            "provider": "INTER",
            "plan": 110,
            "gemPort": 10
        },
        "OZ_PLUS_1": {
            "lineProfile": 17,
            "srvProfile": 111,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 111,
            "gemPort": 11
        },
        "OZ_MAX_1": {
            "lineProfile": 27,
            "srvProfile": 112,
            "vlan": 1102,
            "provider": "INTER",
            "plan": 112,
            "gemPort": 12
        },
        "OZ_NEXT_1": {
            "lineProfile": 37,
            "srvProfile": 113,
            "vlan": 1103,
            "provider": "INTER",
            "plan": 113,
            "gemPort": 13
        },
        "OZ_MAGICAL_1": {
            "lineProfile": 47,
            "srvProfile": 114,
            "vlan": 1104,
            "provider": "INTER",
            "plan": 114,
            "gemPort": 14
        },
        "OZ_SKY_1": {
            "lineProfile": 57,
            "srvProfile": 115,
            "vlan": 1105,
            "provider": "INTER",
            "plan": 115,
            "gemPort": 15
        },
        "OZ_0_2": {
            "lineProfile": 3,
            "srvProfile": 210,
            "vlan": 2100,
            "provider": "VNET",
            "plan": 210,
            "gemPort": 1
        },
        "OZ_PLUS_2": {
            "lineProfile": 17,
            "srvProfile": 211,
            "vlan": 2101,
            "provider": "VNET",
            "plan": 211,
            "gemPort": 21
        },
        "OZ_MAX_2": {
            "lineProfile": 27,
            "srvProfile": 212,
            "vlan": 2102,
            "provider": "VNET",
            "plan": 212,
            "gemPort": 22
        },
        "OZ_NEXT_2": {
            "lineProfile": 37,
            "srvProfile": 213,
            "vlan": 2103,
            "provider": "VNET",
            "plan": 213,
            "gemPort": 23
        },
        "OZ_MAGICAL_2": {
            "lineProfile": 47,
            "srvProfile": 214,
            "vlan": 2104,
            "provider": "VNET",
            "plan": 214,
            "gemPort": 24
        },
        "OZ_SKY_2": {
            "lineProfile": 57,
            "srvProfile": 215,
            "vlan": 2105,
            "provider": "VNET",
            "plan": 215,
            "gemPort": 25
        },
        "OZ_PLUS_IP": {
            "lineProfile": 18,
            "srvProfile": 311,
            "vlan": 102,
            "provider": "PUBLICAS",
            "plan": 311,
            "gemPort": 14
        },
        "OZ_MAX_IP": {
            "lineProfile": 28,
            "srvProfile": 312,
            "vlan": 102,
            "provider": "PUBLICAS",
            "plan": 312,
            "gemPort": 14
        },
        "OZ_NEXT_IP": {
            "lineProfile": 38,
            "srvProfile": 313,
            "vlan": 102,
            "provider": "PUBLICAS",
            "plan": 313,
            "gemPort": 14
        },
        "OZ_MAGICAL_IP": {
            "lineProfile": 48,
            "srvProfile": 314,
            "vlan": 102,
            "provider": "PUBLICAS",
            "plan": 314,
            "gemPort": 14
        },
        "OZ_SKY_IP": {
            "lineProfile": 58,
            "srvProfile": 315,
            "vlan": 102,
            "provider": "PUBLICAS",
            "plan": 315,
            "gemPort": 14
        },
    },
    "2": {
        "OZ_PLUS_1": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 47,
            "gemPort": 14
        },
        "OZ_MAX_1": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 46,
            "gemPort": 14
        },
        "OZ_NEXT_1": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 40,
            "gemPort": 14
        },
        "OZ_MAGICAL_1": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 39,
            "gemPort": 14
        },
        "OZ_SKY_1": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 45,
            "gemPort": 14
        },
        "OZ_START_1": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 23,
            "gemPort": 14
        },
        "OZ_FAMILY_1": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 25,
            "gemPort": 14
        },
        "OZ_EMPRENDE_1": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 42,
            "gemPort": 14
        },
        "OZ_CONECTA_1": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 44,
            "gemPort": 14
        },
        "OZ_INICIATE_1": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 43,
            "gemPort": 14
        },
        "OZ_LIFT_1": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 6,
            "gemPort": 14
        },
        "OZ_UP_1": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 49,
            "gemPort": 14
        },
        "OZ_PLUS_2": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 47,
            "gemPort": 14
        },
        "OZ_MAX_2": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 46,
            "gemPort": 14
        },
        "OZ_NEXT_2": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 40,
            "gemPort": 14
        },
        "OZ_MAGICAL_2": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 39,
            "gemPort": 14
        },
        "OZ_SKY_2": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 45,
            "gemPort": 14
        },
        "OZ_START_2": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 23,
            "gemPort": 14
        },
        "OZ_FAMILY_2": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 25,
            "gemPort": 14
        },
        "OZ_EMPRENDE_2": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 42,
            "gemPort": 14
        },
        "OZ_CONECTA_2": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 44,
            "gemPort": 14
        },
        "OZ_INICIATE_2": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 43,
            "gemPort": 14
        },
        "OZ_LIFT_2": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 6,
            "gemPort": 14
        },
        "OZ_UP_2": {
            "lineProfile": 2,
            "srvProfile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 49,
            "gemPort": 14
        },
        "OZ_PLUS_IP": {
            "lineProfile": 4,
            "srvProfile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 47,
            "gemPort": 14
        },
        "OZ_MAX_IP": {
            "lineProfile": 4,
            "srvProfile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 46,
            "gemPort": 14
        },
        "OZ_NEXT_IP": {
            "lineProfile": 4,
            "srvProfile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 40,
            "gemPort": 14
        },
        "OZ_MAGICAL_IP": {
            "lineProfile": 4,
            "srvProfile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 39,
            "gemPort": 14
        },
        "OZ_SKY_IP": {
            "lineProfile": 4,
            "srvProfile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 45,
            "gemPort": 14
        },
        "OZ_START_IP": {
            "lineProfile": 4,
            "srvProfile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 23,
            "gemPort": 14
        },
        "OZ_FAMILY_IP": {
            "lineProfile": 4,
            "srvProfile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 25,
            "gemPort": 14
        },
        "OZ_EMPRENDE_IP": {
            "lineProfile": 4,
            "srvProfile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 42,
            "gemPort": 14
        },
        "OZ_CONECTA_IP": {
            "lineProfile": 4,
            "srvProfile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 44,
            "gemPort": 14
        },
        "OZ_INICIATE_IP": {
            "lineProfile": 4,
            "srvProfile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 43,
            "gemPort": 14
        },
        "OZ_LIFT_IP": {
            "lineProfile": 4,
            "srvProfile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 6,
            "gemPort": 14
        },
        "OZ_UP_IP": {
            "lineProfile": 4,
            "srvProfile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 49,
            "gemPort": 14
        },
    },
    "3": {
        "OZ_PLUS_1": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 49,
            "gemPort": 14
        },
        "OZ_MAX_1": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 48,
            "gemPort": 14
        },
        "OZ_NEXT_1": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 33,
            "gemPort": 14
        },
        "OZ_MAGICAL_1": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 32,
            "gemPort": 14
        },
        "OZ_SKY_1": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 47,
            "gemPort": 14
        },
        "OZ_START_1": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 9,
            "gemPort": 14
        },
        "OZ_FAMILY_1": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 15,
            "gemPort": 14
        },
        "OZ_EMPRENDE_1": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 44,
            "gemPort": 14
        },
        "OZ_CONECTA_1": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 46,
            "gemPort": 14
        },
        "OZ_INICIATE_1": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 45,
            "gemPort": 14
        },
        "OZ_LIFT_1": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 34,
            "gemPort": 14
        },
        "OZ_UP_1": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "plan": 36,
            "gemPort": 14
        },
        "OZ_PLUS_2": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 49,
            "gemPort": 14
        },
        "OZ_MAX_2": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 48,
            "gemPort": 14
        },
        "OZ_NEXT_2": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 33,
            "gemPort": 14
        },
        "OZ_MAGICAL_2": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 32,
            "gemPort": 14
        },
        "OZ_SKY_2": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 47,
            "gemPort": 14
        },
        "OZ_START_2": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 9,
            "gemPort": 14
        },
        "OZ_FAMILY_2": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 15,
            "gemPort": 14
        },
        "OZ_EMPRENDE_2": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 44,
            "gemPort": 14
        },
        "OZ_CONECTA_2": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 46,
            "gemPort": 14
        },
        "OZ_INICIATE_2": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 45,
            "gemPort": 14
        },
        "OZ_LIFT_2": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 34,
            "gemPort": 14
        },
        "OZ_UP_2": {
            "lineProfile": 2,
            "srvProfile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "plan": 36,
            "gemPort": 14
        },
        "OZ_PLUS_IP": {
            "lineProfile": 5,
            "srvProfile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 49,
            "gemPort": 14
        },
        "OZ_MAX_IP": {
            "lineProfile": 5,
            "srvProfile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 48,
            "gemPort": 14
        },
        "OZ_NEXT_IP": {
            "lineProfile": 5,
            "srvProfile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 33,
            "gemPort": 14
        },
        "OZ_MAGICAL_IP": {
            "lineProfile": 5,
            "srvProfile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 32,
            "gemPort": 14
        },
        "OZ_SKY_IP": {
            "lineProfile": 5,
            "srvProfile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 47,
            "gemPort": 14
        },
        "OZ_START_IP": {
            "lineProfile": 5,
            "srvProfile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 9,
            "gemPort": 14
        },
        "OZ_FAMILY_IP": {
            "lineProfile": 5,
            "srvProfile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 15,
            "gemPort": 14
        },
        "OZ_EMPRENDE_IP": {
            "lineProfile": 5,
            "srvProfile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 44,
            "gemPort": 14
        },
        "OZ_CONECTA_IP": {
            "lineProfile": 5,
            "srvProfile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 46,
            "gemPort": 14
        },
        "OZ_INICIATE_IP": {
            "lineProfile": 5,
            "srvProfile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 45,
            "gemPort": 14
        },
        "OZ_LIFT_IP": {
            "lineProfile": 5,
            "srvProfile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 34,
            "gemPort": 14
        },
        "OZ_UP_IP": {
            "lineProfile": 5,
            "srvProfile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "plan": 36,
            "gemPort": 14
        },
    }
}

plans = {
    "OZ_0_1": {
        "lineProfile": 3,
        "srvProfile": 110,
        "vlan": 1100,
        "provider": "INTER",
        "plan": 110,
        "gemPort": 10
    },
    "OZ_PLUS_1": {
        "lineProfile": 17,
        "srvProfile": 111,
        "vlan": 1101,
        "provider": "INTER",
        "plan": 111,
        "gemPort": 11
    },
    "OZ_MAX_1": {
        "lineProfile": 27,
        "srvProfile": 112,
        "vlan": 1102,
        "provider": "INTER",
        "plan": 112,
        "gemPort": 12
    },
    "OZ_NEXT_1": {
        "lineProfile": 37,
        "srvProfile": 113,
        "vlan": 1103,
        "provider": "INTER",
        "plan": 113,
        "gemPort": 13
    },
    "OZ_MAGICAL_1": {
        "lineProfile": 47,
        "srvProfile": 114,
        "vlan": 1104,
        "provider": "INTER",
        "plan": 114,
        "gemPort": 14
    },
    "OZ_SKY_1": {
        "lineProfile": 57,
        "srvProfile": 115,
        "vlan": 1105,
        "provider": "INTER",
        "plan": 115,
        "gemPort": 15
    },
    "OZ_0_2": {
        "lineProfile": 3,
        "srvProfile": 210,
        "vlan": 2100,
        "provider": "VNET",
        "plan": 210,
        "gemPort": 1
    },
    "OZ_PLUS_2": {
        "lineProfile": 17,
        "srvProfile": 211,
        "vlan": 2101,
        "provider": "VNET",
        "plan": 211,
        "gemPort": 21
    },
    "OZ_MAX_2": {
        "lineProfile": 27,
        "srvProfile": 212,
        "vlan": 2102,
        "provider": "VNET",
        "plan": 212,
        "gemPort": 22
    },
    "OZ_NEXT_2": {
        "lineProfile": 37,
        "srvProfile": 213,
        "vlan": 2103,
        "provider": "VNET",
        "plan": 213,
        "gemPort": 23
    },
    "OZ_MAGICAL_2": {
        "lineProfile": 47,
        "srvProfile": 214,
        "vlan": 2104,
        "provider": "VNET",
        "plan": 214,
        "gemPort": 24
    },
    "OZ_SKY_2": {
        "lineProfile": 57,
        "srvProfile": 215,
        "vlan": 2105,
        "provider": "VNET",
        "plan": 215,
        "gemPort": 25
    },
    "OZ_PLUS_IP": {
        "lineProfile": 18,
        "srvProfile": 311,
        "vlan": 102,
        "provider": "PUBLICAS",
        "plan": 311,
        "gemPort": 14
    },
    "OZ_MAX_IP": {
        "lineProfile": 28,
        "srvProfile": 312,
        "vlan": 102,
        "provider": "PUBLICAS",
        "plan": 312,
        "gemPort": 14
    },
    "OZ_NEXT_IP": {
        "lineProfile": 38,
        "srvProfile": 313,
        "vlan": 102,
        "provider": "PUBLICAS",
        "plan": 313,
        "gemPort": 14
    },
    "OZ_MAGICAL_IP": {
        "lineProfile": 48,
        "srvProfile": 314,
        "vlan": 102,
        "provider": "PUBLICAS",
        "plan": 314,
        "gemPort": 14
    },
    "OZ_SKY_IP": {
        "lineProfile": 58,
        "srvProfile": 315,
        "vlan": 102,
        "provider": "PUBLICAS",
        "plan": 315,
        "gemPort": 14
    },
}
