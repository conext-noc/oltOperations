from datetime import datetime
import userpaths
docs = userpaths.get_my_documents()
date = datetime.now()
fl = f"{date.year}-{date.month}-{date.day}_{date.hour}-{date.minute}.txt"

def log(value):
  print(value)
  print(value, file=open(f"{docs}/logs/{fl}","a"))

def inp(message):
  data = input(message)
  print(f"{message} {data}", file=open(f"{docs}/logs/{fl}","a"))
  return data