def calculate_spid(data):
    SPID = (
        12288 * (int(data["slot"]) - 1)
        + 771 * int(data["port"])
        + 3 * int(data["onu_id"])
    )
    return {"I": SPID, "P": SPID + 1, "V": SPID + 2}
