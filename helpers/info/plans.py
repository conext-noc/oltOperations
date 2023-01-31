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
    "8": "OZ_DEDICADO-10",
    "9": "OZ_START",
    "15": "OZ_FAMILY",
    "16": "OZ_DEDICADO-5",
    "18": "UNLIMITED",
    "19": "OZ_VOIP",
    "30": "OZ_MAX",
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
    "50": "OZ_DEDICADO-10-2",
}
planX15NMaps = {
    "210": "OZ_0",
    "211": "OZ_PLUS",
    "212": "OZ_MAX",
    "213": "OZ_NEXT",
    "214": "OZ_MAGICAL",
    "215": "OZ_SKY",
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
    "9": "OZ_VOIP",
    "11": "OZ_DEDICADO_150",
    "15": "UNLIMITED",
    "16": "OZ_DEDICADO-10",
    "20": "OZ_DEDICADO-5",
    "23": "OZ_START",
    "25": "OZ_FAMILY",
    "39": "OZ_MAGICAL",
    "40": "OZ_NEXT",
    "41": "OZ EMPRENDE",
    "42": "OZ_EMPRENDE",
    "43": "OZ_INICIATE",
    "44": "OZ_CONECTA",
    "45": "OZ_SKY",
    "46": "OZ_MAX",
    "47": "OZ_PLUS",
    "48": "OZ_DEDICADO-10-2",
    "49": "OZ_UP",
}

PLANS = {
    "1": {
        "OZ_0_1": {
            "line_profile": 3,
            "srv_profile": 210,
            "vlan": 3100,
            "provider": "INTER",
            "name": "OZ_0_1",
            "plan": 210,
            "gem_port": 20
        },
        "OZ_PLUS_1": {
            "line_profile": 17,
            "srv_profile": 211,
            "vlan": 3101,
            "name": "OZ_PLUS_1",
            "provider": "INTER",
            "plan": 211,
            "gem_port": 21
        },
        "OZ_MAX_1": {
            "line_profile": 27,
            "srv_profile": 212,
            "vlan": 3102,
            "name": "OZ_MAX_1",
            "provider": "INTER",
            "plan": 212,
            "gem_port": 22
        },
        "OZ_NEXT_1": {
            "line_profile": 37,
            "srv_profile": 213,
            "vlan": 3103,
            "name": "OZ_NEXT_1",
            "provider": "INTER",
            "plan": 213,
            "gem_port": 23
        },
        "OZ_MAGICAL_1": {
            "line_profile": 47,
            "srv_profile": 214,
            "vlan": 3104,
            "name": "OZ_MAGICAL_1",
            "provider": "INTER",
            "plan": 214,
            "gem_port": 24
        },
        "OZ_SKY_1": {
            "line_profile": 57,
            "srv_profile": 215,
            "vlan": 3105,
            "name": "OZ_SKY_1",
            "provider": "INTER",
            "plan": 215,
            "gem_port": 25
        },
        "OZ_0_2": {
            "line_profile": 3,
            "srv_profile": 210,
            "vlan": 2100,
            "provider": "VNET",
            "name": "OZ_0_2",
            "plan": 210,
            "gem_port": 20
        },
        "OZ_PLUS_2": {
            "line_profile": 17,
            "srv_profile": 211,
            "vlan": 2101,
            "name": "OZ_PLUS_2",
            "provider": "VNET",
            "plan": 211,
            "gem_port": 21
        },
        "OZ_MAX_2": {
            "line_profile": 27,
            "srv_profile": 212,
            "vlan": 2102,
            "name": "OZ_MAX_2",
            "provider": "VNET",
            "plan": 212,
            "gem_port": 22
        },
        "OZ_NEXT_2": {
            "line_profile": 37,
            "srv_profile": 213,
            "vlan": 2103,
            "name": "OZ_NEXT_2",
            "provider": "VNET",
            "plan": 213,
            "gem_port": 23
        },
        "OZ_MAGICAL_2": {
            "line_profile": 47,
            "srv_profile": 214,
            "vlan": 2104,
            "name": "OZ_MAGICAL_2",
            "provider": "VNET",
            "plan": 214,
            "gem_port": 24
        },
        "OZ_SKY_2": {
            "line_profile": 57,
            "srv_profile": 215,
            "vlan": 2105,
            "name": "OZ_SKY_2",
            "provider": "VNET",
            "plan": 215,
            "gem_port": 25
        },
        "OZ_PLUS_IP": {
            "line_profile": 18,
            "srv_profile": 311,
            "vlan": 102,
            "provider": "PUBLICAS",
            "name": "OZ_PLUS_IP",
            "plan": 311,
            "gem_port": 14
        },
        "OZ_MAX_IP": {
            "line_profile": 28,
            "srv_profile": 312,
            "vlan": 102,
            "provider": "PUBLICAS",
            "name": "OZ_MAX_IP",
            "plan": 312,
            "gem_port": 14
        },
        "OZ_NEXT_IP": {
            "line_profile": 38,
            "srv_profile": 313,
            "vlan": 102,
            "provider": "PUBLICAS",
            "name": "OZ_NEXT_IP",
            "plan": 313,
            "gem_port": 14
        },
        "OZ_MAGICAL_IP": {
            "line_profile": 48,
            "srv_profile": 314,
            "vlan": 102,
            "provider": "PUBLICAS",
            "name": "OZ_MAGICAL_IP",
            "plan": 314,
            "gem_port": 14
        },
        "OZ_SKY_IP": {
            "line_profile": 58,
            "srv_profile": 315,
            "vlan": 102,
            "provider": "PUBLICAS",
            "name": "OZ_SKY_IP",
            "plan": 315,
            "gem_port": 14
        },
    },
    "2": {
        "OZ_PLUS_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "name": "OZ_PLUS_1",
            "provider": "INTER",
            "plan": 47,
            "gem_port": 14
        },
        "OZ_MAX_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_MAX_1",
            "plan": 46,
            "gem_port": 14
        },
        "OZ_NEXT_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_NEXT_1",
            "plan": 40,
            "gem_port": 14
        },
        "OZ_MAGICAL_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_MAGICAL_1",
            "plan": 39,
            "gem_port": 14
        },
        "OZ_SKY_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_SKY_1",
            "plan": 45,
            "gem_port": 14
        },
        "OZ_START_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_START_1",
            "plan": 23,
            "gem_port": 14
        },
        "OZ_FAMILY_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_FAMILY_1",
            "plan": 25,
            "gem_port": 14
        },
        "OZ_EMPRENDE_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_EMPRENDE_1",
            "plan": 42,
            "gem_port": 14
        },
        "OZ_CONECTA_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_CONECTA_1",
            "plan": 44,
            "gem_port": 14
        },
        "OZ_INICIATE_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_INICIATE_1",
            "plan": 43,
            "gem_port": 14
        },
        "OZ_LIFT_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_LIFT_1",
            "plan": 6,
            "gem_port": 14
        },
        "OZ_UP_1": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_UP_1",
            "plan": 49,
            "gem_port": 14
        },
        "OZ_PLUS_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_PLUS_2",
            "plan": 47,
            "gem_port": 14
        },
        "OZ_MAX_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_MAX_2",
            "plan": 46,
            "gem_port": 14
        },
        "OZ_NEXT_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_NEXT_2",
            "plan": 40,
            "gem_port": 14
        },
        "OZ_MAGICAL_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_MAGICAL_2",
            "plan": 39,
            "gem_port": 14
        },
        "OZ_SKY_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_SKY_2",
            "plan": 45,
            "gem_port": 14
        },
        "OZ_START_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_START_2",
            "plan": 23,
            "gem_port": 14
        },
        "OZ_FAMILY_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_FAMILY_2",
            "plan": 25,
            "gem_port": 14
        },
        "OZ_EMPRENDE_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_EMPRENDE_2",
            "plan": 42,
            "gem_port": 14
        },
        "OZ_CONECTA_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_CONECTA_2",
            "plan": 44,
            "gem_port": 14
        },
        "OZ_INICIATE_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_INICIATE_2",
            "plan": 43,
            "gem_port": 14
        },
        "OZ_LIFT_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_LIFT_2",
            "plan": 6,
            "gem_port": 14
        },
        "OZ_UP_2": {
            "line_profile": 2,
            "srv_profile": 2,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_UP_2",
            "plan": 49,
            "gem_port": 14
        },
        "OZ_PLUS_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_PLUS_IP",
            "plan": 47,
            "gem_port": 14
        },
        "OZ_MAX_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_MAX_IP",
            "plan": 46,
            "gem_port": 14
        },
        "OZ_NEXT_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_NEXT_IP",
            "plan": 40,
            "gem_port": 14
        },
        "OZ_MAGICAL_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_MAGICAL_IP",
            "plan": 39,
            "gem_port": 14
        },
        "OZ_SKY_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_SKY_IP",
            "plan": 45,
            "gem_port": 14
        },
        "OZ_START_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_START_IP",
            "plan": 23,
            "gem_port": 14
        },
        "OZ_FAMILY_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_FAMILY_IP",
            "plan": 25,
            "gem_port": 14
        },
        "OZ_EMPRENDE_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_EMPRENDE_IP",
            "plan": 42,
            "gem_port": 14
        },
        "OZ_CONECTA_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_CONECTA_IP",
            "plan": 44,
            "gem_port": 14
        },
        "OZ_INICIATE_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_INICIATE_IP",
            "plan": 43,
            "gem_port": 14
        },
        "OZ_LIFT_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_LIFT_IP",
            "plan": 6,
            "gem_port": 14
        },
        "OZ_UP_IP": {
            "line_profile": 4,
            "srv_profile": 2,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_UP_IP",
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
            "name": "OZ_PLUS_1",
            "plan": 49,
            "gem_port": 14
        },
        "OZ_MAX_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_MAX_1",
            "plan": 48,
            "gem_port": 14
        },
        "OZ_NEXT_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_NEXT_1",
            "plan": 33,
            "gem_port": 14
        },
        "OZ_MAGICAL_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_MAGICAL_1",
            "plan": 32,
            "gem_port": 14
        },
        "OZ_SKY_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_SKY_1",
            "plan": 47,
            "gem_port": 14
        },
        "OZ_START_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_START_1",
            "plan": 9,
            "gem_port": 14
        },
        "OZ_FAMILY_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_FAMILY_1",
            "plan": 15,
            "gem_port": 14
        },
        "OZ_EMPRENDE_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_EMPRENDE_1",
            "plan": 44,
            "gem_port": 14
        },
        "OZ_CONECTA_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_CONECTA_1",
            "plan": 46,
            "gem_port": 14
        },
        "OZ_INICIATE_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_INICIATE_1",
            "plan": 45,
            "gem_port": 14
        },
        "OZ_LIFT_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_LIFT_1",
            "plan": 34,
            "gem_port": 14
        },
        "OZ_UP_1": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1101,
            "provider": "INTER",
            "name": "OZ_UP_1",
            "plan": 36,
            "gem_port": 14
        },
        "OZ_PLUS_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_PLUS_2",
            "plan": 49,
            "gem_port": 14
        },
        "OZ_MAX_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_MAX_2",
            "plan": 48,
            "gem_port": 14
        },
        "OZ_NEXT_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_NEXT_2",
            "plan": 33,
            "gem_port": 14
        },
        "OZ_MAGICAL_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_MAGICAL_2",
            "plan": 32,
            "gem_port": 14
        },
        "OZ_SKY_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_SKY_2",
            "plan": 47,
            "gem_port": 14
        },
        "OZ_START_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_START_2",
            "plan": 9,
            "gem_port": 14
        },
        "OZ_FAMILY_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_FAMILY_2",
            "plan": 15,
            "gem_port": 14
        },
        "OZ_EMPRENDE_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_EMPRENDE_2",
            "plan": 44,
            "gem_port": 14
        },
        "OZ_CONECTA_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_CONECTA_2",
            "plan": 46,
            "gem_port": 14
        },
        "OZ_INICIATE_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_INICIATE_2",
            "plan": 45,
            "gem_port": 14
        },
        "OZ_LIFT_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_LIFT_2",
            "plan": 34,
            "gem_port": 14
        },
        "OZ_UP_2": {
            "line_profile": 2,
            "srv_profile": 1,
            "vlan": 1102,
            "provider": "VNET",
            "name": "OZ_UP_2",
            "plan": 36,
            "gem_port": 14
        },
        "OZ_PLUS_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_PLUS_IP",
            "plan": 49,
            "gem_port": 14
        },
        "OZ_MAX_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_MAX_IP",
            "plan": 48,
            "gem_port": 14
        },
        "OZ_NEXT_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_NEXT_IP",
            "plan": 33,
            "gem_port": 14
        },
        "OZ_MAGICAL_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_MAGICAL_IP",
            "plan": 32,
            "gem_port": 14
        },
        "OZ_SKY_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_SKY_IP",
            "plan": 47,
            "gem_port": 14
        },
        "OZ_START_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_START_IP",
            "plan": 9,
            "gem_port": 14
        },
        "OZ_FAMILY_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_FAMILY_IP",
            "plan": 15,
            "gem_port": 14
        },
        "OZ_EMPRENDE_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_EMPRENDE_IP",
            "plan": 44,
            "gem_port": 14
        },
        "OZ_CONECTA_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_CONECTA_IP",
            "plan": 46,
            "gem_port": 14
        },
        "OZ_INICIATE_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_INICIATE_IP",
            "plan": 45,
            "gem_port": 14
        },
        "OZ_LIFT_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_LIFT_IP",
            "plan": 34,
            "gem_port": 14
        },
        "OZ_UP_IP": {
            "line_profile": 5,
            "srv_profile": 1,
            "vlan": 1104,
            "provider": "PUBLICAS",
            "name": "OZ_UP_IP",
            "plan": 36,
            "gem_port": 14
        },
    }
}
