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
                resp = varBind.prettyPrint()
                print(resp)
                
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
        print(varBind)
