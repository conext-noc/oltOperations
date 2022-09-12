def activate(actList, enter, commandToSend, exitInfo, comm, olt):
    commandToSend("enable")
    commandToSend("config")
    outputX = comm.recv(65535)
    outputX = outputX.decode("ascii")
    for client in actList:
        print(client)
        commandToSend(
            "interface gpon {}/{}".format(client["frame"], client["slot"]))
        commandToSend("ont activate {} {}".format(
            client["port"], client["id"]))
        commandToSend("display ont info {} {}".format(
            client["port"], client["id"]))
        enter()
        exitInfo()
        # outputClient = comm.recv(65535)
        # outputClient = outputClient.decode("ascii")
        # print(outputClient, file=open("onuOperate/CLIENTES/activate_{}-{}-{}-{}_OLT{}.txt".format(
        #     client["frame"], client["slot"], client["port"], client["id"], olt), "w"))
