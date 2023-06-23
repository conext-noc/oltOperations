from datetime import datetime


def condition(clt):
    t1 = datetime.fromisoformat(str(datetime.now()))
    if isinstance(clt["last_down_date"], float):
        t1 = datetime.strptime(
            f'{clt["last_down_date"] } {clt["last_down_time"] }',
            "%Y-%m-%d %H:%M:%S",
        )
    t2 = datetime.fromisoformat(str(datetime.now()))
    clientTime = t2 - t1
    OFFLINE = clt["status"] == "offline"
    LOS = (
        not isinstance(clt["last_down_cause"], float)
        and "LOS" in clt["last_down_cause"]
        and OFFLINE
        and clt["state"] == "active"
    )
    LOS_ = (
        not isinstance(clt["last_down_cause"], float)
        and "LOS" in clt["last_down_cause"]
        and OFFLINE
        and clt["state"] == "active"
        and clientTime.days >= 90
    )
    SUS = OFFLINE and clt["state"] == "deactivated"
    SUS_ = OFFLINE and clt["state"] == "deactivated" and clientTime.days >= 5
    OFF = (
        not isinstance(clt["last_down_cause"], float)
        and "dying-gasp" in clt["last_down_cause"]
        and OFFLINE
        and clt["state"] == "active"
    )
    UKN = isinstance(clt["last_down_date"], float) and OFFLINE

    alert = (
        "los"
        if LOS
        else "los+"
        if LOS_
        else "suspended"
        if SUS
        else "suspended+"
        if SUS_
        else "off"
        if OFF
        else "unknown"
        if UKN
        else "activated"
    )

    return alert
