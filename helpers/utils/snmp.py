from pysnmp.hlapi import *


def SNMP_get(community, host, oid,port,fsp_inicial,index="0"):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((host, port)),
        ContextData(),
        ObjectType(ObjectIdentity(oid+f".{fsp_inicial}.{index}")),
        lexicographicMode=False
    )

    for errorIndication, errorStatus, errorIndex, varBinds in iterator:
        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                resp = varBind[1].prettyPrint()
                return resp
                
def SNMP_set(community, host, oid,port,fsp_inicial,index,value):
    new_value = Integer(value)
    iterator = setCmd(
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((host, port)),
        ContextData(),
        ObjectType(ObjectIdentity(oid+f".{fsp_inicial}.{index}"),new_value),
    )
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
    for varBind in varBinds:
        print("Ok")


# SNMP_set('ConextRoot','181.232.180.7','1.3.6.1.4.1.2011.6.128.1.1.2.46.1.1',161,'4194312960','0','1')