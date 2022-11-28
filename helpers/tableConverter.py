from helpers.outputDecoder import txt2csvFormatter
import re
import os
from helpers.fileHandler import fromCsv

def table2Dict(header,data, name,idx, tp):
    value = re.sub(" +", " ", data).replace(" ", ",")
    res = header + value
    print(res[:-1], file=open(f"{name}{idx}{tp}.csv", "w", encoding="latin-1"))
    
def toDict(header,data):
    value = re.sub(" +", " ", data).replace(" ", ",")
    print(header + value, file=open("data.csv", "w"))
    result = fromCsv("data.csv")
    os.remove("data.csv")
    return result