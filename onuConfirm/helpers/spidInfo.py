import re

conditionSPID = """Next valid free service virtual port ID: """


def getSPID(comm, commandToSend, enter):
    commandToSend("enable")
    commandToSend("config")
    commandToSend("display service-port next-free-index")
    enter()
    output = comm.recv(65535)
    output = output.decode("ascii")
    print(output, file=open("ResultSPID.txt", "w"))
    value = open("ResultSPID.txt", "r").read()
    result = re.search(conditionSPID, value)
    end = result.span()[1]
    spid = value[end:end+4]

    return spid
