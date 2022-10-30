def colorFormatter(txt,variant):
  color = {
    "activated": u"\u001b[38;5;2m",
    "suspended": u"\u001b[38;5;8m",
    "success": u"\u001b[38;5;46m",
    "warning": u"\u001b[38;5;130m",
    "off": u"\u001b[38;5;9m",
    "los1": u"\u001b[38;5;196m",
    "los1": u"\u001b[38;5;196m",
    "los2": u"\u001b[38;5;160m",
    "ok": u"\u001b[38;5;33m",
    "fail": u"\u001b[38;5;1m",
    "end": "\u001b[0m",
  }
  return color[variant] + txt + color["end"]