
from helpers.constants.definitions import rtrs, olts, endpoints
from helpers.handlers.file_formatter import data_to_dict
from helpers.handlers.printer import log
from helpers.handlers.request import db_request
from helpers.utils.decoder import check, check_iter, decoder
from helpers.handlers.request import db_request

def device_acl(comm, command, quit_ssh, device, _):
    acl_start_id_olt = 10
    # STEP 1 : ENTER CORRESPONDING ACL LIST [✅]
    command("acl name SSH_ACCESS") if device in rtrs else command("acl 3000")

    # STEP 2 : GET CORRESPONDING ACL LIST DATA FROM DEVICE [✅]
    command("display this")
    value = decoder(comm)
    re_acl = check_iter(value, "#")
    acl_start = check(value, "rule 1 permit").span()[0] - 1 if device in rtrs else re_acl[-3][1] + acl_start_id_olt
    acl_end = re_acl[-1 if device in rtrs else -2][0]
    
    device_rule = "rtr" if device in rtrs else "olt"
    live_rules = [
            {f"{device_rule}_rule_id": rule[f"{device_rule}_rule_id"], "ip_addr": rule["ip_addr"]}
            for rule in data_to_dict(
                "NA,unused_1,rtr_rule_id,unused_2,unused_3,unused_4,ip_addr,unused_5" if device in rtrs else "unused_1,olt_rule_id,unused_2,unused_3,unused_4,ip_addr,unused_5",
                value[acl_start:acl_end],
            )
            if rule["unused_2"] != "deny"
        ]
    # STEP 3 : GET ACL DATA STORED IN DB [✅]
    acl_db_rules = db_request(endpoints["get_acls"], {})["data"]
    
    # STEP 4 : CORRELATE & FIND POTENTIAL MISMATCH []
    for live_rule in live_rules:
            for db_rule in acl_db_rules:
                if int(live_rule[f"{device_rule}_rule_id"]) == int(db_rule[f"{device_rule}_rule_id"]):
    # STEP 5 : IF MISMATCH FOUND CHANGE CORRESPONDING RULES [✅]
                    if live_rule["ip_addr"] != db_rule["ip_addr"]:
                        log(f"MISMATCH FOUND ON RULE {live_rule[f'{device_rule}_rule_id']} OF {'RTR' if device in rtrs else 'OLT' } {device}", "warning")
                        command(f"undo rule {live_rule[f'{device_rule}_rule_id']}")
                        command("\n")
                        command(f"rule {live_rule[f'{device_rule}_rule_id']} permit ip source {db_rule['ip_addr']} 0")
                        command("commit") if device in rtrs else None
                        command("\n")
                        
                    else:
                        log("NO MISMATCH WAS FOUND!", "success")
    quit_ssh()
    pass