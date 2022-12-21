import re

def decoder(comm):
    data = ""
    chunk = comm.recv(1024000000)
    chunk = chunk.decode("latin-1")
    data += chunk
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    data = ansi_escape.sub("", data)
    return data

def check(value, condition):
    regex = re.search(condition, value)
    return regex


def checkIter(value, condition):
    result = []
    res = re.finditer(condition, value)
    for match in res:
        result.append(match.span())
    return result
