from helpers.utils.decoder import decoder, check, checkIter
from helpers.failHandler.fail import failChecker
from helpers.utils.printer import log, colorFormatter
from helpers.fileFormatters.fileHandler import dataToDict

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
    "210": "PLAN_0",
    "211": "PLAN_1",
    "212": "PLAN_2",
    "213": "PLAN_3",
    "214": "PLAN_4",
    "215": "PLAN_5",
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

plans = {
    "OZ_0_1": {
        "lineProfile": 3,
        "srvProfile": 110,
        "vlan": 1100,
        "plan": 110,
        "gemPort": 10
    },
    "OZ_PLUS_1": {
        "lineProfile": 17,
        "srvProfile": 111,
        "vlan": 1101,
        "plan": 111,
        "gemPort": 11
    },
    "OZ_MAX_1": {
        "lineProfile": 27,
        "srvProfile": 112,
        "vlan": 1102,
        "plan": 112,
        "gemPort": 12
    },
    "OZ_NEXT_1": {
        "lineProfile": 37,
        "srvProfile": 113,
        "vlan": 1103,
        "plan": 113,
        "gemPort": 13
    },
    "OZ_MAGICAL_1": {
        "lineProfile": 47,
        "srvProfile": 114,
        "vlan": 1104,
        "plan": 114,
        "gemPort": 14
    },
    "OZ_SKY_1": {
        "lineProfile": 57,
        "srvProfile": 115,
        "vlan": 1105,
        "plan": 115,
        "gemPort": 15
    },
    "OZ_0_2": {
        "lineProfile": 3,
        "srvProfile": 210,
        "vlan": 2100,
        "plan": 210,
        "gemPort": 1
    },
    "OZ_PLUS_2": {
        "lineProfile": 17,
        "srvProfile": 211,
        "vlan": 2101,
        "plan": 211,
        "gemPort": 21
    },
    "OZ_MAX_2": {
        "lineProfile": 27,
        "srvProfile": 212,
        "vlan": 2102,
        "plan": 212,
        "gemPort": 22
    },
    "OZ_NEXT_2": {
        "lineProfile": 37,
        "srvProfile": 213,
        "vlan": 2103,
        "plan": 213,
        "gemPort": 23
    },
    "OZ_MAGICAL_2": {
        "lineProfile": 47,
        "srvProfile": 214,
        "vlan": 2104,
        "plan": 214,
        "gemPort": 24
    },
    "OZ_SKY_2": {
        "lineProfile": 57,
        "srvProfile": 215,
        "vlan": 2105,
        "plan": 215,
        "gemPort": 25
    },
}
