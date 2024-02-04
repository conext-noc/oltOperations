import os
from time import sleep
from pysnmp.hlapi import (
    CommunityData,
    ContextData,
    ObjectType,
    ObjectIdentity,
    UdpTransportTarget,
    bulkCmd,
    SnmpEngine,
    nextCmd,
)
from dotenv import load_dotenv

load_dotenv()

class SNMPBulk:
    MAX_RETRIES = 3
    RETRY_DELAY = 2

    def __init__(self, target, *oids):
        self.community = CommunityData(os.environ["SNMP_COMMUNITY"])
        self.target = UdpTransportTarget((target, 161))
        self.context = ContextData()
        self.non_repeaters = 10
        self.max_repetitions = 10
        self.oids = [ObjectType(ObjectIdentity(oid)) for oid in oids]

    def execute(self):
        retry_count = 0

        while retry_count < self.MAX_RETRIES:
            try:
                error_indication, error_status, error_index, data = next(
                    bulkCmd(
                        SnmpEngine(),
                        self.community,
                        self.target,
                        self.context,
                        self.non_repeaters,
                        self.max_repetitions,
                        *self.oids,
                    )
                )
                # print(error_indication, error_status, error_index)
                return data
            except Exception as e:
                print(f"Error: {e}. Retrying...")
                retry_count += 1
                sleep(self.RETRY_DELAY)

        print("Max retries reached. Unable to retrieve SNMP data.")
        return None
class SNMPNext:
    def __init__(self, target, oid):
        self.community = CommunityData(os.environ["SNMP_COMMUNITY"])
        self.target = UdpTransportTarget((target, 161))
        self.context = ContextData()
        self.non_repeaters = 10
        self.max_repetitions = 10
        self.oids = ObjectType(ObjectIdentity(oid))

    def execute(self):
        values = []
        iterator = nextCmd(
            SnmpEngine(),
            self.community,
            self.target,
            self.context,
            self.oids,
            lexicographicMode=False,
            maxRepetitions = self.max_repetitions,
        )
        for errorIndication, errorStatus, errorIndex, varBinds in iterator:
            if errorIndication:
                print(errorIndication)
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            else:
                for varBind in varBinds:
                    values.append(varBind)
        return values