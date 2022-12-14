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


def spidCalc(SLOT, PORT, ID):
    return {
        "I": 12288*(int(SLOT) - 1) + 771 * int(PORT) + 3 * int(ID),
        "V": 12288*(int(SLOT) - 1) + 771 * int(PORT) + 3 * int(ID) + 1,
        "P": 12288*(int(SLOT) - 1) + 771 * int(PORT) + 3 * int(ID) + 2
    }
