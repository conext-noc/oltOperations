from helpers.info.regexConditions import vp_count

def portHandler(client):
    #PROVIDER
    if client["vlan"] == "INTER":
        vp_count['2']['vp_inter'] += 1

    if client["vlan"] == "VNET":
        vp_count['2']['vp_vnet'] += 1

    if client["vlan"] == "IP":
        vp_count['2']['vp_public_ip'] += 1
                
    #PLAN
    if client["plan"] == "OZ_0":
        vp_count['2']['OZ_0'] += 1

    elif client["plan"] == "OZ_MAX":
        vp_count['2']['OZ_MAX'] += 1

    elif client["plan"] == "OZ_SKY":
        vp_count['2']['OZ_SKY'] += 1

    elif client["plan"] == "OZ_MAGICAL":
        vp_count['2']['OZ_MAGICAL'] += 1

    elif client["plan"] == "OZ_NEXT":
        vp_count['2']['OZ_NEXT'] += 1

    elif client["plan"] == "OZ_PLUS":
        vp_count['2']['OZ_PLUS'] += 1

    elif client["plan"] == "OZ_DEDICADO":
        vp_count['2']['OZ_DEDICADO'] += 1

    elif client["plan"] == "OZ_CONECTA":
        vp_count['2']['OZ_CONECTA'] += 1

    else:
        vp_count['2']['NA'] += 1

    vp_count['2']['vp_ttl'] += 1

def dictToZero(dict):
    for key in dict:
        dict[key] = 0


