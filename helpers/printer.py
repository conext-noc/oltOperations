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
}


def colorFormatter(txt, variant):
    return color[variant] + txt + color["end"]

def log(value):
  print(value)
  print(value, file=open(f"{docs}/logs/{fl}","a"))

def inp(message):
  data = input(message)
  print(f"{message} {data}", file=open(f"{docs}/logs/{fl}","a"))
  return data