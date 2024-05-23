from helpers.constants.definitions import Plan, Onu

plan_list = [
    Plan(
        profile="GENERICO1",
        line_profile="Generic_1_V1240",
        srv_profile="Generic_1_V1240",
        gem_port=1,
        vlan=1240,
        traffic_table=110,
        name="OZ_FAMILY_A",
    )
]

onu_list = [
  Onu(device="EG8141A5", mode="Routing"),
  Onu(device="EG8145X6", mode="Routing"),
  Onu(device="EG8010Hv6", mode="Bridging"),
]