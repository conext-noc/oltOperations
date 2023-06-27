from helpers.constants import regex_conditions

vp_count = regex_conditions.vp_count

def portCounter(alert, plan_name_id):
    if (alert == "activated"): vp_count['1']['vp_active_cnt'] +=1
    if (alert == "suspended"): vp_count['1']['vp_deactive_cnt'] += 1
    if (alert == "los"): vp_count['1']['vp_los_cnt'] += 1
    if (alert == "off"): vp_count['1']['vp_off_cnt'] += 1

    #PROVIDER
    planNameCounter(plan_name_id, "1", "vp_inter")
    planNameCounter(plan_name_id, "2", "vp_vnet")
    planNameCounter(plan_name_id, "1", "vp_public_ip")

    #PLAN
    planNameCounter(plan_name_id, "0", "OZ_0")
    planNameCounter(plan_name_id, "MAX", "OZ_MAX")
    planNameCounter(plan_name_id, "SKY", "OZ_SKY")
    planNameCounter(plan_name_id, "MAGICAL", "OZ_MAGICAL")
    planNameCounter(plan_name_id, "NEXT", "OZ_NEXT")
    planNameCounter(plan_name_id, "PLUS", "OZ_PLUS")
    planNameCounter(plan_name_id, "DEDICADO", "OZ_DEDICADO")
    planNameCounter(plan_name_id, "CONECTA", "OZ_CONECTA")


def dictToZero(dict):
    for key in dict:
        dict[key] = 0

def planNameCounter(plan_name_id, cond, var):
    if (cond in plan_name_id): vp_count['2'][var] += 1