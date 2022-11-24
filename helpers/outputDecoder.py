import os
import re
from helpers.printer import log


def decoder(comm):
    data = ""
    chunk = comm.recv(1024000000)
    chunk = chunk.decode("latin-1")
    data += chunk
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    data = ansi_escape.sub("", data)
    return data


def parser(comm, condition, count):
    if count == "s":
        output = decoder(comm)
        log(output, file=open("Result.txt", "w"))
        value = open("Result.txt", "r").read()
        regex = re.search(condition, value)
        os.remove("Result.txt")
        return (value, regex)

    if count == "m":
        output = decoder(comm)
        log(output, file=open(f"Result.txt", "w"))
        value = open(f"Result.txt", "r").read()
        result = []
        res = re.finditer(condition, value)
        os.remove("Result.txt")
        for match in res:
            result.append(match.span())
        return (value, result)


def check(value, condition):
    regex = re.search(condition, value)
    return regex


def checkIter(value, condition):
    result = []
    res = re.finditer(condition, value)
    for match in res:
        result.append(match.span())
    return result


def txt2csvFormatter(file):
    f = open(file)
    lines = f.readlines()
    f.close()
    f = open(file, "w")
    for line in lines:
        f.write(line[1:].replace(" +", ""))
    f.close()


def sshToFile(comm, file, typeOfList):
    output = decoder(comm)
    if "U" not in typeOfList:
        log(output, file=open(f"{file}", "w"))
