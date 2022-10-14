import os
import re


def decoder(comm):
    data = ""
    chunk = comm.recv(65535)
    chunk = chunk.decode("latin1")
    data += chunk
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    data = ansi_escape.sub("", data)
    return data


def parser(comm, condition, count):
    if count == "s":
        output = decoder(comm)
        print(output, file=open("Result.txt", "w"))
        value = open("Result.txt", "r").read()
        regex = re.search(condition, value)
        os.remove("Result.txt")
        return (value, regex)

    if count == "m":
        output = decoder(comm)
        print(output, file=open(f"Result.txt", "w"))
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
