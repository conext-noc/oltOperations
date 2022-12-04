import re
import os
from helpers.fileHandler import fileToDict


def toDict(header, data):
    value = re.sub(" +", " ", data).replace(" ", ",")
    res = header + value
    print(res[:-1], file=open("data.csv", "w"))
    result = fileToDict("data.csv","C")
    os.remove("data.csv")
    return result
