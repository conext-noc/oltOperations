from helpers.outputDecoder import txt2csvFormatter
import re
import os
from helpers.fileHandler import fromCsv
from helpers.printer import log


def table2Dict(header,data, name,idx, tp):
    value = re.sub(" +", " ", data).replace(" ", ",")
    log(value, file=open("data.txt", "w"))
    txt2csvFormatter("data.txt")
    value = open("data.txt", "r").read().replace(" +", "")
    os.remove("data.txt")
    log(header + value, file=open("data.txt", "w"))
    data = open("data.txt", "r").read().replace(" +", "")
    os.remove("data.txt")
    log(data, file=open(f"{name}{idx}{tp}.csv", "w"))
    
def toDict(header,data):
    value = re.sub(" +", " ", data).replace(" ", ",")
    log(header + value, file=open("data.csv", "w"))
    result = fromCsv("data.csv")
    os.remove("data.csv")
    return result