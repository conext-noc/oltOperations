from helpers.outputDecoder import txt2csvFormatter
import re
import os


def table2Dict(header,data, name,idx, tp):
    value = re.sub(" +", " ", data).replace(" ", ",")
    print(value, file=open("data.txt", "w"))
    txt2csvFormatter("data.txt")
    value = open("data.txt", "r").read().replace(" +", "")
    os.remove("data.txt")
    print(header + value, file=open("data.txt", "w"))
    data = open("data.txt", "r").read().replace(" +", "")
    os.remove("data.txt")
    print(data, file=open(f"{name}{idx}{tp}.csv", "w"))
