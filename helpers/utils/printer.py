from datetime import datetime
import userpaths
docs = userpaths.get_my_documents()
date = datetime.now()
fl = f"{date.year}-{date.month}-{date.day}.txt"

color = {
    "activated": "\u001b[38;5;2m",
    "suspended": "\u001b[38;5;8m",
    "suspended+": "\u001b[38;5;235m",
    "success": "\u001b[38;5;46m",
    "warning": "\u001b[38;5;202m",
    "off": "\u001b[38;5;9m",
    "los1": "\u001b[38;5;196m",
    "los1": "\u001b[38;5;196m",
    "los2": "\u001b[38;5;88m",
    "problems": "\u001b[38;5;5m",
    "ok": "\u001b[38;5;33m",
    "unknown": "\u001b[38;5;21m",
    "fail": "\u001b[38;5;1m",
    "end": "\u001b[0m",
    "info": "\u001b[38;5;3m",
    "normal":""
}


def colorFormatter(txt, variant):
    paint = "normal" if variant == "" else variant
    return color[paint] + txt + color["end"]


def log(value):
    currTime = datetime.now()
    now = f"[{currTime.hour}:{currTime.minute}:{currTime.second}]"
    print(value)
    print(f"{now}\n{value}", file=open(f"{docs}/logs/{fl}", "a",encoding="utf-8"))


def inp(message):
    currTime = datetime.now()
    now = f"[{currTime.hour}:{currTime.minute}:{currTime.second}]"
    data = input(message).upper()
    print(f"{now}\n{message} {data}", file=open(f"{docs}/logs/{fl}", "a",encoding="utf-8"))
    return data
