import os
import re
encoding = "ascii"

def decoder(comm):
  output = comm.recv(65535)
  output = output.decode(encoding)
  return output

def parser(comm, condition, count):
  if(count == "s"):
    output = decoder(comm)
    print(output, file=open("Result.txt", "w"))
    value = open("Result.txt", "r").read()
    regex = re.search(condition, value)
    os.remove("Result.txt")
    return (value, regex)
    
  if(count == "m"):
    output = decoder(comm)
    print(output, file=open(f"Result.txt", "w"))
    value = open(f"Result.txt", "r").read()
    result = []
    res = re.finditer(condition,value)
    os.remove("Result.txt")
    for match in res:
      result.append(match.span())
    return(value,result)
  
def check(value,condition):
  regex = re.search(condition, value)
  return regex

def checkIter(value,condition):
  result = []
  res = re.finditer(condition,value)
  for match in res:
    result.append(match.span())
  return result
