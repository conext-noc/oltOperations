condition_onu_temp = "Temperature\(C\)                         : "
condition_onu_pwr = "Rx optical power\(dBm\)                  : "

condition_onu_last_down_cause = ("Last down cause         : ", "Last up time")
condition_onu_last_down_time = ("Last down time          : ", "Last dying gasp time")
condition_onu_status = ("Run state               : ", "Config state")

port_summary = [
    {
        "name": "state",
        "start": -4,
        "end": -3,
        "header": ",onu_id,state,up_date,up_time,down_date,down_time,down_cause_1,down_cause_2,down_cause_3,down_cause_4,down_cause_5,down_cause_6,down_cause_7,down_cause_8",
    },
    {
        "name": "names",
        "start": -2,
        "end": -1,
        "header": ",onu_id,sn,device,distance,rx_tx_power,name1,name2,name3,name4,name5,name6,name7,name8,name9,name10,",
    },
]

condition_port_summary = (
    "------------------------------------------------------------------------------"
)

ports = {
    "olt": {
        "1": [
            {"fsp": "0/1/0"},
            {"fsp": "0/1/1"},
            {"fsp": "0/1/2"},
            {"fsp": "0/1/3"},
            {"fsp": "0/1/4"},
            {"fsp": "0/1/5"},
            {"fsp": "0/1/6"},
            {"fsp": "0/1/7"},
            {"fsp": "0/1/8"},
            {"fsp": "0/1/9"},
            {"fsp": "0/1/10"},
            {"fsp": "0/1/11"},
            {"fsp": "0/1/12"},
            {"fsp": "0/1/13"},
            {"fsp": "0/1/14"},
            {"fsp": "0/1/15"},
            {"fsp": "0/2/0"},
            {"fsp": "0/2/1"},
            {"fsp": "0/2/2"},
            {"fsp": "0/2/3"},
            {"fsp": "0/2/4"},
            {"fsp": "0/2/5"},
            {"fsp": "0/2/6"},
            {"fsp": "0/2/7"},
            {"fsp": "0/2/8"},
            {"fsp": "0/2/9"},
            {"fsp": "0/2/10"},
            {"fsp": "0/2/11"},
            {"fsp": "0/2/12"},
            {"fsp": "0/2/13"},
            {"fsp": "0/2/14"},
            {"fsp": "0/2/15"},
            {"fsp": "0/3/0"},
            {"fsp": "0/3/1"},
            {"fsp": "0/3/2"},
            {"fsp": "0/3/3"},
            {"fsp": "0/3/4"},
            {"fsp": "0/3/5"},
            {"fsp": "0/3/6"},
            {"fsp": "0/3/7"},
            {"fsp": "0/3/8"},
            {"fsp": "0/3/9"},
            {"fsp": "0/3/10"},
            {"fsp": "0/3/11"},
            {"fsp": "0/3/12"},
            {"fsp": "0/3/13"},
            {"fsp": "0/3/14"},
            {"fsp": "0/3/15"},
            {"fsp": "0/4/0"},
            {"fsp": "0/4/1"},
            {"fsp": "0/4/2"},
            {"fsp": "0/4/3"},
            {"fsp": "0/4/4"},
            {"fsp": "0/4/5"},
            {"fsp": "0/4/6"},
            {"fsp": "0/4/7"},
            {"fsp": "0/4/8"},
            {"fsp": "0/4/9"},
            {"fsp": "0/4/10"},
            {"fsp": "0/4/11"},
            {"fsp": "0/4/12"},
            {"fsp": "0/4/13"},
            {"fsp": "0/4/14"},
            {"fsp": "0/4/15"},
            {"fsp": "0/5/0"},
            {"fsp": "0/5/1"},
            {"fsp": "0/5/2"},
            {"fsp": "0/5/3"},
            {"fsp": "0/5/4"},
            {"fsp": "0/5/5"},
            {"fsp": "0/5/6"},
            {"fsp": "0/5/7"},
            {"fsp": "0/5/8"},
            {"fsp": "0/5/9"},
            {"fsp": "0/5/10"},
            {"fsp": "0/5/11"},
            {"fsp": "0/5/12"},
            {"fsp": "0/5/13"},
            {"fsp": "0/5/14"},
            {"fsp": "0/5/15"},
            # {"fsp": "0/6/0"},
            {"fsp": "0/6/1"},
            {"fsp": "0/6/2"},
            {"fsp": "0/6/3"},
            {"fsp": "0/6/4"},
            {"fsp": "0/6/5"},
            {"fsp": "0/6/6"},
            {"fsp": "0/6/7"},
            {"fsp": "0/6/8"},
            {"fsp": "0/6/9"},
            {"fsp": "0/6/10"},
            {"fsp": "0/6/11"},
            {"fsp": "0/6/12"},
            {"fsp": "0/6/13"},
            {"fsp": "0/6/14"},
            {"fsp": "0/6/15"},
            {"fsp": "0/7/0"},
            {"fsp": "0/7/1"},
            {"fsp": "0/7/2"},
            {"fsp": "0/7/3"},
            {"fsp": "0/7/4"},
            {"fsp": "0/7/5"},
            {"fsp": "0/7/6"},
            {"fsp": "0/7/7"},
            {"fsp": "0/7/8"},
            {"fsp": "0/7/9"},
            {"fsp": "0/7/10"},
            {"fsp": "0/7/11"},
            {"fsp": "0/7/12"},
            {"fsp": "0/7/13"},
            {"fsp": "0/7/14"},
            # {"fsp": "0/7/15"},
            {"fsp": "0/10/0"},
            {"fsp": "0/10/1"},
            {"fsp": "0/10/2"},
            # {"fsp": "0/10/3"},
            {"fsp": "0/10/4"},
            {"fsp": "0/10/5"},
            {"fsp": "0/10/6"},
            {"fsp": "0/10/7"},
            {"fsp": "0/10/8"},
            {"fsp": "0/10/9"},
            # {"fsp": "0/10/10"},
            {"fsp": "0/10/11"},
            {"fsp": "0/10/12"},
            {"fsp": "0/10/13"},
            # {"fsp": "0/10/14"},
            {"fsp": "0/10/15"},
            {"fsp": "0/11/0"},
            {"fsp": "0/11/1"},
            {"fsp": "0/11/2"},
            {"fsp": "0/11/3"},
            {"fsp": "0/11/4"},
            {"fsp": "0/11/5"},
            {"fsp": "0/11/6"},
            # {"fsp": "0/11/7"},
            {"fsp": "0/11/8"},
            # {"fsp": "0/11/9"},
            # {"fsp": "0/11/10"},
            # {"fsp": "0/11/11"},
            # {"fsp": "0/11/12"},
            # {"fsp": "0/11/13"},
            # {"fsp": "0/11/14"},
            # {"fsp": "0/11/15"},
        ],
        "2": [
            {"fsp": "0/1/0"},
            {"fsp": "0/1/1"},
            {"fsp": "0/1/2"},
            {"fsp": "0/1/3"},
            {"fsp": "0/1/4"},
            {"fsp": "0/1/5"},
            {"fsp": "0/1/6"},
            {"fsp": "0/1/7"},
            {"fsp": "0/1/8"},
            {"fsp": "0/1/9"},
            {"fsp": "0/1/10"},
            {"fsp": "0/1/11"},
            {"fsp": "0/1/12"},
            {"fsp": "0/1/13"},
            {"fsp": "0/1/14"},
            {"fsp": "0/1/15"},
            {"fsp": "0/2/0"},
            {"fsp": "0/2/1"},
            {"fsp": "0/2/2"},
            {"fsp": "0/2/3"},
            {"fsp": "0/2/4"},
            {"fsp": "0/2/5"},
            {"fsp": "0/2/6"},
            {"fsp": "0/2/7"},
            {"fsp": "0/2/8"},
            {"fsp": "0/2/9"},
            {"fsp": "0/2/10"},
            {"fsp": "0/2/11"},
            {"fsp": "0/2/12"},
            {"fsp": "0/2/13"},
            {"fsp": "0/2/14"},
            {"fsp": "0/2/15"},
            {"fsp": "0/3/0"},
            {"fsp": "0/3/1"},
            {"fsp": "0/3/2"},
            {"fsp": "0/3/3"},
            {"fsp": "0/3/4"},
            {"fsp": "0/3/5"},
            {"fsp": "0/3/6"},
            {"fsp": "0/3/7"},
            {"fsp": "0/3/8"},
            {"fsp": "0/3/9"},
            {"fsp": "0/3/10"},
            {"fsp": "0/3/11"},
            {"fsp": "0/3/12"},
            {"fsp": "0/3/13"},
            {"fsp": "0/3/14"},
            {"fsp": "0/3/15"},
        ],
        "3": [
            {"fsp": "0/1/0"},
            {"fsp": "0/1/1"},
            {"fsp": "0/1/2"},
            {"fsp": "0/1/3"},
            {"fsp": "0/1/4"},
            {"fsp": "0/1/5"},
            {"fsp": "0/1/6"},
            {"fsp": "0/1/7"},
            {"fsp": "0/1/8"},
            {"fsp": "0/1/9"},
            {"fsp": "0/1/10"},
            {"fsp": "0/1/11"},
            {"fsp": "0/1/12"},
            {"fsp": "0/1/13"},
            {"fsp": "0/1/14"},
            {"fsp": "0/1/15"},
            {"fsp": "0/2/0"},
            {"fsp": "0/2/1"},
            {"fsp": "0/2/2"},
            {"fsp": "0/2/3"},
            {"fsp": "0/2/4"},
            {"fsp": "0/2/5"},
            {"fsp": "0/2/6"},
            {"fsp": "0/2/7"},
            {"fsp": "0/2/8"},
            {"fsp": "0/2/9"},
            {"fsp": "0/2/10"},
            {"fsp": "0/2/11"},
            {"fsp": "0/2/12"},
            {"fsp": "0/2/13"},
            {"fsp": "0/2/14"},
            {"fsp": "0/2/15"},
        ],
    },
    "count": {
        "1": {
            "0/1/0": 0,
            "0/1/1": 0,
            "0/1/2": 0,
            "0/1/3": 0,
            "0/1/4": 0,
            "0/1/5": 0,
            "0/1/6": 0,
            "0/1/7": 0,
            "0/1/8": 0,
            "0/1/9": 0,
            "0/1/10": 0,
            "0/1/11": 0,
            "0/1/12": 0,
            "0/1/13": 0,
            "0/1/14": 0,
            "0/1/15": 0,
            "0/2/0": 0,
            "0/2/1": 0,
            "0/2/2": 0,
            "0/2/3": 0,
            "0/2/4": 0,
            "0/2/5": 0,
            "0/2/6": 0,
            "0/2/7": 0,
            "0/2/8": 0,
            "0/2/9": 0,
            "0/2/10": 0,
            "0/2/11": 0,
            "0/2/12": 0,
            "0/2/13": 0,
            "0/2/14": 0,
            "0/2/15": 0,
            "0/3/0": 0,
            "0/3/1": 0,
            "0/3/2": 0,
            "0/3/3": 0,
            "0/3/4": 0,
            "0/3/5": 0,
            "0/3/6": 0,
            "0/3/7": 0,
            "0/3/8": 0,
            "0/3/9": 0,
            "0/3/10": 0,
            "0/3/11": 0,
            "0/3/12": 0,
            "0/3/13": 0,
            "0/3/14": 0,
            "0/3/15": 0,
            "0/4/0": 0,
            "0/4/1": 0,
            "0/4/2": 0,
            "0/4/3": 0,
            "0/4/4": 0,
            "0/4/5": 0,
            "0/4/6": 0,
            "0/4/7": 0,
            "0/4/8": 0,
            "0/4/9": 0,
            "0/4/10": 0,
            "0/4/11": 0,
            "0/4/12": 0,
            "0/4/13": 0,
            "0/4/14": 0,
            "0/4/15": 0,
            "0/5/0": 0,
            "0/5/1": 0,
            "0/5/2": 0,
            "0/5/3": 0,
            "0/5/4": 0,
            "0/5/5": 0,
            "0/5/6": 0,
            "0/5/7": 0,
            "0/5/8": 0,
            "0/5/9": 0,
            "0/5/10": 0,
            "0/5/11": 0,
            "0/5/12": 0,
            "0/5/13": 0,
            "0/5/14": 0,
            "0/5/15": 0,
            "0/6/0": 0,
            "0/6/1": 0,
            "0/6/2": 0,
            "0/6/3": 0,
            "0/6/4": 0,
            "0/6/5": 0,
            "0/6/6": 0,
            "0/6/7": 0,
            "0/6/8": 0,
            "0/6/9": 0,
            "0/6/10": 0,
            "0/6/11": 0,
            "0/6/12": 0,
            "0/6/13": 0,
            "0/6/14": 0,
            "0/6/15": 0,
            "0/7/0": 0,
            "0/7/1": 0,
            "0/7/2": 0,
            "0/7/3": 0,
            "0/7/4": 0,
            "0/7/5": 0,
            "0/7/6": 0,
            "0/7/7": 0,
            "0/7/8": 0,
            "0/7/9": 0,
            "0/7/10": 0,
            "0/7/11": 0,
            "0/7/12": 0,
            "0/7/13": 0,
            "0/7/14": 0,
            "0/7/15": 0,
            "0/10/0": 0,
            "0/10/1": 0,
            "0/10/2": 0,
            "0/10/3": 0,
            "0/10/4": 0,
            "0/10/5": 0,
            "0/10/6": 0,
            "0/10/7": 0,
            "0/10/8": 0,
            "0/10/9": 0,
            "0/10/10": 0,
            "0/10/11": 0,
            "0/10/12": 0,
            "0/10/13": 0,
            "0/10/14": 0,
            "0/10/15": 0,
            "0/11/0": 0,
            "0/11/1": 0,
            "0/11/2": 0,
            "0/11/3": 0,
            "0/11/4": 0,
            "0/11/5": 0,
            "0/11/6": 0,
            "0/11/7": 0,
            "0/11/8": 0,
            "0/11/9": 0,
            "0/11/10": 0,
            "0/11/11": 0,
            "0/11/12": 0,
            "0/11/13": 0,
            "0/11/14": 0,
            "0/11/15": 0,
        },
        "2": {
            "0/1/0": 0,
            "0/1/1": 0,
            "0/1/2": 0,
            "0/1/3": 0,
            "0/1/4": 0,
            "0/1/5": 0,
            "0/1/6": 0,
            "0/1/7": 0,
            "0/1/8": 0,
            "0/1/9": 0,
            "0/1/10": 0,
            "0/1/11": 0,
            "0/1/12": 0,
            "0/1/13": 0,
            "0/1/14": 0,
            "0/1/15": 0,
            "0/2/0": 0,
            "0/2/1": 0,
            "0/2/2": 0,
            "0/2/3": 0,
            "0/2/4": 0,
            "0/2/5": 0,
            "0/2/6": 0,
            "0/2/7": 0,
            "0/2/8": 0,
            "0/2/9": 0,
            "0/2/10": 0,
            "0/2/11": 0,
            "0/2/12": 0,
            "0/2/13": 0,
            "0/2/14": 0,
            "0/2/15": 0,
            "0/3/0": 0,
            "0/3/1": 0,
            "0/3/2": 0,
            "0/3/3": 0,
            "0/3/4": 0,
            "0/3/5": 0,
            "0/3/6": 0,
            "0/3/7": 0,
            "0/3/8": 0,
            "0/3/9": 0,
            "0/3/10": 0,
            "0/3/11": 0,
            "0/3/12": 0,
            "0/3/13": 0,
            "0/3/14": 0,
            "0/3/15": 0,
        },
        "3": {
            "0/1/0": 0,
            "0/1/1": 0,
            "0/1/2": 0,
            "0/1/3": 0,
            "0/1/4": 0,
            "0/1/5": 0,
            "0/1/6": 0,
            "0/1/7": 0,
            "0/1/8": 0,
            "0/1/9": 0,
            "0/1/10": 0,
            "0/1/11": 0,
            "0/1/12": 0,
            "0/1/13": 0,
            "0/1/14": 0,
            "0/1/15": 0,
            "0/2/0": 0,
            "0/2/1": 0,
            "0/2/2": 0,
            "0/2/3": 0,
            "0/2/4": 0,
            "0/2/5": 0,
            "0/2/6": 0,
            "0/2/7": 0,
            "0/2/8": 0,
            "0/2/9": 0,
            "0/2/10": 0,
            "0/2/11": 0,
            "0/2/12": 0,
            "0/2/13": 0,
            "0/2/14": 0,
            "0/2/15": 0,
        },
    },
}

vp_count = {
    "1": {
        "vp_ttl": 0,
        "vp_active_cnt": 0,
        "vp_deactive_cnt": 0,
        "vp_los_cnt": 0,
        "vp_off_cnt": 0,
    },
    "2": {
        "vp_vnet": 0,
        "vp_inter": 0,
        "vp_public_ip": 0,
        "OZ_0": 0,
        "OZ_MAX": 0,
        "OZ_SKY": 0,
        "OZ_MAGICAL": 0,
        "OZ_NEXT": 0,
        "OZ_PLUS": 0,
        "OZ_DEDICADO": 0,
        "OZ_CONECTA": 0,
        "NA": 0,
    },
}


speed = {
    "up": "Up traffic \(kbps\)          : ",
    "down": "Down traffic \(kbps\)        : ",
    "cond": "----------------------------------------------------------------",
}

routers_ints = {
    "RTRE1": {"ip": "181.232.180.1", "ints": ["GigabitEthernet0/3/7(10G)"]},
    "RTRE2": {
        "ip": "181.232.180.2",
        "ints": ["GigabitEthernet0/3/7(10G)", "GigabitEthernet0/3/8(10G)"],
    },
    "RTRA1": {
        "ip": "181.232.180.3",
        "pool": [
            "residencial_1",
            "plan_0_inet1",
            "plan_0_inet2",
            "plan_1_inet1",
            "plan_1_inet2",
            "plan_2_inet1",
            "plan_2_inet2",
            "plan_3_inet1",
            "plan_3_inet2",
            "plan_4_inet1",
            "plan_4_inet2",
            "plan_5_inet1",
            "plan_5_inet2",
        ],
        "section": {
            "1": {"start": 4, "end": 5},
            "2": {"start": 7, "end": 8},
        },
    },
    "RTRA2": {
        "ip": "181.232.180.4",
        "pool": [
            "residencial_2",
            "plan_0_inet1",
            "plan_0_inet2",
            "plan_1_inet1",
            "plan_2_inet1",
            "plan_3_inet1",
            "plan_4_inet1",
            "plan_4_inet2",
            "plan_5_inet1",
            "plan_5_inet2",
        ],
        "section": {
            "1": {"start": 4, "end": 5},
            "2": {"start": 7, "end": 8},
        },
    },
}

interface = {
    "start": "InUti/OutUti: input utility/output utility",
    "end": "NULL0",
    "header": "Interface,PHY,Protocol,InUti,OutUti,inErrors,outErrors\n",
}

rtr_conflicts = {
    "condition": "---------------------------------------------------------------------------------------",
    "headerConf": "NA,ID,start,end,total,used,idle,conflict,disable,reserved,staticBind",
    "headerSect": "ip,mac,userId,lease,status,index,na",
}
