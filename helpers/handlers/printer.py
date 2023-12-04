from datetime import datetime
import userpaths
import warnings


docs = userpaths.get_my_documents()
date = datetime.now()

color = {
    "activated": "\u001b[38;5;2m",
    "suspended": "\u001b[38;5;8m",
    "suspended+": "\u001b[38;5;235m",
    "success": "\u001b[38;5;46m",
    "warning": "\u001b[38;5;202m",
    "off": "\u001b[38;5;9m",
    "los": "\u001b[38;5;196m",
    "los+": "\u001b[38;5;88m",
    "problems": "\u001b[38;5;5m",
    "ok": "\u001b[38;5;33m",
    "unknown": "\u001b[38;5;21m",
    "fail": "\u001b[38;5;1m",
    "end": "\u001b[0m",
    "info": "\u001b[38;5;3m",
    "normal": "",
}

USER_NAME = ""

def color_formatter(txt, variant):
    paint = "normal" if variant == "" else variant
    return color[paint] + txt + color["end"]

def log(value, variant):
    fl = f"{USER_NAME}_{date.year}-{date.month}-{date.day}.txt"
    currTime = datetime.now()
    now = f"[{currTime.hour}:{currTime.minute}:{currTime.second}]"
    formatted_value = color_formatter(value, variant)
    
    # Open the file using the 'with' statement to ensure it's properly closed
    with open(f"{docs}/logs/{fl}", "a", encoding="utf-8") as log_file:
        # Ignore ResourceWarning
        warnings.filterwarnings("ignore", category=ResourceWarning)
        print(formatted_value)
        print(f"{now}\n{value}", file=log_file)

def inp(message):
    global USER_NAME
    if USER_NAME == "":
        USER_NAME = input("ingrese su nombre : ").upper()
    fl = f"{USER_NAME}_{date.year}-{date.month}-{date.day}.txt"
    currTime = datetime.now()
    now = f"[{currTime.hour}:{currTime.minute}:{currTime.second}]"
    data = input(message).upper()
    
    # Open the file using the 'with' statement to ensure it's properly closed
    with open(f"{docs}/logs/{fl}", "a", encoding="utf-8") as log_file:
        # Ignore ResourceWarning
        warnings.filterwarnings("ignore", category=ResourceWarning)
        print(f"{now}\n{message} {data}", file=log_file)
    
    return data